import uuid
from django.db import models
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel


class BaseModel(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id = models.UUIDField(default=uuid.uuid4,primary_key=True, verbose_name="主键id")
    created_time = models.DateTimeField(auto_created=True, auto_now_add=True, null=False, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_created=False, auto_now=True, null=True, verbose_name='更新时间')

    class Meta:
        abstract = True