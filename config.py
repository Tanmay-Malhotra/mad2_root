class Config():
    DEBUG = False
    SQL_ALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    DEBUG = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'thisshouldbekeptsecret'
    SECRET_KEY = "shouldbekeyveryhidden"

    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"

    WTF_CSRF_ENABLED = False

    CACHE_TYPE = 'RedisCache'
    CACHE_KEY_PREFIX = 'my_prefix'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 4
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_DEBUG = True
    CACHE_REDIS_DEBUG = True

    MAIL_DEBUG = True
    DEBUG = True