import datetime
from email.message import EmailMessage

from aiohttp import web
from aiohttp_security import remember, forget, authorized_userid
import aiohttp_jinja2

from app.db.models import UserPasswordResetLink
from app.db.queries import get_user_by_login, create_user, \
    get_user_by_email, check_user_uniqueness, get_user_by_id, is_valid_user
from app.enums import UploadType
from app.utils.password.hash import generate_hash, check_hash
from app.utils.validation import UserSchema
from app.mailing import send_email_message, jinja_env
from app.config import Config
from app.uploads import validate_upload, add_upload
from app.utils.password.exceptions import GeneratePasswordHashException, \
    CheckPasswordHashException
from app.exceptions import UserWithSuchLoginAlreadyExistedException, \
    UserNotFoundException, PasswordResetLinkNotFound, PasswordResetLinkExpired, \
    UserAlreadyExistingException

routes = web.RouteTableDef()


@routes.get('/register')
@routes.post('/register')
async def register(request: web.Request) -> web.Response:
    if request.method == 'GET':
        return aiohttp_jinja2.render_template('auth/register.html', request, context={})
    elif request.method == 'POST':
        # TODO: remove file upload here cause for this purpose there is seperate handler (upload_comment_image)
        data = dict(await request.post())
        file: web.FileField = data.get('profile_image')
        if file:
            validate_upload(file, UploadType.PROFILE_IMAGE)
            upload = await add_upload(file, UploadType.PROFILE_IMAGE)
            data['profile_image_id'] = upload.id
        del data['profile_image']

        login_ = data['login']
        email_ = data['email']
        existed_user = await check_user_uniqueness(login=login_, email=email_)
        if existed_user:
            raise UserAlreadyExistingException

        try:
            hashed_password = generate_hash(data['password'])
        except GeneratePasswordHashException:
            # TODO handle properly
            raise
        else:
            data.update({'password': hashed_password})

        try:
            await create_user(**data)
        except UserWithSuchLoginAlreadyExistedException:
            raise web.HTTPBadRequest
        url = request.app.router['login'].url_for()
        raise web.HTTPFound(location=url)


@routes.get('/login', name='login')
@routes.post('/login')
async def login(request: web.Request) -> web.Response:
    if request.method == 'GET':
        forgot_password_url = request.app.router['password-reset-request'].url_for()
        return aiohttp_jinja2.render_template('auth/login.html', request,
                                              context={'forgot_password_url': forgot_password_url})
    elif request.method == 'POST':
        data = await request.json()
        entity = data['identity']
        if entity.__contains__('@'):
            db_user = await get_user_by_email(data['identity'], raise_error=True)
        else:
            db_user = await get_user_by_login(data['identity'], raise_error=True)
        if not db_user:
            raise UserNotFoundException
        try:
            check_hash(data['password'], db_user.password)
        except CheckPasswordHashException:
            # TODO: make proper exception
            raise web.HTTPUnauthorized
        payload = str(db_user.id)
        # url = request.app.router['events'].url_for()
        # response = web.HTTPFound(location=url)
        response = web.json_response(UserSchema().dump(db_user))
        await remember(request, response, payload)
        return response


@routes.get('/logout')
async def logout(request: web.Request):
    redirect = request.app.router['login'].url_for()
    redirect_response = web.HTTPFound(location=redirect)
    await forget(request, redirect_response)
    raise redirect_response


@routes.get('/password-reset-request', name='password-reset-request')
@routes.post('/password-reset-request')
async def password_reset_request(request: web.Request) -> web.Response:
    if request.method == 'GET':
        return aiohttp_jinja2.render_template('auth/forgot_password_request.html', request, context={})
    elif request.method == 'POST':
        data = await request.post()
        db_user = await get_user_by_email(data['email'])
        if db_user:
            password_reset = await UserPasswordResetLink(user_id=db_user.id).create()

            message = EmailMessage()
            template = jinja_env.get_template('emails/password_reset.html')
            password_reset_url = \
                Config.BASE_URL + \
                str(request.app.router['password-reset-procedure'].url_for(reset_id=str(password_reset.id)))
            data = {
                'login': db_user.login,
                'username': db_user.fullname,
                'password_reset_link': password_reset_url
            }
            html_message = await template.render_async(**data)
            message.add_alternative(html_message, subtype='html')
            send_email_message(message, send_to=db_user.email)

            url = request.app.router['health'].url_for()
            raise web.HTTPFound(location=url)


@routes.get('/password-reset-procedure/{reset_id}', name='password-reset-procedure')
@routes.post('/password-reset-procedure/{reset_id}')
async def password_reset_procedure(request: web.Request) -> web.Response:
    if request.method == 'GET':
        link_id = request.match_info['reset_id']
        password_reset_db = await UserPasswordResetLink.get(link_id)
        if not password_reset_db:
            raise PasswordResetLinkNotFound
        time_created = password_reset_db.created_at
        if password_reset_db.is_expired or \
                time_created + datetime.timedelta(days=3) < datetime.datetime.now():
            raise PasswordResetLinkExpired

        return aiohttp_jinja2.render_template('auth/forgot_password_form.html', request, context={})

    elif request.method == 'POST':
        data = await request.post()
        new_password = data['password']
        try:
            hashed_password = generate_hash(new_password)
        except GeneratePasswordHashException:
            # TODO handle properly
            raise

        link_id = request.match_info['reset_id']
        password_reset_db = await UserPasswordResetLink.get(link_id)
        user_db = await password_reset_db.user

        await password_reset_db.update(is_expired=True).apply()
        await user_db.update(password=hashed_password).apply()

        login_url = request.app.router['login'].url_for()
        raise web.HTTPFound(location=login_url)


@routes.get('/change-password', name='change-password')
@routes.post('/change-password')
async def change_password(request: web.Request) -> web.Response:
    if request.method == 'GET':
        return aiohttp_jinja2.render_template('auth/change_password.html', request, context={})
    elif request.method == 'POST':
        data = dict(await request.post())
        user_id = await authorized_userid(request)
        if not user_id:
            print("You are not authorized")
            raise
        db_user = await get_user_by_id(user_id)

        # TODO: do check directly while getting user
        await is_valid_user(db_user)

        old_password = data['old_password']
        try:
            check_hash(old_password, db_user.password)
        except CheckPasswordHashException:
            # TODO: make proper exception
            raise web.HTTPUnauthorized

        new_password = data['new_password_1']
        new_password_retry = data['new_password_2']
        if new_password != new_password_retry:
            print("Введенные пароли не совпадают")
            raise

        try:
            hashed_password = generate_hash(new_password)
        except GeneratePasswordHashException:
            # TODO handle properly
            raise

        if hashed_password == db_user.password:
            print("Новый пароль совпадает со старым")
            raise

        await db_user.update(password=hashed_password).apply()
        url_login = request.app.router['login'].url_for()
        raise web.HTTPFound(location=url_login)
