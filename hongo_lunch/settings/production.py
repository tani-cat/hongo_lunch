import os
import django_heroku
import dj_database_url

from .base import *


DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com']

SECRET_KEY = os.environ['SECRET_KEY']

# MiddleWareはWhitenoiseのために上書きする
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=False)

DATABASES = {
    'default': dj_database_url.config(),
}
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ERROR_WEBHOOK_URL = os.environ['ERROR_WEBHOOK_URL']

django_heroku.settings(locals())
