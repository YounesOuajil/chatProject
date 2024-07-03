from django.urls import re_path,path
from .consumers import ChatConsumer

websocket_urlpatterns = [

    re_path(r"^ws/chat/(?P<sender_id>\w+)/(?P<receiver_id>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r'ws/user/(?P<user_id>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<sender_id>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<userId>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<sender_id>\w+)/(?P<receiver_id>\w+)/(?P<room_id>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<sender_id>\w+)/(?P<receiver_id>\w+)/(?P<session_id>\w+)/$', ChatConsumer.as_asgi()),


]   

# U7F95AK3NUR49X5YL315FF1T
