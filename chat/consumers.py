import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
from channels.db import database_sync_to_async
from chat.services import chat_save_message, chat_delete_message



class ChatConsumer(AsyncWebsocketConsumer):
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
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.channel_layer.group_send(
            self.room_group_name, {
            "type": "chat_message",
            "message":"",
            'username': self.scope['user'].username.title(),
            'is_logged_in': False
        
    })

    async def receive(self, text_data):
        user = self.scope["user"]
        await login(self.scope, user)
        # save the session (if the session backend does not access the db you can use `sync_to_async`)
        await database_sync_to_async(self.scope["session"].save)()
        print(user)

        text_data_json = json.loads(text_data)
        message = str(user)+ ": " + text_data_json["message"]+ '\n'

        # Send message to room group
        if text_data_json["message"] != "":
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'chat_message',
                    'username': self.scope['user'].username.title(),
                    'message': message,
                    'is_logged_in': True
                }
            )

        
            await chat_save_message(
                username=self.scope['user'].username.title(),
                room_id=self.room_name,
                message=message
            )
        else:
            id = text_data_json["id"]
            await chat_delete_message(
                id = id
            )
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'chat_message',
                    'username': self.scope['user'].username.title(),
                    'message': message,
                    'is_logged_in': True
                }
            )


    async def chat_message(self, event):
        message = event["message"]
        status = event['is_logged_in']
        user = event['username']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "status": status, "user":user}))






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
