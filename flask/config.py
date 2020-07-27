import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('EMAIL_USER')
    # MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

print(Config.test)

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    TESTING = False


class ProductionConfig(BaseConfig):
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    DEBUG = False