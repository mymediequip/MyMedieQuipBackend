from .base import *

DOMAIN_NAME = 'http://13.53.198.145:8000/'

DEBUG = True
ALLOWED_HOSTS = ['localhost:4200', '*']


DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'mmq_live',
            'USER': 'mmq_live',
            'PASSWORD': 'tech',
            'HOST': 'localhost',
            'PORT': '5432',
            },
}

API_URL = "http://127.0.0.1:8000/api/v1/"
BASE_FILE_PATH = "http://13.53.198.145:8000/mmq_apps/"
# NEW_API_URL = "http://127.0.0.1:8000/api/v1/"

