# Generated by Django 3.2.7 on 2021-10-04 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0010_alter_order_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drink_Dessert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('type', models.CharField(choices=[('1', 'drink'), ('2', 'dessert')], default='1', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Drink_Dessert_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('drink_dessert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizzas.drink_dessert')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizzas.order')),
            ],
        ),
    ]
