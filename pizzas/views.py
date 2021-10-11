import string
from datetime import datetime
import random

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from pizzas.models import Dish, Order, Ingredient, Dish_Item, Order_Item, User, Drink_Dessert, Drink_Dessert_Item, \
    Discount_Code, Area, Delivery_Person


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
    for delivery_person in Delivery_Person.objects.all():
        if delivery_person.can_deliver_again:
            delivery_person.status = '1'
            delivery_person.save()
    for order in Order.objects.filter(status='2'):
        couriers = get_couriers(order)
        if len(couriers) > 0 and not order.cancellable:
            order.delivery_person = couriers[0]
            order.status = '3'
            order.date_picked_up = datetime.now()
            order.delivery_person.status = '2'
            order.delivery_person.save()
            order.save()
    pizza_count = 0
    for order in Order.objects.filter(status='3'):
        if (now.replace(tzinfo=None) - order.date_created.replace(tzinfo=None)).total_seconds() > 900:
            for dish in order.dishes.all():
                pizza_count+=1
            order.status = '4'
            order.date_completed = datetime.now()
            order.save()
    if len(Discount_Code.objects.filter(user = user)) != user.pizza_count//10:
        codes = user.pizza_count//10 - len(Discount_Code.objects.filter(user=user))
        for i in range(codes):
            code = Discount_Code(user=user, string=generate_code())
            code.save()

    context = {
        'user': user,
        'orders_in_progress': Order.objects.filter(status='2'),
        'orders_cancelled': Order.objects.filter(status='5'),
        'orders_delivery': Order.objects.filter(status='3'),
        'orders_completed': Order.objects.filter(status='4'),
        'codes': Discount_Code.objects.filter(user = user, active = True)
    }
    return render(request, 'Orders.html', context)

def get_couriers(order):
    area_code = order.postal_code
    couriers = []
    for delivery_person in Delivery_Person.objects.filter(area = order.postal_code, status = '1'):
        couriers.append(delivery_person)

    for delivery_person in Delivery_Person.objects.filter(area = order.postal_code, status = '2'):
        if delivery_person.can_pick_up:
            couriers.append(delivery_person)
    return couriers

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
            postal_code = Area.objects.get(postal_code = request.POST['area_code'])
            order.postal_code = postal_code
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
        'order_id': order_id,
        'areas': Area.objects.all()

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


def dish_delete(request, cart_id, dish_id):
    cart = Order.objects.get(pk = cart_id)
    dish = Dish.objects.get(pk=dish_id)
    order_item = Order_Item.objects.filter(order = cart, dish = dish).first()
    order_item.delete()
    return redirect('menu')

def drink_dessert_delete(request, cart_id, drink_dessert_id):
    cart = Order.objects.get(pk = cart_id)
    drink_dessert = Drink_Dessert.objects.get(pk=drink_dessert_id)
    drink_dessert_item = Drink_Dessert_Item.objects.filter(order = cart, drink_dessert = drink_dessert).first()
    drink_dessert_item.delete()
    return redirect('menu')

def generate_code():
    letters = string.ascii_lowercase
    str = ''
    for i in range(0,6):
        str += letters[random.randint(0,len(letters)-1)]
    return str
