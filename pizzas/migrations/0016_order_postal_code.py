# Generated by Django 3.2.7 on 2021-10-11 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0015_auto_20211007_0009'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='pizzas.area'),
        ),
    ]
