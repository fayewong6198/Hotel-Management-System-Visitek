# Generated by Django 3.0.5 on 2020-04-21 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='security_question',
        ),
        migrations.RemoveField(
            model_name='user',
            name='serurity_answer',
        ),
    ]
