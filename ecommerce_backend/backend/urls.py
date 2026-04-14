from . import views
from . import api
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
    path('cart/',views.cart,name='cart'),
    path('cart/checkout/',views.checkout,name='checkout'),
    path('dashboard/',views.admin_dashboard,name='admin_dashboard'),
    
    # API Routes (BE-1, BE-2)
    path('api/register/', api.register, name='api_register'),
    path('api/login/', api.login, name='api_login'),
    path('api/products/', api.get_products, name='api_products'),
    path('api/cart/', api.manage_cart, name='api_cart'),
    path('api/orders/', api.list_orders, name='api_orders'),
    path('api/orders/create/', api.create_order, name='api_create_order'),
    path('api/admin/stats/', api.admin_only_stats, name='api_admin_stats'),
    path("api/products/create/", api.create_product,name="api_create_product"),
]