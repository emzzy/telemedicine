from settings.dev import env

# tell celery about Redis - same URL as CACHES setting
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
