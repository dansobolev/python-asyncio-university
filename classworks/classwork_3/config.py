import pathlib


class Config(object):
    BASE_DIR = pathlib.Path(__file__).parent
    BASE_URL = 'http://127.0.0.1:8080'
