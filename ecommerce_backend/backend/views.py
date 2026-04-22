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
        "image": "https://images.pexels.com/photos/6621469/pexels-photo-6621469.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "gallery": [
            "https://images.pexels.com/photos/6621469/pexels-photo-6621469.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/5069433/pexels-photo-5069433.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/7796574/pexels-photo-7796574.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/3737579/pexels-photo-3737579.jpeg?auto=compress&cs=tinysrgb&w=1200",
        ],
    },
    {
        "slug": "ocean-mist-body-oil",
        "name": "Ocean Mist Body Oil",
        "category": "Body Care",
        "price": 950,
        "stock": 56,
        "description": "Lightweight body oil with marine botanicals and vitamin E. Seals in moisture quickly and leaves a satin, non-sticky finish.",
        "image": "https://images.pexels.com/photos/3737579/pexels-photo-3737579.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "gallery": [
            "https://images.pexels.com/photos/3737579/pexels-photo-3737579.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/3373726/pexels-photo-3373726.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/6663570/pexels-photo-6663570.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/4465827/pexels-photo-4465827.jpeg?auto=compress&cs=tinysrgb&w=1200",
        ],
    },
    {
        "slug": "the-gift-set",
        "name": "The Gift Set",
        "category": "Gift Sets",
        "price": 1799,
        "stock": 32,
        "description": "A curated bundle of cleanser, serum, and glow cream in travel-ready sizes. Designed for simple routines and instant gifting.",
        "image": "https://images.pexels.com/photos/7796574/pexels-photo-7796574.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "gallery": [
            "https://images.pexels.com/photos/7796574/pexels-photo-7796574.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/5069433/pexels-photo-5069433.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/6621469/pexels-photo-6621469.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/3762879/pexels-photo-3762879.jpeg?auto=compress&cs=tinysrgb&w=1200",
        ],
    },
    {
        "slug": "estee-lauder-call-555-lipstick",
        "name": "Estee Lauder Pure Color Explicit Slick Shine Lipstick - Call 555",
        "category": "Makeup",
        "price": 3500,
        "stock": 18,
        "description": "Ultra-precision, high-intensity shine lipstick with one-swipe payoff. Smooth glide, feather-light feel, and a rich satin finish.",
        "image": "https://images.pexels.com/photos/3373726/pexels-photo-3373726.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "gallery": [
            "https://images.pexels.com/photos/3373726/pexels-photo-3373726.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/6621332/pexels-photo-6621332.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/7440054/pexels-photo-7440054.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/7755654/pexels-photo-7755654.jpeg?auto=compress&cs=tinysrgb&w=1200",
        ],
    },
    {
        "slug": "sea-kelp-vitalizing-shampoo",
        "name": "Sea Kelp Vitalizing Shampoo",
        "category": "Hair Care",
        "price": 1320,
        "stock": 39,
        "description": "Sulfate-free shampoo enriched with sea kelp and niacinamide to cleanse buildup while preserving scalp moisture and shine.",
        "image": "https://images.pexels.com/photos/4465827/pexels-photo-4465827.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "gallery": [
            "https://images.pexels.com/photos/4465827/pexels-photo-4465827.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/6621469/pexels-photo-6621469.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/3737579/pexels-photo-3737579.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/7796574/pexels-photo-7796574.jpeg?auto=compress&cs=tinysrgb&w=1200",
        ],
    },
    {
        "slug": "dead-sea-mud-and-mint-mask",
        "name": "Dead Sea Mud & Mint Mask",
        "category": "Skin Care",
        "price": 2400,
        "stock": 24,
        "description": "Cooling clay mask with dead sea minerals and mint extract. Pulls out impurities and visibly softens texture in one use.",
        "image": "https://images.pexels.com/photos/6621332/pexels-photo-6621332.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "gallery": [
            "https://images.pexels.com/photos/6621332/pexels-photo-6621332.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/6621469/pexels-photo-6621469.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/3762879/pexels-photo-3762879.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/5069433/pexels-photo-5069433.jpeg?auto=compress&cs=tinysrgb&w=1200",
        ],
    },
    {
        "slug": "coastal-breeze-cooling-mist",
        "name": "Coastal Breeze Cooling Mist",
        "category": "Body Care",
        "price": 240,
        "stock": 58,
        "description": "Rapid-cooling skin mist that refreshes and hydrates with lightweight marine extracts.",
        "image": "https://images.pexels.com/photos/4465122/pexels-photo-4465122.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "gallery": [
            "https://images.pexels.com/photos/4465122/pexels-photo-4465122.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/3373730/pexels-photo-3373730.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/6621457/pexels-photo-6621457.jpeg?auto=compress&cs=tinysrgb&w=1200",
            "https://images.pexels.com/photos/6621460/pexels-photo-6621460.jpeg?auto=compress&cs=tinysrgb&w=1200",
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
        if not request.user.is_authenticated or request.user.role != 'admin':
            return HttpResponse('Unauthorized: Admin access required', status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped

# Create your views here.
def homepage(request):
    ensure_featured_products()
    return render(request,'homepage.html')


def product_detail(request, slug):
    ensure_featured_products()
    item = featured_product_by_slug(slug)
    if not item:
        return HttpResponse('Product not found', status=404)

    product = Product.objects.select_related('category').filter(name=item["name"]).first()
    if not product:
        return HttpResponse('Product not found', status=404)

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