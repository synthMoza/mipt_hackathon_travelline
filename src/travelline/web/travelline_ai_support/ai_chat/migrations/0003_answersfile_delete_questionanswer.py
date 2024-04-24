# Generated by Django 5.0.4 on 2024-04-24 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_chat', '0002_questionanswer_short_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswersFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.TextField(verbose_name='filename')),
                ('content', models.TextField(verbose_name='content')),
                ('addition_date', models.DateTimeField(verbose_name='DateTime')),
            ],
        ),
        migrations.DeleteModel(
            name='QuestionAnswer',
        ),
    ]
