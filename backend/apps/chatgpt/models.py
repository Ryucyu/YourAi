from django.db import models

# Create your models here.
from backend.common.base_models import BaseModel


class ChatBox(BaseModel):
    detail = models.CharField(max_length=16, null=True, verbose_name='对话细节')


class ChatMessage(BaseModel):
    response = models.TextField(max_length=1024, null=True, verbose_name='响应文本')
    message = models.JSONField(max_length=1024, null=True, verbose_name='对话文本')
    chatbox = models.ForeignKey(ChatBox, on_delete=models.CASCADE, db_constraint=False, verbose_name="box_id")







