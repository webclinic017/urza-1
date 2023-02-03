import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NewsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        await self.channel_layer.group_add("news", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("news", self.channel_name)

    # Send new article to all clients
    async def new_article(self, event):
        data = event["data"]
        await self.send(text_data=json.dumps(data))
