from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.test import TestCase

from server_apps.trading.consumers import TradingConsumer


class TradingTest(TestCase):

    async def test_trading_consumer(self):
        communicator = WebsocketCommunicator(TradingConsumer.as_asgi(), "/ws/trading/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        # Send (news) json
        channel_layer = get_channel_layer()
        await channel_layer.group_send("trading", {"test": "test"})
        response = await communicator.receive_from()
        self.assertEqual(response, {"status": "Ok"})

        await communicator.disconnect()
