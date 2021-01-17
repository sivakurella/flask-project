from .env_vars import *

class Config:
    DEBUG=True
    SQLALCHEMY_DATABASE_URI=f'postgresql+psycopg2://{DB_USER}:{DB_PASSWD}@localhost:{DB_PORT_NO}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
