from flask_restx import fields, Namespace
from flask_restx.reqparse import RequestParser
from flask import request
from http import HTTPStatus
from marshmallow_sqlalchemy.fields import Nested
from collections import OrderedDict

from openapi_genclient.models import (
    PortfolioPosition as TinPortfolioPosition,
    Order as TinOrder,
    MoneyAmount
)
from app.logic.tinkoff_client import client, ACCOUNT_ID

from .common import Resource, abort
from app.models import ma, Stock

orders_ns = ns = Namespace(
    name="orders", description="CRUD orders", path="/orders"
)

class TinOrderSchema(ma.Schema):
    class Meta:
        model = TinOrder
        fields = [
            'figi',
            'operation',    # 'Buy',
            'type',         # 'Limit',
            'price',
            'requested_lots',
            'executed_lots',
            'status',       # 'New',
            'order_id',
        ]
        ordered = True



@ns.route('', endpoint='orders')
class PortfolioResource(Resource):
    def get(self):
        """
        Get active orders list
        """
        assert type(ACCOUNT_ID) == str
        assert len(ACCOUNT_ID) > 0
        resp = client.orders.orders_get(broker_account_id=ACCOUNT_ID)
        # print('---', resp)
        assert resp.status == 'Ok'
        assert type(resp.payload) == list
        orders = resp.payload
        # tin_order_schema = TinOrderSchema()
        # res = tin_order_schema.dump(orders, many=True)
        my_orders = []
        for o in orders:
            stock = Stock.query.filter(Stock.figi == o.figi).limit(1).one()
            od = OrderedDict(
                ticker=stock.ticker,
                operation=o.operation,
                type=o.type,
                price=o.price,
                requested_lots=o.requested_lots,
                executed_lots=o.executed_lots,
                status=o.status,
                order_id=o.order_id,
                currency=stock.currency,
                lot=stock.lot
            )
            my_orders.append(od)
        return my_orders, HTTPStatus.OK
