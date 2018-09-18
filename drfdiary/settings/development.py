from .base import *

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'drfdiary_dev',
        'USER':     'postgres',
        'PASSWORD': '',
        'HOST':     'localhost',
        'PORT':     '',
    }
}
