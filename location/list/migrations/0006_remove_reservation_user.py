# Generated by Django 4.2 on 2023-05-22 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0005_reservation_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='user',
        ),
    ]
