# Generated by Django 5.0.4 on 2024-04-25 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_chat', '0003_answersfile_delete_questionanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answersfile',
            name='addition_date',
            field=models.DateTimeField(verbose_name='datetime'),
        ),
    ]
