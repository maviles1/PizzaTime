"""pizzaTime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pizzas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', views.menu, name= 'menu'),
    path('menu/<int:dish_id>/', views.dish, name= 'dish'),
    path('order/<int:order_id>', views.cart,name = 'order'),
    path('menu/<int:dish_id>/extras', views.extras,name = 'extras'),
    path('', views.home, name = 'home'),
    path('orders', views.my_orders, name = 'orders'),
    path('order/cancel/<int:order_id>', views.cancel_order, name = 'order_cancel'),
    path('confirmation/<int:order_id>', views.confirmation, name = 'confirmation'),
    path('finalize/<int:order_id>', views.finalize, name = 'finalize'),
    path('drink_dessert/<int:drink_dessert_id>', views.drink_dessert, name = 'drink_dessert'),
    path('cart/delete/<int:cart_id>/<int:dish_id>', views.dish_delete, name = 'dish_delete'),
    path('cart/delete/drink/<int:cart_id>/<int:drink_dessert_id>', views.drink_dessert_delete, name = 'drink_dessert_delete'),
    path('discounts/', views.discounts, name= 'discounts')
]
