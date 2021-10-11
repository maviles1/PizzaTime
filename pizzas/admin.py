from django.contrib import admin
from .models import User, Ingredient, Dish, Delivery_Person, Order, Order_Item, Dish_Item, Extra, Area, Drink_Dessert, \
    Drink_Dessert_Item, Discount_Code

# Register your models here.
admin.site.register(User)
admin.site.register(Ingredient)
admin.site.register(Dish)
admin.site.register(Order)
admin.site.register(Order_Item)
admin.site.register(Dish_Item)
admin.site.register(Extra)
admin.site.register(Delivery_Person)
admin.site.register(Area)
admin.site.register(Drink_Dessert)
admin.site.register(Drink_Dessert_Item)
admin.site.register(Discount_Code)