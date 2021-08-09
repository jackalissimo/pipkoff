from flask_restx._http import HTTPStatus
from flask_restx import Resource as OriginalResource
from flask_restx.utils import unpack
import flask
from werkzeug.exceptions import HTTPException


def response_method_docorator(method):
    def wrapped(*args, **kwargs):
        if method.__name__ == "options":
            return method(*args, **kwargs)
        else:
            body, code, headers = unpack(method(*args, **kwargs))
            return {"data": body, "success": True}, code, headers

    return wrapped


def abort(code=HTTPStatus.INTERNAL_SERVER_ERROR, message=None, **kwargs):
    try:
        flask.abort(code)
    except HTTPException as e:
        kwargs["success"] = False
        if message:
            kwargs["error"] = str(message)
        if kwargs:
            e.data = kwargs
        raise


class Resource(OriginalResource):
    method_decorators = [response_method_docorator]
