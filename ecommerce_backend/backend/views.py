from django.shortcuts import render, redirect
from django.http import HttpResponse

def admin_required_session(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return HttpResponse('Unauthorized: Admin access required', status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped

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

@admin_required_session
def admin_dashboard(request):
    # Protected route placeholder
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

def checkout(request):
    return render(request,"checkout.html")