from flask_restx import fields, Namespace
from flask_restx.reqparse import RequestParser
from flask import request
from http import HTTPStatus
from marshmallow_sqlalchemy.fields import Nested
from datetime import datetime, timedelta

from openapi_genclient.models import (
    Operation as TinOperation,
    OperationTrade as TinOperationTrade,
    MoneyAmount
)
from app.logic.tinkoff_client import client, ACCOUNT_ID

from .common import Resource, abort
from app.models import ma
from .portfolio import MoneyAmountSchema

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


@ns.route('', endpoint='operations')
class OperationsResource(Resource):
    def get(self):
        assert type(ACCOUNT_ID) == str
        assert len(ACCOUNT_ID) > 0
        dt1 = (datetime.now() - timedelta(hours=12)).strftime("%Y-%m-%dT%H:%M:%S+03:00")
        dt2 = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+03:00")
        resp = client.operations.operations_get(_from=dt1, to=dt2, broker_account_id=ACCOUNT_ID)

        assert resp.status == 'Ok'
        assert type(resp.payload.operations) == list
        # print('---', resp.payload.operations)

        # fields = [
        #     'date',
        #     'figi',
        #     'operation_type',
        #     'quantity',
        #     'price',
        #     'currency',
        #     'status',
        #     'trades',
        #     'instrument_type',
        #     'is_margin_call',
        #     'payment',
        #     'commission',
        #     'id',
        # ]
        # for op in resp.payload.operations:
        #     print('====')
        #     for el in fields:
        #         try:
        #             v = getattr(op, el)
        #             print('---', el, v, type(v))
        #             if type(v) == list:
        #                 print('-----', type(v[0]), v[0])
        #         except:
        #             pass

        operations = resp.payload.operations
        tin_operations_schema = TinOperationSchema()
        res = tin_operations_schema.dump(operations, many=True)

        return res, HTTPStatus.OK
