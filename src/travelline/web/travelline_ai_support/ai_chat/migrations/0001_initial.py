# Generated by Django 5.0.4 on 2024-04-24 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(verbose_name='Question')),
                ('answer', models.TextField(verbose_name='Answer')),
                ('addition_date', models.DateTimeField(verbose_name='Date Time answer was added')),
                ('relevance', models.IntegerField(verbose_name='Relevance')),
            ],
        ),
    ]
