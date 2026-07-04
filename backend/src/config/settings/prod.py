from .base import *

DEBUG = False

SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DATABASE_NAME"),
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASSWORD"),
        'HOST': env("DATABASE_HOST"),
        'PORT': '5432',
    }
}

STATIC_ROOT = BASE_DIR / 'staticfiles'

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='eu-west-2')
AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN')
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

# Admin styling adjustment
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

STORAGES =  {'staticfiles': {'BACKEND': 'storages.backends.s3boto3.S3StaticStorage'}}

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# compression and caching support for Whitenoise
STORAGES = {
    'default': {
        "BACKEND": "storages.backends.s3.S3Storage"
    },

    "staticfiles": {
        'BACKEND': 'storages.backends.s3boto3.S3StaticStorage'
    }
}


# Modify these security settings for webhook compatibility
CSRF_COOKIE_SECURE = False if DEBUG else True
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_NAME = 'csrftoken'

# Add this to allow missing Referer header
CSRF_TRUSTED_ORIGINS = ['https://www.hazel.ng', 'https://hazel.ng']
CSRF_REFERER_REQUIRED = False
