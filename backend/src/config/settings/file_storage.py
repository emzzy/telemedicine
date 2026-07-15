import os
from .base import BASE_DIR
from decouple import config


# # compression and caching support for Whitenoise
# STORAGES = {
#     'default': {
#         "BACKEND": "storages.backends.s3.S3Storage",
#         #'BACKEND': 'django.core.files.storage.FileSystemStorage',
#         'OPTIONS': {},
#     },

#     "staticfiles": {
#         'BACKEND': 'storages.backends.s3boto3.S3StaticStorage',
#         # "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

# AWS Config
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN')
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

# File uploads
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#MEDIA_URL = '/media/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
