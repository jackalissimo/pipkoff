from flask import Flask, send_from_directory
# from flask_cors import CORS
# from utils.error_logger import ErrorLogger
# from utils.auth import init_jwt
from app.models import init_db
from app.cli import init_cli
from os import environ


def init_routes(application: Flask):
    import app.routes

    for bp_name in app.routes.__all__:
        bp = getattr(app.routes, bp_name)
        application.register_blueprint(bp)

    @application.route('/public/<path:filename>')
    def base_static(filename):
        return send_from_directory(application.root_path + '/../public/', filename)


def create_app(env=None):
    application = Flask(__name__)
    if env is not None:
        application.env = env
    application.config.from_object(f"app.config.{application.env.capitalize()}")
    # ErrorLogger(application)
    init_db(application)
    init_cli(application)
    # # CORS(application)
    # CORS(application, resources={r"/*": {"origins": "*"}})
    # init_jwt(application)
    # init_routes(application)

    return application

app = create_app()
print('heeeeey, app')
