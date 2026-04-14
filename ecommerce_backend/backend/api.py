import json
import jwt
import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.db.models import Q
from .models import User, Category, Product, Cart, CartItem, Order, OrderItem, Review

# Helper function
def get_user_from_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return User.objects.filter(id=payload['user_id']).first()
    except:
        return None

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = get_user_from_token(request)
        if not user or user.role != 'admin':
            return JsonResponse({'error': 'Admin privileges required'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def user_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = get_user_from_token(request)
        if not user:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        request.user = user  # Inject
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'user')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username exists'}, status=400)
        
        user = User(username=username, role=role)
        user.set_password(password)
        user.save()
        # Create empty cart for user
        Cart.objects.create(user=user)
        return JsonResponse({'message': 'User registered successfully'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            payload = {
                'user_id': user.id,
                'role': user.role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            return JsonResponse({'token': token, 'role': user.role})
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_products(request):
    # Pagination & Search optimization (BE-3)
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 10))
    search = request.GET.get('search', '')
    
    query = Product.objects.select_related('category') # DB optimization
    if search:
        query = query.filter(name__icontains=search)
    
    total = query.count()
    start = (page - 1) * size
    products = query[start:start+size]
    
    data = []
    for p in products:
        data.append({
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'stock': p.stock,
            'category': p.category.name if p.category else ''
        })
    return JsonResponse({'products': data, 'total': total, 'page': page})

@csrf_exempt
@user_required
def manage_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    if request.method == 'GET':
        items = cart.items.select_related('product').all()
        # Fast lookup via dict (BE-3 performance constraint)
        items_dist = {item.product.id: {'qty': item.quantity, 'name': item.product.name, 'price': float(item.product.price)} for item in items}
        
        data = [{'product_id': pid, **info} for pid, info in items_dist.items()]
        total = sum(i['qty'] * i['price'] for i in items_dist.values())
        return JsonResponse({'items': data, 'total': total})
        
    elif request.method == 'POST':
        data = json.loads(request.body)
        pid = data.get('product_id')
        qty = data.get('quantity', 1)
        
        product = Product.objects.filter(id=pid).first()
        if not product:
            return JsonResponse({'error': 'Product not found'}, status=404)
            
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += qty
        else:
            item.quantity = qty
        item.save()
        return JsonResponse({'message': 'Item added to cart'})
        
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        pid = data.get('product_id')
        CartItem.objects.filter(cart=cart, product_id=pid).delete()
        return JsonResponse({'message': 'Item removed'})

@csrf_exempt
@user_required
def create_order(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return JsonResponse({'error': 'Cart is empty'}, status=400)
            
        total = 0
        order = Order.objects.create(user=request.user, total_price=0)
        
        items_to_create = []
        for item in cart.items.select_related('product'):
            price = item.product.price
            items_to_create.append(OrderItem(
                order=order, product=item.product, price=price, quantity=item.quantity
            ))
            total += price * item.quantity
            item.product.stock -= item.quantity
            item.product.save()
            
        OrderItem.objects.bulk_create(items_to_create) # optimization BE-3
        order.total_price = total
        order.save()
        
        cart.items.all().delete() # clear cart
        return JsonResponse({'message': 'Order placed successfully', 'order_id': order.id})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@user_required
def list_orders(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
        data = []
        for o in orders:
            data.append({
                'id': o.id,
                'total': float(o.total_price),
                'status': o.status,
                'date': str(o.created_at),
                'items': [{'name': i.product.name, 'qty': i.quantity} for i in o.items.all()]
            })
        return JsonResponse({'orders': data})

@csrf_exempt
@admin_required
def admin_only_stats(request):
    if request.method == 'GET':
        return JsonResponse({'orders_count': Order.objects.count(), 'users_count': User.objects.count()})

@csrf_exempt
@admin_required
def create_product(request):
    if request.method == "POST":
        data = json.loads(request.body)

        name = data.get("name")
        price = data.get("price")
        stock = data.get("stock", 0)

        if not name or not price:
            return JsonResponse({"error": "Name and price required"}, status=400)

        product = Product.objects.create(
            name=name,
            price=price,
            stock=stock
        )

        return JsonResponse({
            "message": "Product created",
            "id": product.id
        })

    return JsonResponse({"error": "Method not allowed"}, status=405)