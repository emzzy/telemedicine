from .base import *
from .dev import SECRET_KEY

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "ATOMIC_REQUESTS": True,
        "NAME": ":memory:"
    }
}

SECRET_KEY = SECRET_KEY