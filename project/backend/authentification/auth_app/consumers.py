from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .redis_client import r
from .utils_views import utils_get_user
import json


class User_connection(AsyncWebsocketConsumer):
        
    async def connect(self):
        cookies = {}
        headers = dict(self.scope["headers"])
        if b"cookie" in headers:
            cookie_header = headers[b"cookie"].decode()
            cookies = {key: value for key, value in [cookie.split('=') for cookie in cookie_header.split('; ')]}
        else :
            await self.close()
            return
        
        token = cookies.get('token')
        refresh_token = cookies.get('refresh_token')
        token42 = cookies.get('42_access_token')
        self.user = await self.sync_utils_get_user(token, refresh_token, token42)
        if self.user is None:
            await self.close()
            return
        self.group_name = f'user_{self.user.id}' #mettre le user dans un groupe de son id permet de gerer les connections multiples du meme user, expl plusieur pages ouvertes
        await self.channel_layer.group_add(
        self.group_name,
        self.channel_name # id unique de l'instance de AsyncWebsocketConsumer
        )
        await self.accept()
        await self.update_user_status('online')
        await self.notify_friends('online')
        await self.get_friends_status()

    async def disconnect(self, close_code):
       if hasattr(self, "user"):
            if hasattr(self, "group_name"):
                await self.channel_layer.group_discard(
                    self.group_name,
                    self.channel_name
            )
            await self.update_user_status('offline')
            await self.delete_twoFA_data()
            await self.notify_friends('offline')

    async def receive(self, text_data):
        pass

    async def send(self, text_data):
       pass

    @sync_to_async # l'operation sur redis est synchrone et bloquante, donc on utilise sync_to_async pour la rendre asynchrone
    def update_user_status(self, status):
        r.set(f'user_{self.user.id}_status', status)
    
    @sync_to_async
    def delete_twoFA_data(self):
        r.delete(f'user_{self.user.id}_twoFA_verified')
        r.delete(f'user_{self.user.id}_twoFA_code')
    
    async def notify_friends(self, status):
        friends = await self.get_friends_list()
        for friend in friends:
            
            await self.channel_layer.group_send(
                f'user_{friend.id}',
                {
                    'type': 'send_user_status_update',
                    'user_id': self.user.id,
                    'status': status,
                }
            )
    
    async def send_user_status_update(self, event):
        await self.send(text_data=json.dumps({
            'user_id': event['user_id'],
            'status': event['status'],
        }))
    
    async def get_friends_status(self): 
        friends = await self.get_friends_list()
        for friend in friends:
            status = await self.get_user_status(friend.id)
            await self.send(text_data=json.dumps({
                'user_id': friend.id,
                'status': status,
            }))
    
    @sync_to_async
    def get_user_status(self, user_id):
        return r.get(f'user_{user_id}_status').decode()
    
    @sync_to_async
    def get_friends_list(self):
        return list(self.user.custom_user.friends_list.all())
        #return self.user.custom_user.friends_list.all()
    
    @staticmethod
    @sync_to_async
    def sync_utils_get_user(token, refresh_token, token42):
        return utils_get_user(token, refresh_token, token42)