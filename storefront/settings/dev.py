from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-7j1lx&zfaq4o2btzi16$t7t#p*rztq@9d0i+lq#2!t=bf80b4z'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bodytrak_db',
        'HOST': 'mysql',
        'USER': 'root',
        'PASSWORD': 'MyPassword2024'
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp4dev'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525
DEFAULT_FROM_EMAIL = 'thecloudavenger@gmail.com'


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        'TIMEOUT' : 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK' : lambda request: True
}