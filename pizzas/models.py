import math
from datetime import datetime



from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, name, password, area_code, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') == False:
            raise ValueError('s')
        if other_fields.get('is_superuser') == False:
            raise ValueError('s')
        return self.create_user(email, name, password, area_code, **other_fields)

    def create_user(self, email, name, password, area_code,**other_fields):
        if not email:
            raise ValueError(_("please provide an email"))
        email = self.normalize_email(email)
        user = self.model(email = email, name = name, area_code = area_code,**other_fields)
        user.set_password(password)
        user.save()
        return user

    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    area_code = models.CharField(max_length=100, default='1')
    types = [('1', 'customer'),('2', 'employee'), ('3', 'delivery person')]
    type =models.CharField(max_length=100,choices=types, default='1')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'area_code']
    objects = CustomAccountManager()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    @property
    def pizza_count(self):
        count = 0
        orders = Order.objects.filter(user = self, status = '4')
        for order in orders:
            count += len(order.dishes.all())
        return count

    @property
    def pizzas_left(self):
        pizza_count = self.pizza_count%10
        if 10-pizza_count < 0:
            return 0
        return 10-pizza_count

    @property
    def eligible_for_discount(self):
        if self.pizzas_left == 0:
            return True
        return False


class Area(models.Model):
    postal_code = models.IntegerField()

class Delivery_Person(models.Model):
    name = models.CharField(max_length=100, null = True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null = True)
    status_choices = [('1', 'no orders'),('2', 'delivering')]
    status = models.CharField(max_length=100, choices = status_choices, default='1')

    @property
    def get_orders(self):
        return Order.objects.filter(delivery_person = self)

    @property
    def can_pick_up(self):
        orders = Order.objects.filter(delivery_person = self, status = '3')
        preparing_orders = Order.objects.filter(postal_code = self.area, status = '2')
        for order in orders:
            for preparing_order in preparing_orders:
                if (preparing_order.date_created.replace(tzinfo=None) - order.date_created.replace(tzinfo=None)).total_seconds() < 60:
                    return True
        return False

    def can_pick_up_order(self, order_to_check):
        orders = Order.objects.filter(delivery_person = self, status = '3')
        for order in orders:
            if (order_to_check.date_created.replace(tzinfo=None) - order.date_created.replace(tzinfo=None)).total_seconds() < 60:
                return True
        return False


    @property
    def can_deliver_again(self):
        orders = Order.objects.filter(delivery_person = self, status = '4')
        if len(Order.objects.filter(delivery_person = self, status = '3')) != 0:
            return False
        for order in orders:
            if (datetime.now().replace(tzinfo=None) - order.date_created.replace(tzinfo=None)).total_seconds() < 1800:
                return False
        return True

    def __str__(self):
        return self.name


    @property
    def get_active_orders(self):
        return Order.objects.filter(delivery_person=self, status = '3')

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    vegetarian = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient, through='Dish_Item', through_fields=('dish', 'ingredient'))

    @property
    def price(self):
        total = 0
        for ingredient in self.ingredients.all():
            total += ingredient.price*(Dish_Item.objects.filter(dish = self, ingredient = ingredient)).first().quantity
        return round(total*1.4,2)

    @property
    def ingredients_str(self):
        str = ''
        for ingredient in self.ingredients.all():
            str += ingredient.name + ', '
        return str[0:len(str)-2]

    @property
    def vegetarian(self):
        for ingredient in self.ingredients.all():
            if not ingredient.vegetarian:
                return False
        return True
    def __str__(self):
        return self.name

class Drink_Dessert(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    types = [('1','drink'), ('2', 'dessert')]
    type = models.CharField(max_length=100, choices=types, default='1')
    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status_choices = [('1','incomplete'),('2','in preparation'), ('3','on the way'), ('4','completed'), ('5','cancelled')]
    delivery_person = models.ForeignKey(Delivery_Person, on_delete=models.CASCADE, null =True, blank=True)
    status = models.CharField(max_length=100,choices=status_choices,default='1')
    dishes = models.ManyToManyField(Dish, through='Order_Item', through_fields=('order', 'dish'))
    drinks_desserts = models.ManyToManyField(Drink_Dessert, through='Drink_Dessert_Item', through_fields=('order', 'drink_dessert'))
    date_created = models.DateTimeField(null = True, default= None)
    postal_code = models.ForeignKey(Area, default=None, null=True, on_delete=models.CASCADE)
    date_picked_up = models.DateTimeField(null=True, default=None, blank=True)
    date_completed = models.DateTimeField(null=True, default=None, blank=True)
    address = models.CharField(max_length=100,null=True, default=None, blank=True)
    phone = models.CharField(max_length=100,null=True, default=None, blank=True)
    @property
    def vat(self):
        return round(0.09*self.price,2)

    @property
    def total(self):
        total = self.price
        if self.discounted:
            total = total*0.9
        return round(total + self.vat, 2)

    @property
    def discount(self):
        return round(0.1*self.price,2)

    @property
    def price(self):
        total = 0
        for dish in self.dishes.all():
            total += dish.price
        for drink_dessert in self.drinks_desserts.all():
            total += drink_dessert.price
        return round(total,2)

    @property
    def discounted(self):
        if len(Discount_Code.objects.filter(order=self)) > 0:
            return True
        return False

    @property
    def valid(self):
        return len(self.dishes.all()) != 0

    @property
    def cancellable(self):
        now = datetime.now()
        return (now.replace(tzinfo=None) - self.date_created.replace(tzinfo=None)).total_seconds() < 300

    @property
    def eta(self):
        now = datetime.now()
        15 - (now.replace(tzinfo=None) - self.date_created.replace(tzinfo=None)).total_seconds() / 60

        string = str(math.trunc(15 - (now.replace(tzinfo=None) - self.date_created.replace(tzinfo=None)).total_seconds() // 60))
        string += ":"
        string += str(60 -(math.trunc(((now.replace(tzinfo=None) - self.date_created.replace(tzinfo=None)).total_seconds()) % 60)))

        return string


class Order_Item(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    extras = models.ManyToManyField(Ingredient, through='Extra', through_fields=('order_item', 'ingredient'))

class Dish_Item(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.ingredient.name + " | " + self.dish.name

class Extra(models.Model):
    order_item = models.ForeignKey(Order_Item, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Drink_Dessert_Item(models.Model):
    drink_dessert = models.ForeignKey(Drink_Dessert, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Discount_Code(models.Model):
    string = models.CharField(max_length=6)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)