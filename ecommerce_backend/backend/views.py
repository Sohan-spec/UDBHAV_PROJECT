from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Product


DUMMY_PRODUCT_DESCRIPTION = (
    "Ultra-precision. High-intensity shine in one swipe. "
    "8-hour wear with all-day comfort and smooth application. "
    "Color-true performance with no fade, feather, or flinch. "
    "Instantly conditions lips and skin with plumping moisture while creating a sleek, glossy finish."
)


FEATURED_PRODUCT_CATALOG = [
    {
        "slug": "algae-bloom-revitalizer",
        "name": "Algae Bloom Revitalizer",
        "category": "Skin Care",
        "price": 1299,
        "stock": 45,
        "description": "Ultra-hydrating overnight serum powered by mineral-rich sea algae. Restores skin bounce and helps dull skin look fresh by morning.",
        "image": "https://images.pexels.com/photos/4041392/pexels-photo-4041392.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "gallery": [
            "https://images.pexels.com/photos/4041392/pexels-photo-4041392.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1601049676869-702ea24cfd58?auto=format&fit=crop&w=1200&q=80",
            "https://images.pexels.com/photos/4041407/pexels-photo-4041407.jpeg?auto=compress&cs=tinysrgb&w=1200",
        ],
    },
    {
        "slug": "ocean-mist-body-oil",
        "name": "Ocean Mist Body Oil",
        "category": "Body Care",
        "price": 950,
        "stock": 56,
        "description": "Lightweight body oil with marine botanicals and vitamin E. Seals in moisture quickly and leaves a satin, non-sticky finish.",
        "image": "https://images.pexels.com/photos/4041391/pexels-photo-4041391.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "gallery": [
            "https://images.pexels.com/photos/4041391/pexels-photo-4041391.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    {
        "slug": "the-gift-set",
        "name": "The Gift Set",
        "category": "Gift Sets",
        "price": 1799,
        "stock": 32,
        "description": "A curated bundle of cleanser, serum, and glow cream in travel-ready sizes. Designed for simple routines and instant gifting.",
        "image": "https://images.pexels.com/photos/4465829/pexels-photo-4465829.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "gallery": [
            "https://images.pexels.com/photos/4465829/pexels-photo-4465829.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.unsplash.com/photo-1596462502278-27bfdc403348?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=1200&q=80",
            "https://images.pexels.com/photos/4041392/pexels-photo-4041392.jpeg?auto=compress&cs=tinysrgb&w=1200",
        ],
    },
    {
        "slug": "estee-lauder-call-555-lipstick",
        "name": "Estee Lauder Pure Color Explicit Slick Shine Lipstick - Call 555",
        "category": "Makeup",
        "price": 3500,
        "stock": 18,
        "description": "Ultra-precision, high-intensity shine lipstick with one-swipe payoff. Smooth glide, feather-light feel, and a rich satin finish.",
        "image": "https://images.pexels.com/photos/2533266/pexels-photo-2533266.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "gallery": [
            "https://images.pexels.com/photos/2533266/pexels-photo-2533266.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    {
        "slug": "sea-kelp-vitalizing-shampoo",
        "name": "Sea Kelp Vitalizing Shampoo",
        "category": "Hair Care",
        "price": 1320,
        "stock": 39,
        "description": "Sulfate-free shampoo enriched with sea kelp and niacinamide to cleanse buildup while preserving scalp moisture and shine.",
        "image": "https://images.pexels.com/photos/4465124/pexels-photo-4465124.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "gallery": [
            "https://images.pexels.com/photos/4465124/pexels-photo-4465124.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    {
        "slug": "dead-sea-mud-and-mint-mask",
        "name": "Dead Sea Mud & Mint Mask",
        "category": "Skin Care",
        "price": 2400,
        "stock": 24,
        "description": "Cooling clay mask with dead sea minerals and mint extract. Pulls out impurities and visibly softens texture in one use.",
        "image": "https://images.pexels.com/photos/3762873/pexels-photo-3762873.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "gallery": [
            "https://images.pexels.com/photos/3762873/pexels-photo-3762873.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=1200&q=80",
            "https://images.pexels.com/photos/3762875/pexels-photo-3762875.jpeg?auto=compress&cs=tinysrgb&w=1200",
        ],
    },
    {
        "slug": "coastal-breeze-cooling-mist",
        "name": "Coastal Breeze Cooling Mist",
        "category": "Body Care",
        "price": 240,
        "stock": 58,
        "description": "Rapid-cooling skin mist that refreshes and hydrates with lightweight marine extracts.",
        "image": "https://images.pexels.com/photos/4041390/pexels-photo-4041390.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "gallery": [
            "https://images.pexels.com/photos/4041390/pexels-photo-4041390.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.unsplash.com/photo-1571875257727-256c39da42af?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?auto=format&fit=crop&w=1200&q=80",
            "https://images.pexels.com/photos/4041391/pexels-photo-4041391.jpeg?auto=compress&cs=tinysrgb&w=1200",
        ],
    },
    {
        "slug": "reva-glow-cream-sample",
        "name": "REVA Novelty Glow Cream (Sample)",
        "category": "Gifts",
        "price": 0,
        "stock": 100,
        "description": "Miniature sample of our signature glow cream. Yours free as a REVA Novelty Gift!",
        "image": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1556228578-8c89e6adf883?auto=format&fit=crop&w=1200&q=80",
            "https://images.pexels.com/photos/3762875/pexels-photo-3762875.jpeg?auto=compress&cs=tinysrgb&w=1200",
        ],
    },
    {
        "slug": "algae-bloom-serum-vial",
        "name": "Algae Bloom Serum (Mini Vial)",
        "category": "Gifts",
        "price": 0,
        "stock": 150,
        "description": "Travel-sized tester of our best-selling revitalizing serum.",
        "image": "https://images.pexels.com/photos/4041407/pexels-photo-4041407.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "gallery": [
            "https://images.pexels.com/photos/4041407/pexels-photo-4041407.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    {
        "slug": "udbhav-keyring",
        "name": "Udbhav Official Keyring",
        "category": "Gifts",
        "price": 0,
        "stock": 200,
        "description": "Premium UDBHAV-branded collectible keychain.",
        "image": "https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?auto=format&fit=crop&w=1200&q=80",
        ],
    },
]


def ensure_featured_products():
    for item in FEATURED_PRODUCT_CATALOG:
        category, _ = Category.objects.get_or_create(name=item["category"])
        product, _ = Product.objects.get_or_create(
            name=item["name"],
            defaults={
                "category": category,
                "description": DUMMY_PRODUCT_DESCRIPTION,
                "price": item["price"],
                "stock": item["stock"],
            },
        )

        changed = False
        if product.category_id != category.id:
            product.category = category
            changed = True
        if float(product.price) != float(item["price"]):
            product.price = item["price"]
            changed = True
        if product.stock != item["stock"]:
            product.stock = item["stock"]
            changed = True
        if (product.description or "") != DUMMY_PRODUCT_DESCRIPTION:
            product.description = DUMMY_PRODUCT_DESCRIPTION
            changed = True

        if changed:
            product.save(update_fields=["category", "price", "stock", "description"])


def featured_product_by_slug(slug):
    return next((item for item in FEATURED_PRODUCT_CATALOG if item["slug"] == slug), None)


def featured_product_by_name(name):
    return next((item for item in FEATURED_PRODUCT_CATALOG if item["name"] == name), None)

def admin_required_session(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or (request.user.role != 'admin' and not request.user.is_superuser):
            return HttpResponse('Unauthorized: Admin access required', status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped

# Create your views here.
def homepage(request):
    return render(request,'homepage.html')

def shop(request):
    ensure_featured_products()
    return render(request, 'shop.html')

def product_detail(request, slug):
    from django.utils.text import slugify
    ensure_featured_products()
    item = featured_product_by_slug(slug)
    product = None
    if item:
        product = Product.objects.select_related('category').filter(name=item["name"]).first()

    if not product:
        for p in Product.objects.select_related('category').all():
            if slugify(p.name) == slug:
                product = p
                break

    if not product:
        return HttpResponse('Product not found', status=404)

    if not item:
        image_url = product.image.url if product.image else ""
        item = {
            "slug": slug,
            "name": product.name,
            "category": product.category.name if product.category else "Uncategorized",
            "price": float(product.price),
            "stock": product.stock,
            "description": product.description or DUMMY_PRODUCT_DESCRIPTION,
            "image": image_url,
            "gallery": [image_url] if image_url else [],
        }

    return render(request, 'product_detail.html', {
        'product': product,
        'item_meta': item,
        'dummy_description': DUMMY_PRODUCT_DESCRIPTION,
    })
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

# SECURITY FIX: Protect admin dashboard  require authenticated admin session.
@admin_required_session
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

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