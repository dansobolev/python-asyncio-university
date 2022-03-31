from aiohttp import web

from app.db.models import Upload
from app.uploads import add_upload, validate_upload, get_upload_path
from app.enums import UploadType
from app.exceptions import UploadNotFound


routes = web.RouteTableDef()


@routes.post('/upload-entity')
async def upload_comment_image(request: web.Request) -> web.Response:
    data = dict(await request.post())
    file = data.get('file')
    upload_type = UploadType[data.get('upload_type')]
    validate_upload(file, upload_type)
    upload = await add_upload(file, upload_type)

    return web.json_response({'upload_id': str(upload.id),
                              'upload_type': upload.type.name})


@routes.get('/images/{image_id}')
async def get_image(request: web.Request) -> web.FileResponse:
    upload_id = request.match_info['image_id']
    upload = await Upload.get(upload_id)
    if not upload:
        raise UploadNotFound

    upload_path = get_upload_path(upload)
    response = web.FileResponse(upload_path)
    return response


@routes.get('/attachment-doc/{doc_id}')
async def get_attachment_doc(request: web.Request) -> web.FileResponse:
    doc_id = request.match_info['doc_id']
    upload = await Upload.get(doc_id)
    if not upload:
        raise UploadNotFound

    upload_path = get_upload_path(upload)
    response = web.FileResponse(upload_path, headers={'Content-Disposition':
                                                      f"attachment; filename*=UTF-8''{upload.file_name}"})
    return response
