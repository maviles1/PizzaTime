from django.db import models

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Pizza(models.Model):
    pizza_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

class Ingredient(models.Model):
    ingredient_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)


class Pizza_Item(models.Model):
    pizza_item_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)

class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Order_Item(models.Model):
    order_item_id = models.IntegerField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)