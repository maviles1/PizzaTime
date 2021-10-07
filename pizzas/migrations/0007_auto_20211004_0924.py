# Generated by Django 3.2.7 on 2021-10-04 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0006_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postal_code', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='delivery_person',
            name='country_code',
        ),
        migrations.AddField(
            model_name='delivery_person',
            name='status',
            field=models.CharField(choices=[('1', 'no orders'), ('2', 'delivering')], default='1', max_length=100),
        ),
        migrations.AddField(
            model_name='delivery_person',
            name='area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pizzas.area'),
        ),
    ]
