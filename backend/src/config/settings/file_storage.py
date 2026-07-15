# import os
# from .base import BASE_DIR

# # # compression and caching support for Whitenoise
# # STORAGES = {
# #     'default': {
# #         "BACKEND": "storages.backends.s3.S3Storage",
# #         #'BACKEND': 'django.core.files.storage.FileSystemStorage',
# #         'OPTIONS': {},
# #     },

# #     "staticfiles": {
# #         'BACKEND': 'storages.backends.s3boto3.S3StaticStorage',
# #         # "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
# #     },
# # }

# # AWS Config
# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
# AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')
# STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

# # File uploads
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# #MEDIA_URL = '/media/'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
