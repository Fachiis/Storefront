from .common import *


DEBUG = True

SECRET_KEY = "o_-qd9acy3+&4hh1xm(#ntv(wit3)pf&%^97xl)y!(7^0^&bhe3jrh1$gm_1s3g#_ft^%5gb!p!188cbf@h0*o@t#*3$)"

MIDDLEWARE += [
    "silk.middleware.SilkyMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "storefront",
        "HOST": "localhost",
        "USER": "fachiis",
        "PASSWORD": "zasha1996",
    }
}
