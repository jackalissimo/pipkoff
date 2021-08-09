import logging
from logging.handlers import TimedRotatingFileHandler

class ErrorLogger:
    def __init__(self, app):
        filename = app.config.get("ERROR_LOG_FILE", "log/error.log")
        logging.basicConfig(
            handlers=[ TimedRotatingFileHandler(filename, when='D', backupCount=10) ],
            level=logging.ERROR,
            format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
            datefmt='%Y-%m-%dT%H:%M:%S'
        )
