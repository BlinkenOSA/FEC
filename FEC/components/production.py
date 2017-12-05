# SECURITY WARNING: keep the secret key used in production secret!
import os

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")