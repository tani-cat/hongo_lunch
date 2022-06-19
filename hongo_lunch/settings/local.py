import os

from .base import *
from .secret_key import _SECRET_KEY_CODE


DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# SECRET_KEYの設定についてはREADMEを参照
SECRET_KEY = _SECRET_KEY_CODE

# settings.pyからそのままコピー
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# 以下は共通項目への追加
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INSTALLED_APPS += (
    'debug_toolbar',
)
