# views.py

from rest_framework.response import Response
from authentication.models import Message ,User
from authentication.serializers import MessageSerializer,UserSerializer 
from rest_framework.decorators import api_view
from django.db.models import Q

@api_view(['GET'])
def conversation_history(request, sender_id, receiver_id):
    # Fetch conversation history from the database
    messages = Message.objects.filter(
        sender=sender_id, recipient=receiver_id
    ) | Message.objects.filter(
        sender=receiver_id, recipient=sender_id
    )

    # Serialize the messages
    serialized_messages = MessageSerializer(messages, many=True)

    return Response(serialized_messages.data)




@api_view(['GET'])
def conversation_users_history(request, senderId):
    # Fetch conversation history from the database
    messages = Message.objects.filter(
        Q(sender=senderId) | Q(recipient=senderId)
    ).distinct()  # Ensuring distinct users

    # Get unique recipient IDs excluding the current user
    sender = set()
    for message in messages:
        if message.sender_id != senderId:
            sender.add(message.sender_id)
        if message.recipient_id != senderId:
            sender.add(message.recipient_id)

    # Fetch User instances corresponding to recipient IDs
    users = User.objects.filter(pk__in=sender)

    # Serialize the user instances
    serializer = UserSerializer(users, many=True)  # Assuming you have a UserSerializer
    return Response(serializer.data)
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.db.models import Q
# from authentication.models import Message, User
# from  authentication.serializers import MessageSerializer, UserSerializer

# @api_view(['GET'])
# def conversation_history(request, sender_id, receiver_id):
#     messages = Message.objects.filter(
#         (Q(sender=sender_id) & Q(recipient=receiver_id)) | 
#         (Q(sender=receiver_id) & Q(recipient=sender_id))
#     )
#     serialized_messages = MessageSerializer(messages, many=True)
#     return Response(serialized_messages.data)

# @api_view(['GET'])
# def conversation_users_history(request, senderId):
#     messages = Message.objects.filter(
#         Q(sender=senderId) | Q(recipient=senderId)
#     ).distinct()
#     sender = set()
#     for message in messages:
#         if message.sender_id != senderId:
#             sender.add(message.sender_id)
#         if message.recipient_id != senderId:
#             sender.add(message.recipient_id)
#     users = User.objects.filter(pk__in=sender)
#     serializer = UserSerializer(users, many=True)
    
#     conversation_ids = Message.objects.filter(
#         Q(sender=senderId) | Q(recipient=senderId)
#     ).values_list('conversation_id', flat=True).distinct()
    
#     return Response({
#         'users': serializer.data,
#         'conversation_ids': list(conversation_ids)
#     })
