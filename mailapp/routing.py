from django.urls import path
from mailapp import consumers

websocket_urlpatterns = [
    path('ws/emails/', consumers.EmailConsumer.as_asgi()),
]
