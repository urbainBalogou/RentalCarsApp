# Generated by Django 4.2 on 2023-05-21 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0003_remove_order_car_remove_order_reserve_order_car_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='car',
        ),
        migrations.RemoveField(
            model_name='order',
            name='reserve',
        ),
        migrations.AddField(
            model_name='order',
            name='car',
            field=models.ManyToManyField(to='list.voiture'),
        ),
        migrations.AddField(
            model_name='order',
            name='reserve',
            field=models.ManyToManyField(to='list.reservation'),
        ),
    ]
