import os
from openapi_client import openapi


class TestBaseApi:
    def setup_class(self):
        AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
        self.ACCOUNT_ID = os.environ.get('ACCOUNT_ID')
        self.client = openapi.api_client(AUTH_TOKEN)
