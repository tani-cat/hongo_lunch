import os
import django_heroku
import dj_database_url

from .base import *


DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com']

SECRET_KEY = os.environ['SECRET_KEY']

db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=False)

DATABASES = {
    'default': dj_database_url.config(),
}
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ERROR_WEBHOOK_URL = os.environ['ERROR_WEBHOOK_URL']

django_heroku.settings(locals())
