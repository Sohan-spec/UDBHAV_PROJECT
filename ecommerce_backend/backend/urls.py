from . import views
from django.urls import path
urlpatterns=[
    path('',views.homepage,name='homepage'),
    path('electronics/',views.electronics,name='electronics'),
    path('household/',views.household,name='household'),
    path('clothes/',views.clothes,name='clothes'),
    path('electronics/phones/',views.phones,name='phones'),
    path('electronics/phones/apple/',views.apple,name='apple'),
    path('electronics/phones/samsung/',views.samsung,name='samsung'),
    path('electronics/laptops/',views.laptops,name='laptops'),
    path('electronics/laptops/asus/',views.asus,name='asus'),
    path('electronics/laptops/macbook/',views.macbook,name='macbook'),
    path('household/kitchen/',views.kitchenware,name='kitchenware'),
    path('household/furniture/',views.furniture,name='furniture'),
    path('clothes/tshirts/',views.tshirts,name='tshirts'),
    path('clothes/pants/',views.pants,name='pants'),
    path('household/kitchen/utensils/',views.utensils,name='utensils'),
    path('household/kitchen/groceries/',views.groceries,name='groceries'),
    path('household/furniture/sofas/',views.sofas,name='sofas'),
    path('household/furniture/beds/',views.beds,name='beds'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('profile/',views.profile,name='profile'),
    path('profile/address/',views.address,name='address'),
    path('cart/checkout/',views.checkout,name='checkout'),
    path('dashboard/',views.admin_dashboard,name='admin_dashboard'),

]