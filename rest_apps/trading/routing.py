from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r"ws/trading/", consumers.TradingConsumer.as_asgi(), "ws-trading"),
]
