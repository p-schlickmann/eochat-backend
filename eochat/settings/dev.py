from eochat.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'anything'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

CLIENT_URL = 'http://localhost:3000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'eochat',
        'USER': 'mendespedro',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}
