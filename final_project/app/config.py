import pathlib
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # common
    BASE_DIR = pathlib.Path(__file__).parent

    # database
    DB_NAME = os.getenv('DB_NAME', 'postgres')
    DB_USER = os.getenv('DB_USER', 'admin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_URL = rf'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    DB_SSL = bool(os.getenv('DB_SSL', False))

    # server
    AIO_HTTP_VERSION = os.getenv('AIO_HTTP_VERSION', 'http')
    AIO_HOST = os.getenv('AIO_HOST', 'localhost')
    AIO_PORT = int(os.getenv('AIO_PORT', 8080))
    BASE_URL = rf'{AIO_HTTP_VERSION}://{AIO_HOST}:{AIO_PORT}'

    # secrets
    SECRET_TOKEN = os.getenv('SECRET_TOKEN', 'secret_token')
    COOKIE_SECRET = os.getenv('COOKIE_SECRET', 'cookie_secret_token')

    # mailing
    EMAIL_ADMIN = os.getenv('EMAIL_ADMIN', 'admin@gmail.com')

    # admin
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@gmail.com')
    ADMIN_PHONE_NUMBER = os.getenv('ADMIN_PHONE_NUMBER', '+79999999999')

    # uploads
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/uploads')
    UPLOAD_FOLDER_PATH = str(pathlib.Path(__file__).parent.parent) + UPLOAD_FOLDER
    UPLOAD_DEFAULT_MAX_LENGTH = 1024 * 1024 * 50
    UPLOAD_ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx']
    UPLOAD_PROFILE_IMAGE_MAX_SIZE = int(os.getenv('UPLOAD_PROFILE_IMAGE_MAX_SIZE', 1024 * 1024 * 5))

    if not os.path.isdir(UPLOAD_FOLDER_PATH):
        os.mkdir(UPLOAD_FOLDER_PATH)
