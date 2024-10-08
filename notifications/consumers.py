import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Notification
from api.v1.deps import get_current_user


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
     #   headers = dict(self.scope['headers'])
      #  access_token = headers.get('Authorization')
      #  await get_current_user(access_token)
        
      #  self.receiver_id = user_data.get('id')
      #  if not self.receiver_id:
      #      await self.close()
      #      return
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        await self.channel_layer.group_add(
            self.receiver_id,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.receiver_id,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)

        await self._save_notification(json_data)

        await self.channel_layer.group_send(
            self.receiver_id, {
                'type': 'send_notification',
                'text': json_data.get('text'),
                'event_link': json_data.get('event_link'),
                'receiver_id': self.receiver_id,

            }
        )
        
    async def send_notification(self, event):
        json_data = {
            'text': event.get('text'),
            'event_link': event.get('event_link'),
            'receiver_id': self.receiver_id,
        }
        text_data = json.dumps(json_data)
        await self.send(text_data)

    @sync_to_async
    def _save_notification(self, data):
        data['receiver_id'] = self.receiver_id
        return Notification.objects.create(**data)