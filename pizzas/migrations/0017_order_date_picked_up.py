# Generated by Django 3.2.7 on 2021-10-11 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0016_order_postal_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_picked_up',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]