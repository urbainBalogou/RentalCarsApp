# Generated by Django 4.1.7 on 2023-05-25 02:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0007_alter_client_adresse_alter_client_numero_tel_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
