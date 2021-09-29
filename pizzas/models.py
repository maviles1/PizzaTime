from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Delivery_Person(models.Model):
    country_code = models.IntegerField()

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

class Dish(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_person = models.ForeignKey(Delivery_Person, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    dishes = models.ManyToManyField(Dish)

class Dish_Item(models.Model):
    description = models.CharField(max_length=100)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    food = models.ForeignKey(Dish, on_delete=models.CASCADE)


class Order_Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Dish, on_delete=models.CASCADE)

