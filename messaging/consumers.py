from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
from authentication.models import Message, User, Clients
import json

# Global variable to store connected clients
connected_clients = {}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        
        await self.add_client_channel(self.sender_id, self.channel_name)

        await self.accept()
        print(f"Connected: sender_id={self.sender_id}, receiver_id={self.receiver_id}")

    async def disconnect(self, close_code):
        await self.remove_client_channel(self.channel_name)
        print(f"Disconnected: sender_id={self.sender_id}, receiver_id={self.receiver_id}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        print(f"Received message: {data}")

        handlers = {
            'chat_message': self.handle_chat_message,
            'offer': self.handle_offer,
            'answer': self.handle_answer,
            'ice_candidate': self.handle_ice_candidate,
            'call_ended': self.handle_call_ended,
        }

        if message_type in handlers:
            await handlers[message_type](data)
        else:
            print(f"Unknown message type: {message_type}")

    async def handle_chat_message(self, data):
        message = data['message']
        print(f"Handling chat message: {message}")
        await self.save_message(message)

        receiver_channel_name = await self.get_channel_name(self.receiver_id)
        if receiver_channel_name:
            await self.channel_layer.send(
                receiver_channel_name,
                {
                    "type": "chat.message",
                    "message": message,
                    "sender_id": self.sender_id,
                    "receiver_id": self.receiver_id
                }
            )

    async def handle_offer(self, data):
        global connected_clients
        receiver_channel_name = await self.get_channel_name(self.receiver_id)
        connected_clients[self.receiver_id] = data['sender_id']
        if receiver_channel_name:
            await self.channel_layer.send(
                receiver_channel_name,
                {
                    "type": "webrtc.offer",
                    "offer": data['offer'],
                    "callType": data.get('callType'),
                    "sender_id": self.sender_id,
                }
            )
        print(f'Offer handled: sender_id={self.sender_id}, receiver_id={self.receiver_id}')

    async def handle_answer(self, data):
        global connected_clients
        sender_id = connected_clients.get(self.sender_id)
        if sender_id:
            receiver_channel_name = await self.get_channel_name(sender_id)
            if receiver_channel_name:
                await self.channel_layer.send(
                    receiver_channel_name,
                    {
                        "type": "webrtc.answer",
                        "answer": data['answer'],
                        "sender_id": self.sender_id,
                    }
                )
            print(f'Answer handled: sender_id={self.sender_id}, receiver_id={sender_id}')
        else:
            print(f'No sender found for receiver_id={self.sender_id}')

    async def handle_ice_candidate(self, data):
        print(f"Handling ICE candidate: {data}")
        global connected_clients
        receiver_channel_name = await self.get_channel_name(self.receiver_id)
        connected_clients[self.receiver_id] = data['sender_id']
        if receiver_channel_name:
            await self.channel_layer.send(
                receiver_channel_name,
                {
                    "type": "webrtc.ice_candidate",
                    "candidate": data['candidate'],
                    "sender_id": self.sender_id,
                }
            )

    async def handle_call_ended(self, data):
        global connected_clients
        receiver_id = connected_clients.get(self.sender_id)
        if receiver_id:
            receiver_channel_name = await self.get_channel_name(receiver_id)
            if receiver_channel_name:
                await self.channel_layer.send(
                    receiver_channel_name,
                    {
                        "type": "webrtc.call_ended",
                        "sender_id": self.sender_id,
                    }
                )
            del connected_clients[self.sender_id]  # Remove the connection
        else:
            print(f"No active call found for sender_id={self.sender_id}")

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        receiver_id = event['receiver_id']
        print(f"Sending chat message: {message}, sender_id: {sender_id}")
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'sender_id': sender_id,
            'receiver_id': receiver_id
        }))

    async def webrtc_offer(self, event):
        print(f"Sending WebRTC offer: {event}")
        await self.send(text_data=json.dumps({
            'type': 'offer',
            'offer': event['offer'],
            'callType': event.get('callType'),
            'sender_id': event['sender_id'],
        }))

    async def webrtc_answer(self, event):
        print(f"Sending WebRTC answer: {event}")
        await self.send(text_data=json.dumps({
            'type': 'answer',
            'answer': event['answer'],
            'sender_id': event['sender_id'],
        }))

    async def webrtc_ice_candidate(self, event):
        print(f"Sending WebRTC ICE candidate: {event}")
        await self.send(text_data=json.dumps({
            'type': 'ice_candidate',
            'candidate': event['candidate'],
            'sender_id': event['sender_id'],
        }))

    async def webrtc_call_ended(self, event):
        print(f"Sending WebRTC call ended: {event}")
        await self.send(text_data=json.dumps({
            'type': 'call_ended',
            'sender_id': event['sender_id'],
        }))

    @sync_to_async
    def save_message(self, message):
        try:
            sender = User.objects.get(id=self.sender_id)
            recipient = User.objects.get(id=self.receiver_id)
            Message.objects.create(sender=sender, recipient=recipient, content=message)
        except User.DoesNotExist as e:
            print(f"Error saving message: {e}")

    @sync_to_async
    def get_channel_name(self, user_id):
        try:
            client = Clients.objects.filter(user_id=user_id).first()
            return client.channel_name if client else None
        except Clients.DoesNotExist:
            return None

    @sync_to_async
    def add_client_channel(self, user_id, channel_name):
        if Clients.objects.filter(user_id=user_id).exists():
            return 
        else:
            Clients.objects.create(user_id=user_id, channel_name=channel_name)

    @sync_to_async
    def remove_client_channel(self, channel_name):
        Clients.objects.filter(channel_name=channel_name).delete()