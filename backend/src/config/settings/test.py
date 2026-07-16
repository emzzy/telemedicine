from .base import *
from .dev import SECRET_KEY

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "ATOMIC_REQUESTS": False
    }
}

SECRET_KEY = SECRET_KEY