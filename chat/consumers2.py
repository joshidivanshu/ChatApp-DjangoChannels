import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
from channels.db import database_sync_to_async
from chat.services import chat_save_message



class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name


        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name, {
            "type": "chat_message",
            "message":"",
            'username': self.scope['user'].username.title(),
            'is_logged_in': True
                                
        })

    async def disconnect(self, close_code):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name


        await self.channel_layer.group_send(
            self.room_group_name, {
            "type": "chat_message",
            "message":"",
            'username': self.scope['user'].username.title(),
            'is_logged_in': False
        
    })


    async def chat_message(self, event):
        status = event['is_logged_in']
        user = event['username']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"status": status, "user":user}))




# class StatusConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name


#         await self.channel_layer.group_send(
#             self.room_group_name, {
#             "type": "chat_message",
#             "message":"",
#             'username': self.scope['user'].username.title(),
#             'is_logged_in': True
                                
#     })

#     async def disconnect(self, close_code):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name


#         await self.channel_layer.group_send(
#             self.room_group_name, {
#             "type": "chat_message",
#             "message":"",
#             'username': self.scope['user'].username.title(),
#             'is_logged_in': False
        
#     })


#     async def chat_message(self, event):
#         status = event['is_logged_in']
#         user = event['username']
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({"status": status, "user":user}))
