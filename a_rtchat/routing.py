from django.urls import path
from .consumers import *  # consumers.py is the same as views.py but for web sockets connection


websocket_urlpatterns = [
    path("ws/chatroom/<chatroom_name>", ChatroomConsumer.as_asgi()),
]