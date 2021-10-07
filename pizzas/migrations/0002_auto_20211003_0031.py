# Generated by Django 3.2.7 on 2021-10-03 00:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish_item',
            name='description',
        ),
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.IntegerField()),
                ('Ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizzas.ingredient')),
                ('Order_Item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizzas.order_item')),
            ],
        ),
    ]