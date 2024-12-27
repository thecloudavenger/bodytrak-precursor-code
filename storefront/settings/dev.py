from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-7j1lx&zfaq4o2btzi16$t7t#p*rztq@9d0i+lq#2!t=bf80b4z'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bodytrak_db',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'MyPassword2024'
    }
}
