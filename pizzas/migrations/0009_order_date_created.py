# Generated by Django 3.2.7 on 2021-10-04 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0008_delivery_person_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_created',
            field=models.DateTimeField(null=True),
        ),
    ]
