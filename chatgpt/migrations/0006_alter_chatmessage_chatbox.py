# Generated by Django 4.1.7 on 2023-03-25 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chatgpt', '0005_alter_chatbox_id_alter_chatmessage_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='chatbox',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='chatgpt.chatbox', verbose_name='box_id'),
        ),
    ]
