import openai

from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from YourAi.settings import OPENAI_KEY
from backend.apps.chatgpt.models import ChatMessage, ChatBox
from backend.apps.chatgpt.serializers import ChatBoxSerialzier, ChatMessageSerialzier
from backend.common.chatgpt import ask_gpt

openai.api_key = OPENAI_KEY


class ChatBoxView(ModelViewSet):
    queryset = ChatBox.objects.all()
    serializer_class = ChatBoxSerialzier
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_time']


class ChatMessageView(ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerialzier
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_time']

    def get_queryset(self):
        return ChatMessage.objects.filter(chatbox=self.kwargs['pk'])

    def create(self, request, *args, **kwargs):
        conversation = []
        # 将发送信息储存到数据库
        message = {"role": "user", "content": request.data.get('message')}
        chat_record = ChatMessage.objects.create(
            chatbox=ChatBox.objects.filter(id=request.data.get('id')).first(),
            message=message
        )
        # 获取先前的对话信息
        prev_message = ChatMessage.objects.filter(chatbox=self.kwargs['pk']).order_by('created_time')
        for i in prev_message:
            conversation.append(i.message)
        # 获取回答，并存入之前创建的提问消息
        answer = ask_gpt(conversation)
        chat_record.response = answer
        chat_record.save()

        return Response(data=answer)
