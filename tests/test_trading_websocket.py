import pytest
from channels.testing import WebsocketCommunicator

from server.asgi import application

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


@pytest.mark.asyncio
class TestTradingWebsocket:
    async def test_connect(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(application=application, path="/ws/news/")
        connected, _ = await communicator.connect()
        assert connected

        await communicator.disconnect()

    async def test_can_send_and_receive_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application,
            path='/ws/news/'
        )
        await communicator.connect()
        await communicator.send_json_to({"data": "test"})
        response = await communicator.receive_json_from()
        assert response == {"data": "test"}
        await communicator.disconnect()
