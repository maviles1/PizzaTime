# Generated by Django 3.2.7 on 2021-10-11 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0018_auto_20211011_0758'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_completed',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
