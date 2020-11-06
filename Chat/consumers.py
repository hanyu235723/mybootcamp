from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Messager

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name,
                                                    self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name,
                                                        self.channel_name)
    def fetch_message(self,data):
        # message is list
        messages = Messager.get_last_10_messages()
        messagelist = []
        # each message is a Message instance
        #serialize is a process to transform class object into str? because only string can be transfer
        for message in messages:
            messagelist.append({
                'author': message.author.first_name,
                'content': message.content,
                'timestamp': str(message.create_date)
            })
        content = {
            'command':'fetch_message',
            'message': messagelist
        }
        print (messagelist)

        self.send(text_data=json.dumps(content))
  
    def new_message(self, data):
        newmessage = Messager()
        User = get_user_model()
        author = User.objects.get(first_name=data['from'])
        newmessage.author = author
        newmessage.content = data['message']
        newmessage.create_date = timezone.now()
        newmessage.save()
        content = {
            'command':'new_message',
            'message': {
                'author': newmessage.author.first_name,
                'content': newmessage.content,
                'timestamp': str(newmessage.create_date)
            }
        }
        self.send_message(content)

    commands = {'fetch_message': fetch_message, 'new_message': new_message}

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self,data)

    def send_message(self, content):
      
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'chat_message',
            'message': content
        })

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        text_data=json.dumps(message)
    
        self.send(text_data=text_data)
    
   