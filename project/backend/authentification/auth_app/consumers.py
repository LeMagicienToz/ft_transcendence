from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

r = redis.StrictRedis(host='redis', port=6379, db=0) #cree une instance
class User_connection(AsyncWebsocketConsumer):
        async def connect(self):
                self.user = self.scope['user']
                self.user_id = self.user.id
                self.group_name = f'user_{self.user_id}' #mettre le user dans un groupe de son id permet de gerer les connections multiples du meme user, expl plusieur pages ouvertes
        
                await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
                )
                await self.accept()
                await self.update_user_status('online')
        
        async def disconnect(self, close_code):
                await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
                )
                await self.update_user_status('offline')

        @sync_to_async
        def update_user_status(self, status):
            r.set(f'user_{self.user_id}_status', status)