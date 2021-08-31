from flask_restx import fields, Namespace
from flask_restx.reqparse import RequestParser
from flask import request
from http import HTTPStatus
from marshmallow_sqlalchemy.fields import Nested
from datetime import datetime, timedelta
from dateutil import parser as dparser

from openapi_genclient.models import (
    Operation as TinOperation,
    OperationTrade as TinOperationTrade,
    MoneyAmount
)
from app.logic.tinkoff_client import client, ACCOUNT_ID

from .common import Resource, abort
from app.models import ma
from .portfolio import MoneyAmountSchema
from app.logic.date import date_format

operations_ns = ns = Namespace(
    name="operations", description="CRUD operations", path="/operations"
)


class TinOperationTradeSchema(ma.Schema):
    class Meta:
        model = TinOperationTrade
        fields = [
            'date',
            'price',
            'quantity',
            'trade_id'
        ]


class TinOperationSchema(ma.Schema):
    commission = Nested(MoneyAmountSchema)
    trades = Nested(TinOperationTradeSchema, many=True)
    class Meta:
        model = TinOperation
        fields = [
            'date',
            'figi',
            'operation_type',
            'quantity',
            'price',
            'currency',
            'status',
            'trades',
            'instrument_type',
            'is_margin_call',
            'payment',
            'commission',
            'id',
        ]
        ordered = True

req_parser = RequestParser(bundle_errors=True)
req_parser.add_argument(
    name='from', type=str, required=False, nullable=True
)
req_parser.add_argument(
    name='to', type=str, required=False, nullable=True
)
req_parser.add_argument(
    name='hours', type=int, required=False, nullable=True
)


@ns.route('', endpoint='operations')
class OperationsResource(Resource):
    @ns.expect(req_parser)
    @ns.response(int(HTTPStatus.OK), description="Ok")
    @ns.response(int(HTTPStatus.BAD_REQUEST), description="Bad request")
    @ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), description="Server error")
    def get(self):
        assert type(ACCOUNT_ID) == str
        assert len(ACCOUNT_ID) > 0
        _from = request.args.get('from', default=None, type=str)
        to = request.args.get('to', default=date_format(datetime.now()), type=str)
        delta_hours = request.args.get('hours', default=16, type=int)
        dt_to = dparser.parse(to)
        to = date_format(dt_to)
        if not _from:
            dt_from = dt_to - timedelta(hours=delta_hours)
        else:
            dt_from = dparser.parse(_from)
        _from = date_format(dt_from)
        resp = client.operations.operations_get(_from=_from, to=to, broker_account_id=ACCOUNT_ID)

        assert resp.status == 'Ok'
        assert type(resp.payload.operations) == list
        # print('---', resp.payload.operations)

        operations = resp.payload.operations
        tin_operations_schema = TinOperationSchema()
        res = tin_operations_schema.dump(operations, many=True)

        return res, HTTPStatus.OK
