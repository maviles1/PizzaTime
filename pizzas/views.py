import string
from datetime import datetime
import random

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from pizzas.models import Dish, Order, Ingredient, Dish_Item, Order_Item, User, Drink_Dessert, Drink_Dessert_Item, \
    Discount_Code


def menu(request):
    context = {
        'dishes': Dish.objects.all(),
        'cart': active_order(Order.objects.filter(user=request.user), request.user),
        'drinks': Drink_Dessert.objects.filter(type='1'),
        'desserts': Drink_Dessert.objects.filter(type='2'),
        'order_id': active_order(Order.objects.filter(user=request.user), request.user).id
    }
    ingredients = Ingredient.objects.all()
    counter = 1
    return render(request, 'Menu.html', context)


def dish(request, dish_id):
    if request.method == 'GET':
        context = {
            'dish': Dish.objects.get(pk=dish_id),
            'ingredients': Dish.objects.get(pk=dish_id).ingredients.all,
            'all_ingredients': Ingredient.objects.all,
        }
        return render(request, 'Dish.html', context)
    if request.method == 'POST':
        current_user = request.user
        orders = Order.objects.filter(user=current_user)
        order = active_order(orders, current_user)
        # extra = Ingredient.objects.get(pk=int(request.POST.get('extra', None)))
        order_item = Order_Item(dish=Dish.objects.get(pk=dish_id), order=order)
        order_item.save()
        # order_item.extras.add(extra)

        # order.dishes.add(Dish.objects.get(pk = dish_id))
        # order_items = Order_Item.objects.filter(order = order, dish = Dish.objects.get(pk = dish_id))
        #
        # if len(order_items) != 0:
        #     order_item = Order_Item.objects.get(order = order, dish = Dish.objects.get(pk = dish_id))
        #     order_item.quantity += 1;
        #     order_item.extras.add(extra)
        #     order_item.save()
        return redirect('menu')


def cart(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(pk=order_id)
        order_items = Order_Item.objects.filter(order=order)
        order.status = str(int(order.status) + 1)
        order.date_created = datetime.now()
        order.save()
        return redirect('menu')
    if request.method == 'GET':
        order = Order.objects.get(pk=order_id)
        order_items = Order_Item.objects.filter(order=order)
        context = {
            'items': order_items,
            'order_id': order_id
        }
        return render(request, 'Cart.html', context)


def my_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    now = datetime.now()
    for order in Order.objects.filter(status='2'):
        if (now.replace(tzinfo=None) - order.date_created.replace(tzinfo=None)).total_seconds() > 300:
            order.status = '3'
            order.save()
    if user.eligible_for_discount:
        code = Discount_Code(user=user, string = generate_code())
        code.save()

    context = {
        'user': user,
        'orders_in_progress': Order.objects.filter(status='2'),
        'orders_cancelled': Order.objects.filter(status='5'),
        'orders_delivery': Order.objects.filter(status='3'),
        'codes': Discount_Code.objects.filter(user = user, active = True)
    }
    return render(request, 'Orders.html', context)


def cancel_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.status = '5'
    order.save()
    return redirect('orders')


def extras(request, dish_id):
    context = {

    }
    return render(request, 'Extra.html', context)


def active_order(orders, current_user):
    for order in orders:
        if order.status == '1':
            return order
    o = Order(user=current_user)
    o.save()
    return o


def home(request):
    context = {'form': UserCreationForm()}
    return render(request, 'Home.html', context)


def confirmation(request, order_id):
    if request.method == 'POST':
        if is_valid(request.POST['code']) or not request.POST['code']:
            order = Order.objects.get(pk=order_id)
            if request.POST['code'] != '':
                code = get_code(request.POST['code'])
                code.order = order
                code.active = False
                code.save()
            order_items = Order_Item.objects.filter(order=order)
            order.status = str(int(order.status) + 1)
            order.date_created = datetime.now()
            order.save()
            context = {'order_id': order_id,
                       'order': Order.objects.get(pk=order_id)}
            return render(request, 'Confirmation.html', context)
        return redirect('finalize', order_id=order_id)
    if request.method == 'GET':
        return redirect('orders')


def drink_dessert(request, drink_dessert_id):
    if request.method == 'POST':
        current_user = request.user
        orders = Order.objects.filter(user=current_user)
        order = active_order(orders, current_user)
        # extra = Ingredient.objects.get(pk=int(request.POST.get('extra', None)))
        drink_dessert_item = Drink_Dessert_Item(drink_dessert=Drink_Dessert.objects.get(pk=drink_dessert_id),
                                                order=order)
        drink_dessert_item.save()
        return redirect('menu')


def finalize(request, order_id):
    if not Order.objects.get(pk=order_id).valid:
        return redirect('menu')
    context = {
        'order_id': order_id
    }
    return render(request, 'Finalize.html', context)


def is_valid(code_str):
    codes = Discount_Code.objects.filter(string=code_str)
    for code in codes:
        if code.string == code_str and code.active:
            return True
    return False


def get_code(code_str):
    codes = Discount_Code.objects.filter(string=code_str)
    for code in codes:
        if code.string == code_str and code.active:
            return code


def generate_code():
    letters = string.ascii_lowercase
    str = ''
    for i in range(0,6):
        str += letters[random.randint(0,len(letters)-1)]
    return str
