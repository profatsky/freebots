import os
from datetime import timedelta

from authx import AuthXConfig
from dotenv import load_dotenv

load_dotenv()

CLIENT_APP_URL = os.environ.get('CLIENT_APP_URL')

JWT_SECRET = os.environ.get('JWT_SECRET')

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
TEST_DB_NAME = os.environ.get('TEST_DB_NAME')


auth_config = AuthXConfig(
    JWT_ALGORITHM='HS256',
    JWT_SECRET_KEY=JWT_SECRET,
    JWT_TOKEN_LOCATION=['headers'],
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=30),
)
