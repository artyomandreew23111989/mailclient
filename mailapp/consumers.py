import json
from channels.generic.websocket import AsyncWebsocketConsumer

class EmailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('emails', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('emails', self.channel_name)

    async def email_created(self, event):
        await self.send(text_data=json.dumps(event['email']))
