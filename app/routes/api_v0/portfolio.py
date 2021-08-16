from flask_restx import fields, Namespace
from flask_restx.reqparse import RequestParser
from flask import request
from http import HTTPStatus
from marshmallow_sqlalchemy.fields import Nested

from openapi_genclient.models import (
    PortfolioPosition as TinPortfolioPosition,
    MoneyAmount
)
from app.logic.tinkoff_client import client, ACCOUNT_ID

from .common import Resource, abort
from app.models import ma

portfolio_ns = ns = Namespace(
    name="portfolio", description="CRUD portfolio", path="/portfolio"
)

class MoneyAmountSchema(ma.Schema):
    class Meta:
        model = MoneyAmount
        fields = [
            'currency',
            'value',
        ]


class TinPositionSchema(ma.Schema):
    average_position_price = Nested(MoneyAmountSchema)
    expected_yield = Nested(MoneyAmountSchema)
    class Meta:
        model = TinPortfolioPosition
        fields = [
            'ticker',
            'name',
            'lots',
            'balance',
            'average_position_price',
            'expected_yield',
            'instrument_type',
            'blocked',
            # 'average_position_price_no_nkd',
            'figi',
            # 'isin',
        ]
        ordered = True


@ns.route("", endpoint='portfolio')
class PortfolioResource(Resource):
    def get(self):
        assert type(ACCOUNT_ID) == str
        assert len(ACCOUNT_ID) > 0
        pf = client.portfolio.portfolio_get(broker_account_id=ACCOUNT_ID)
        # print('---', pf)
        assert pf.status == 'Ok'
        assert type(pf.payload.positions) == list

        positions = pf.payload.positions
        tin_position_schema = TinPositionSchema()
        res = tin_position_schema.dump(positions, many=True)

        return res, HTTPStatus.OK
