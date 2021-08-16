import json
from datetime import datetime, timedelta

from flask_restx import fields, Namespace
from flask_restx.reqparse import RequestParser
from flask import request
from http import HTTPStatus
from dateutil import parser as dparser

from .common import Resource, abort
from app.models import (
    ma, Stock
)

parser_ns = ns = Namespace(
    name="market", description="CRUD market", path="/market"
)

