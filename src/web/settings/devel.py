from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY='django-insecure-THIS_IS_NOT_A_SECRET_KEY'
print('**WARNING**: Using insecure key. Fine if running midsin_web locally.')

TIME_ZONE = 'UTC'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
