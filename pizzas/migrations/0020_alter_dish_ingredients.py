# Generated by Django 3.2.7 on 2021-10-11 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0019_order_date_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='ingredients',
            field=models.ManyToManyField(to='pizzas.Ingredient'),
        ),
    ]