import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import chat_room.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teleapp.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                chat_room.routing.websocket_urlpatterns
            )
        )
    }
)
