# Generated by Django 5.0.4 on 2024-04-24 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionanswer',
            name='short_question',
            field=models.TextField(default='nope', verbose_name='Short Question'),
            preserve_default=False,
        ),
    ]
