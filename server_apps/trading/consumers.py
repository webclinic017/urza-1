import json

from channels.generic.websocket import AsyncWebsocketConsumer

from event_controller.alpaca_news import start_alpaca_news_stream


class TradingConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add("trading", self.channel_name)
        await start_alpaca_news_stream()
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("trading", self.channel_name)

    # Receive trade from client
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.channel_layer.group_send("trading", {"type": "trade_response", "message": message})

    # Send news article to client
    async def new_article(self, article):
        await self.channel_layer.group_send("trading", json.dumps(article))

    # Send trade response back to client
    async def trade_response(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
