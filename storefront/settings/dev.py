from .common import *


DEBUG = True

SECRET_KEY = "o_-qd9acy3+&4hh1xm(#ntv(wit3)pf&%^97xl)y!(7^0^&bhe3jrh1$gm_1s3g#_ft^%5gb!p!188cbf@h0*o@t#*3$)"

MIDDLEWARE += [
    "silk.middleware.SilkyMiddleware",
]

DATABASES = {
    "default": {
        #** When using MySQL, you must install the MySQL client library (mysqlclient) globally and in the virtual environment.
        "ENGINE": "django.db.backends.mysql",
        "NAME": "storefront",
        "HOST": "localhost",
        "USER": "fachiis",
        "PASSWORD": "this is fachiis",
        "PORT": "3306",
    }
}

CELERY_BROKER_URL = "redis://redis:6379/1"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/2",
        #** Set the expiration time in minute for the cached data in memory
        #** 10 minutes before the cache expires
        "TIMEOUT": 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# SMTP Server Configuration
EMAIL_HOST = "smtp4dev"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 2525

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: True}
