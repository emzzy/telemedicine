from settings.dev import os

# tell celery about Redis - same URL as CACHES setting
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
