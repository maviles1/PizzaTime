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
    path('menu/<int:dish_id>/add', views.add, name= 'add'),
    path('order/<int:order_id>', views.order,name = 'order')

]
