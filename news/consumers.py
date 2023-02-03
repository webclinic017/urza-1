from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NewsConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add("news", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("news", self.channel_name)

    # Receive new article from webcrawler
    async def receive(self, content):
        # Send message to channel layer
        await self.channel_layer.group_send(
            "news", {"type": "new_article", "content": content}
        )

    # Receive message from channel layer
    async def new_article(self, event):
        content = event["content"]
        # Send new article to all clients
        await self.send_json(content)
