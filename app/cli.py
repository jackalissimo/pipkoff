import click
from flask import Flask
from flask.cli import AppGroup
# from .models.common import db
# from flask_sqlalchemy import SQLAlchemy
from app.models import (
    db, Stock
)
from app.logic.stock import stock_init_db


stock_cli = AppGroup('stock')
@stock_cli.command('init-db')
def cmd_stock_init_db():
    """
    $ flask stock init-db  --- populates stocks table
    """
    stock_init_db()


# DB Create based on Models
mydb_cli = AppGroup('mydb')
@mydb_cli.command('create_all')
def db_create():
    print(db)
    db.create_all()

@mydb_cli.command('drop_all')
def db_drop():
    print(db)
    db.drop_all()


def init_cli(application: Flask):
    application.cli.add_command(stock_cli)
    application.cli.add_command(mydb_cli)
