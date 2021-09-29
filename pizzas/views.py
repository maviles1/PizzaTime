from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from pizzas.models import Dish, Order, Ingredient


def menu(request):
    dishes = Dish.objects.all()
    return HttpResponse(dishes.size())


def test(request):
    if request.method == "POST":
        pass
    pass

def dish(request, dish_id):
    Ingredient(name = "").save()
    return HttpResponse(Dish.objects.get(pk = dish_id))

def add(request):
    current_user = request.user
    order = Order.objects.get(user = current_user)

def order(request, order_id):
    current_user = request.user
    order = Order.objects.get(pk = order_id)

def food(request):
    pass
