import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Message

from icecream import ic


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.room_name = self.scope["url_route"]["kwargs"].get(
                "room_name", "default_room"
            )

            host = dict(self.scope["headers"]).get(b"host", None)
            subdomain = None

            if host:
                host = host.decode("utf-8")
                domain_parts = host.split(".")
                subdomain = domain_parts[0]

            if subdomain:
                self.room_group_name = f"{subdomain}"
            else:
                self.room_group_name = f"chat_{self.room_name}"

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

        except Exception as e:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message", "")
            user = self.scope["user"]

            print(user.first_name)

            if not isinstance(user, AnonymousUser):
                await self.save_message(user, self.room_group_name, message)
                username = f"{user.first_name} {user.last_name}"  # Get the username
            else:
                username = "Anonymous"

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": username,  # Include the username
                },
            )
        except Exception as e:
            print(f"Error during message receiving: {e}")

    async def chat_message(self, event):
        try:
            message = event["message"]
            username = event["username"]  # Retrieve the username from the event

            await self.send(
                text_data=json.dumps(
                    {
                        "message": message,
                        "username": username,  # Include the username in the response
                    }
                )
            )
        except Exception as e:
            print(f"Error during message sending: {e}")

    @database_sync_to_async
    def save_message(self, user, room_name, content):
        Message.objects.create(user=user, room_name=room_name, content=content)
