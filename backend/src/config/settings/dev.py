from .base import *

DEBUG = True

SECRET_KEY='django-insecure-a3*pv#(r*&tn5vjbj2@-ht@n18g@2-6op&73un1m3oz&55q)kq'

CORS_ALLOW_ALL_ORIGINS = True

ALLOWED_HOSTS = [
        "127.0.0.1",
        "localhost",
        "http://localhost:5173/"
    ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'teledb',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
        'OPTIONS': {}
    },

    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

STATIC_URL = "static/"

STATICFILES_DIRS = [
    #BASE_DIR / 'frontend' / 'static',
    BASE_DIR / 'staticfiles',
    BASE_DIR / 'static',
    BASE_DIR / 'backend' / 'staticfiles'
]

SITE_URL='http://localhost:5173'

MEDIA_URL = '/media/'