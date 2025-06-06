# Generated by Django 5.1.1 on 2024-11-15 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0015_reservation_region_alter_facture_montant_facture'),
    ]

    operations = [
        migrations.AddField(
            model_name='voiture',
            name='climatisation',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='voiture',
            name='nombre_siege',
            field=models.PositiveIntegerField(default=5),
        ),
    ]
