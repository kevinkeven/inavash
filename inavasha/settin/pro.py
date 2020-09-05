from .base import *

DEBUG = False

ADMINS = ('kevin keven', 'kevinkeven20@gmail.com')

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog',
        'USER': 'mysite',
        'PASSWORD': 'mysite',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}