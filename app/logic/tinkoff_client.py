from os import environ
from openapi_client import openapi


AUTH_TOKEN = environ.get('AUTH_TOKEN')
ACCOUNT_ID = environ.get('ACCOUNT_ID')
client = openapi.api_client(AUTH_TOKEN)
