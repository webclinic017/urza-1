import pytest
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator

from server_apps.trading.consumers import TradingConsumer

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


@pytest.mark.asyncio
class TestTrading:
    async def test_trading_websocket(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(TradingConsumer.as_asgi(), "/ws/trading/")
        connected, subprotocol = await communicator.connect()
        assert connected

        # Send (news) json
        channel_layer = get_channel_layer()
        await channel_layer.group_send("trading", {"test": "test"})
        response = await communicator.receive_from()
        assert response == {"status": "Received Trade"}

        await communicator.disconnect()
