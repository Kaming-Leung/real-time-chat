"""
ASGI config for a_core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'a_core.settings')

django_asgi_app = get_asgi_application() # Initial the application which only handles incoming HTTP requests

# Import the routing.py AFTER the get_asgi_application() !!!
from a_rtchat import routing

# Add a router so that the application can also handle web sockets
# AllowedHostsOriginValidator (security feature): make sure the connections are accepted in our listed allow hosts settings 
# AuthMiddlewareStack: gives us access to the login users
# URLRouter: map urls using the routing.py file
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
    ),
})
