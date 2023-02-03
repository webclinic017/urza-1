import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NewsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add("news", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("news", self.channel_name)

    # Receive message from client
    async def receive(self, text_data):
        text_from_json = json.loads(text_data)
        data = text_from_json["data"]
        msg_type = ["type"]
        await self.channel_layer.group_send("news", {"type": msg_type, "data": data})

    # Send new article to all clients
    async def new_article(self, event):
        data = event["data"]
        await self.send(text_data=json.dumps(data))

    # Send each response to a new article to every (other) client
    async def article_response(self, event):
        data = event["data"]
        await self.send(text_data=json.dumps(data))
