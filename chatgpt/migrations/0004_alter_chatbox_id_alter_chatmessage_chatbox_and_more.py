# Generated by Django 4.1.7 on 2023-03-25 14:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chatgpt', '0003_alter_chatbox_id_alter_chatmessage_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatbox',
            name='id',
            field=models.UUIDField(default=uuid.UUID('e7baa3c3-678c-4afa-9686-b8c140bb0e58'), primary_key=True, serialize=False, verbose_name='主键id'),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='chatbox',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatgpt.chatbox', verbose_name='box_id'),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='id',
            field=models.UUIDField(default=uuid.UUID('e7baa3c3-678c-4afa-9686-b8c140bb0e58'), primary_key=True, serialize=False, verbose_name='主键id'),
        ),
    ]
