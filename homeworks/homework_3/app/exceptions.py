from aiohttp.web import HTTPBadRequest


class MissingFieldException(HTTPBadRequest):
    pass
