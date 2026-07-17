from .base import *

DEBUG = os.getenv("DEBUG")

SECRET_KEY = os.getenv("SECRET_KEY")

CORS_ALLOW_ALL_ORIGINS = True

ALLOWED_HOSTS = []

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

# STORAGES = {
#     'default': {
#         'BACKEND': 'django.core.files.storage.FileSystemStorage',
#         'OPTIONS': {}
#     },

#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     }
# }

STATIC_URL = "static/"

STATICFILES_DIRS = [
    #BASE_DIR / 'frontend' / 'static',
    BASE_DIR / 'staticfiles',
    BASE_DIR / 'static',
    BASE_DIR / 'backend' / 'staticfiles'
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

SITE_URL='http://localhost:5173'

MEDIA_URL = '/media/'