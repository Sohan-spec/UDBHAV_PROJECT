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
]