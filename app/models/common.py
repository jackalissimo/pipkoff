from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

db = SQLAlchemy()
ma = Marshmallow()

def init_db(app: Flask):
    db.init_app(app)
    # Migrate(app, db)
    ma.init_app(app)
