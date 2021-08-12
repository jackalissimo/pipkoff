from flask import Blueprint, request, url_for
from flask_restx import Api as OriginalApi
from werkzeug.exceptions import HTTPException

from .market import market_ns
# from .portfolio import portfolio_ns
from .stock import stock_ns

namespaces = [
    market_ns,
    # portfolio_ns,
    stock_ns,
]


class Api(OriginalApi):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        scheme = request.headers.get("X-Forwarded-Proto", "http")
        return url_for(self.endpoint("specs"), _external=True, _scheme=scheme)


api_v0_bp = Blueprint("api_v0", __name__, url_prefix="/api/v0")
api = Api(
    api_v0_bp,
    title="PIPKOFF JSON-API",
    version="0",
    description="Api methods documentation",
    doc='/ui'
)


@api_v0_bp.errorhandler(422)
def handle_validataion_error(error):
    if hasattr(error, "data"):
        data = str(error.data)
    else:
        data = str(error)
    return {"success": False, "message": str(error), "data": data}, 422


@api.errorhandler
def default_error_handler(error):
    return {"success": False, "data": str(error)}, getattr(error, "code", 500)


@api.errorhandler(HTTPException)
def http_exception_handler(error):
    return {"success": False, "data": str(error)}, getattr(error, "code", 500)


for ns in namespaces:
    api.add_namespace(ns)
