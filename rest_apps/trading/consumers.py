from channels.generic.websocket import AsyncJsonWebsocketConsumer

from event_controller.alpaca_news import start_alpaca_news_stream


class TradingConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add("trading", self.channel_name)
        await start_alpaca_news_stream()
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("trading", self.channel_name)

    # Receive trade from client
    async def receive(self, text_data):
        print(text_data)

    # Receive news article and send to client
    async def new_article(self, article):
        await self.channel_layer.group_send(text_data=article)
