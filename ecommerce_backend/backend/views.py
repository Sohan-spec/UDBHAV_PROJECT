from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def homepage(request):
    return render(request,'homepage.html')

def login(request):
    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')

def profile(request):
    return render(request,'Profile.html')

def address(request):
    return render(request,'address.html')

def checkout(request):
    return render(request,'checkout.html')

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

def cart(request):
    return render(request,'cart.html')

def clothes(request):
    return render(request,'clothes.html')

def electronics(request):
    return render(request,'electronics.html')

def household(request):
    return render(request,'household.html')

def phones(request):
    return render(request,'phones.html')

def apple(request):
    return render(request,'apple.html')

def samsung(request):
    return render(request,'samsung.html')

def laptops(request):
    return render(request,'laptops.html')

def asus(request):
    return render(request,'asus.html')

def macbook(request):
    return render(request,'macbook.html')

def kitchenware(request):
    return render(request,'kitchen.html')

def furniture(request):
    return render(request,'furniture.html')

def tshirts(request):
    return render(request,'tshirts.html')

def pants(request):
    return render(request,'pants.html')

def utensils(request):
    return render(request,'utensils.html')

def groceries(request):
    return render(request,'grocery.html')

def sofas(request):
    return render(request,'sofas.html')

def beds(request):
    return render(request,'beds.html')