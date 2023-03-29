from rest_framework.serializers import ModelSerializer

from backend.apps.chatgpt.models import ChatBox, ChatMessage


class ChatBoxSerialzier(ModelSerializer):
    class Meta:
        model = ChatBox
        fields = ['id', 'detail', 'created_time']


class ChatMessageSerialzier(ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'message', 'chatbox', 'created_time', 'response']
