import json

from channels.generic.websocket import AsyncWebsocketConsumer


class TradingConsumer(AsyncWebsocketConsumer):
    # Receive trade from client
    async def receive(self, trade):
        trade_json = json.loads(trade)
        print(trade)

    # Receive news article and send to client
    async def new_article(self, article):
        await self.send(text_data=json.dumps(article))
