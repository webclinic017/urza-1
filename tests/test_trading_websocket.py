from channels.testing import WebsocketCommunicator
from django.test import TestCase

from server_apps.trading.consumers import TradingConsumer


class TradingTest(TestCase):

    async def test_trading_consumer(self):
        communicator = WebsocketCommunicator(TradingConsumer.as_asgi(), "/ws/trading/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        # Test sending text
        await communicator.send_to(text_data="hello")
        response = await communicator.receive_from()
        self.assertEqual(response, "hello")
        # Close
        await communicator.disconnect()
