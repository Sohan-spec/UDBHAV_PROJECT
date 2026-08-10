import json
import jwt
import os
import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.db.models import Q
from django.utils.text import slugify
from django.core.exceptions import ImproperlyConfigured
from .models import User, Category, Product, Cart, CartItem, Order, OrderItem, Review
from .views import featured_product_by_name, featured_product_by_slug


def _get_required_admin_pin():
    """Return the ADMIN_SECURITY_PIN from environment. Raises if not set."""
    pin = os.getenv('ADMIN_SECURITY_PIN', '').strip()
    if not pin:
        raise ImproperlyConfigured(
            "ADMIN_SECURITY_PIN is not set in the environment. "
            "The server cannot process admin operations without it."
        )
    return pin


def resolve_product_media(product):
    if product.image:
        return product.image.url, []
    slug = slugify(product.name)
    featured = featured_product_by_slug(slug) or featured_product_by_name(product.name)
    if not featured:
        return "", []
    return featured["image"], featured.get("gallery", [])

# Helper function
def get_user_from_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('user_id')
        if user_id is None:
            return None
        return User.objects.filter(id=user_id).first()
    except jwt.ExpiredSignatureError:
        return None  # Token has expired — reject silently
    except jwt.InvalidTokenError:
        return None  # Forged / malformed token — reject silently

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = get_user_from_token(request)
        if not user or (user.role != 'admin' and not user.is_superuser):
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
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)

        username = data.get('username', '').strip()
        password = data.get('password', '')

        # --- SECURITY FIX: role is ALWAYS forced to 'user' regardless of what ---
        # --- the client sends. Admins MUST be created via: manage.py createsuperuser ---
        role = 'user'

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)

        if len(username) < 3 or len(username) > 150:
            return JsonResponse({'error': 'Username must be between 3 and 150 characters'}, status=400)

        if len(password) < 8:
            return JsonResponse({'error': 'Password must be at least 8 characters'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already taken'}, status=400)

        user = User(username=username, role=role)
        user.set_password(password)
        user.save()
        # Create empty cart for the new user
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
            from django.contrib.auth import login as auth_login
            auth_login(request, user)
            role = 'admin' if (user.role == 'admin' or user.is_superuser) else user.role
            # SECURITY: Use timezone-aware UTC datetime (utcnow() is deprecated in Python 3.12+)
            payload = {
                'user_id': user.id,
                'role': role,
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=8)
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            return JsonResponse({'token': token, 'role': role})
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

_products_seeded = False

@csrf_exempt
def get_products(request):
    global _products_seeded
    if not _products_seeded:
        from .views import ensure_featured_products
        ensure_featured_products()
        _products_seeded = True
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
        image, gallery = resolve_product_media(p)
        data.append({
            'id': p.id,
            'name': p.name,
            'slug': slugify(p.name),
            'price': float(p.price),
            'stock': p.stock,
            'category': p.category.name if p.category else '',
            'description': p.description or '',
            'image': image,
            'gallery': gallery,
        })
    return JsonResponse({'products': data, 'total': total, 'page': page})

@csrf_exempt
@user_required
def manage_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    if request.method == 'GET':
        items = cart.items.select_related('product').all()
        # Fast lookup via dict (BE-3 performance constraint)
        items_list = []
        for item in items:
            image, _ = resolve_product_media(item.product)
            items_list.append({
                'product_id': item.product.id,
                'qty': item.quantity,
                'name': item.product.name,
                'price': float(item.product.price),
                'image': image,
            })
        
        total = sum(i['qty'] * i['price'] for i in items_list)
        return JsonResponse({'items': items_list, 'total': total})
        
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)
        pid = data.get('product_id')
        qty = data.get('quantity', 1)

        # SECURITY FIX: Validate quantity is a positive integer
        try:
            qty = int(qty)
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Invalid quantity'}, status=400)
        if qty < 1:
            return JsonResponse({'error': 'Quantity must be at least 1'}, status=400)
        if qty > 100:
            return JsonResponse({'error': 'Quantity cannot exceed 100 per request'}, status=400)

        product = Product.objects.filter(id=pid).first()
        if not product:
            return JsonResponse({'error': 'Product not found'}, status=404)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        new_qty = qty if created else item.quantity + qty

        # SECURITY FIX: Ensure cart quantity never exceeds available stock
        if new_qty > product.stock:
            return JsonResponse(
                {'error': f'Only {product.stock} unit(s) in stock'},
                status=400
            )

        item.quantity = new_qty
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
            # SECURITY FIX: Verify sufficient stock before placing the order
            if item.product.stock < item.quantity:
                order.delete()  # Roll back the order stub
                return JsonResponse(
                    {'error': f"Insufficient stock for '{item.product.name}'. "
                              f"Available: {item.product.stock}, requested: {item.quantity}"},
                    status=400
                )
            price = item.product.price
            items_to_create.append(OrderItem(
                order=order, product=item.product, price=price, quantity=item.quantity
            ))
            total += price * item.quantity
            item.product.stock -= item.quantity
            item.product.save()

        OrderItem.objects.bulk_create(items_to_create)  # optimization BE-3
        order.total_price = total
        order.save()

        cart.items.all().delete()  # clear cart
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
        orders = Order.objects.select_related('user').prefetch_related('items__product').all().order_by('-created_at')
        orders_data = []
        for o in orders:
            orders_data.append({
                'id': o.id,
                'customer': o.user.username,
                'items': [{'name': i.product.name, 'qty': i.quantity} for i in o.items.all()],
                'total': float(o.total_price),
                'status': o.status,
            })
        return JsonResponse({
            'orders_count': Order.objects.count(),
            'users_count': User.objects.count(),
            'orders': orders_data
        })

@csrf_exempt
@admin_required
def create_product(request):
    if request.method == "POST":
        # ── Level 2 Security: Mandatory Operations Security PIN ──────────────
        # SECURITY FIX: PIN is required from env — no weak fallback allowed.
        try:
            expected_pin = _get_required_admin_pin()
        except ImproperlyConfigured as e:
            return JsonResponse({'error': str(e)}, status=500)

        admin_pin = request.headers.get('X-Admin-Pin', '').strip()
        if not admin_pin or admin_pin != expected_pin:
            return JsonResponse({'error': 'MFA security PIN validation failed'}, status=403)

        # ── Parse request body (multipart form or JSON) ───────────────────────
        if 'multipart/form-data' in request.content_type or request.FILES:
            name = request.POST.get("name", "").strip()
            price_raw = request.POST.get("price", "")
            stock_raw = request.POST.get("stock", "0")
            category_name = request.POST.get("category", "").strip()
            description = request.POST.get("description", "").strip()
        else:
            try:
                data = json.loads(request.body)
            except (json.JSONDecodeError, ValueError):
                return JsonResponse({"error": "Invalid JSON body"}, status=400)
            name = data.get("name", "").strip()
            price_raw = data.get("price", "")
            stock_raw = data.get("stock", "0")
            category_name = data.get("category", "").strip()
            description = data.get("description", "").strip()

        # ── Input validation ──────────────────────────────────────────────────
        if not name:
            return JsonResponse({"error": "Product name is required"}, status=400)
        if not price_raw:
            return JsonResponse({"error": "Price is required"}, status=400)

        try:
            price = float(price_raw)
        except (TypeError, ValueError):
            return JsonResponse({"error": "Price must be a valid number"}, status=400)
        # SECURITY FIX: Reject negative prices
        if price < 0:
            return JsonResponse({"error": "Price cannot be negative"}, status=400)

        try:
            stock = int(stock_raw or 0)
        except (TypeError, ValueError):
            return JsonResponse({"error": "Stock must be a valid integer"}, status=400)
        # SECURITY FIX: Reject negative stock
        if stock < 0:
            return JsonResponse({"error": "Stock cannot be negative"}, status=400)

        category = None
        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)

        image = request.FILES.get('image')

        product = Product.objects.create(
            name=name,
            price=price,
            stock=stock,
            category=category,
            description=description,
            image=image
        )

        return JsonResponse({"message": "Product created", "id": product.id})

    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
@user_required
def profile(request):
    user = request.user
    if request.method == 'GET':
        return JsonResponse({
            'username': user.username,
            'mobile': user.first_name
        })
    elif request.method == 'POST':
        data = json.loads(request.body)
        new_username = data.get('username')
        new_password = data.get('password')
        new_mobile = data.get('mobile')
        
        if new_username:
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                return JsonResponse({'error': 'Username already taken'}, status=400)
            user.username = new_username
            
        if new_password:
            user.set_password(new_password)
            
        if new_mobile is not None:
            user.first_name = new_mobile
            
        user.save()
        return JsonResponse({'message': 'Profile updated successfully'})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_categories(request):
    if request.method == 'GET':
        categories = list(Category.objects.values_list('name', flat=True).distinct())
        return JsonResponse({'categories': categories})
    return JsonResponse({'error': 'Method not allowed'}, status=405)