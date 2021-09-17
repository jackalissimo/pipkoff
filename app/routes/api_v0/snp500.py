from flask_restx import fields, Namespace
from http import HTTPStatus

from .common import Resource, abort
from app.logic.snp500 import parse_snp500_wiki


snp500_ns = ns = Namespace(
    name="snp500", description="CRUD S&P500", path="/snp500"
)


@ns.route("/parse", endpoint='snp500-parse')
class Snp500ParserResource(Resource):
    @ns.response(int(HTTPStatus.OK), description="Ok")
    @ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), description="Server error")
    def post(self):
        res = {}
        try:
            res = parse_snp500_wiki()
        except Exception as e:
            abort(message=str(e))
        return res, HTTPStatus.OK
