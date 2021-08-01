import os
from os.path import (join, dirname, realpath)
from dotenv import load_dotenv


PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_NAME = "pipkoff-api"
dotenv_path = join(dirname(dirname(realpath(__file__))), '.env')
load_dotenv(dotenv_path)
print('heeeeey, congfig')


def get_db_connection_string():
    password = os.environ.get("POSTGRES_PASSWORD")
    username = os.environ.get("POSTGRES_USER")
    dbname = os.environ.get("POSTGRES_DB")
    hostname = os.environ.get("POSTGRES_HOST", "postgres")
    port = os.environ.get("POSTGRES_PORT", 5432)
    return f"postgresql://{username}:{password}@{hostname}:{port}/{dbname}?target_session_attrs=read-write"


def read_key(filename):
    keys_dir = os.environ.get("KEYS_DIR", "keys")
    with open(f"{keys_dir}/{filename}") as fh:
        return fh.read()


class Config:
    ADMINS = ["jackal364hype@yandex.ru"]
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "keamMO7787#ihf2h9hh560Gp2.bh3d6#"
    )
    JWT_ALGORITHM = "RS256"
    # JWT_PUBLIC_KEY = read_key("public.pem")
    JWT_COOKIE_DOMAIN = ".jackalsite"
    JWT_DECODE_LEEWAY = 15
    JWT_TOKEN_LOCATION = ("headers", "cookies", "query_string")
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_REFRESH_COOKIE_NAME = "refresh_token"
    JWT_COOKIE_CSRF_PROTECT = False
    # JWT_BLACKLIST_ENABLED = True
    # JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_db_connection_string()

    TEMPLATES_AUTO_RELOAD = True
    ERROR_LOG_FILE = f"{PROJECT_PATH}/log/{PROJECT_NAME}.error.log"


class Testing(Config):
    PRESERVE_CONTEXT_ON_EXCEPTION = 1
    FLASK_DEBUG = 1
    TESTING = 1
    # SQLALCHEMY_ECHO = True

class Development(Config):
    FLASK_DEBUG = int(os.environ.get("FLASK_DEBUG", 1))
    # SQLALCHEMY_ECHO = True

class Production(Config):
    FLASK_DEBUG = int(os.environ.get("FLASK_DEBUG", 0))
