from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .redis_client import r

class User_connection(AsyncWebsocketConsumer):
        async def connect(self):
                self.user = self.scope['user']
                self.group_name = f'user_{self.user.id}' #mettre le user dans un groupe de son id permet de gerer les connections multiples du meme user, expl plusieur pages ouvertes
        
                await self.channel_layer.group_add(
                self.group_name,
                self.channel_name # id unique de l'instance de AsyncWebsocketConsumer
                )
                await self.accept()
                await self.update_user_status('online')
        
        async def disconnect(self, close_code):
                await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
                )
                await self.update_user_status('offline')
                await self.delete_twoFA_data()

        @sync_to_async # l'operation sur redis est synchrone et bloquante, donc on utilise sync_to_async pour la rendre asynchrone
        def update_user_status(self, status):
            r.set(f'user_{self.user.id}_status', status)
        
        @sync_to_async
        def delete_twoFA_data(self):
            r.delete(f'user_{self.user.id}_twoFA_verified')
            r.delete(f'user_{self.user.id}_twoFA_code')
