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
    # ── Electronics: Smartphones ──────────────────────────────────────────────
    {
        "slug": "iphone-15",
        "name": "iPhone 15",
        "category": "Smartphones",
        "price": 79999,
        "stock": 25,
        "description": "Apple iPhone 15 with A16 Bionic chip, 48MP camera system, Dynamic Island, and all-day battery life. Premium build with ceramic shield front.",
        "image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=1200&h=1500&fit=crop",
            "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    {
        "slug": "iphone-14",
        "name": "iPhone 14",
        "category": "Smartphones",
        "price": 59999,
        "stock": 30,
        "description": "Apple iPhone 14 featuring A15 Bionic chip, advanced dual-camera system, Crash Detection, and Emergency SOS via satellite.",
        "image": "https://images.unsplash.com/photo-1678685888221-cda773a3dcdb?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1678685888221-cda773a3dcdb?w=1200&h=1500&fit=crop",
            "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    {
        "slug": "galaxy-s24",
        "name": "Galaxy S24",
        "category": "Smartphones",
        "price": 74999,
        "stock": 22,
        "description": "Samsung Galaxy S24 with Galaxy AI, Snapdragon 8 Gen 3, 50MP adaptive camera, and a stunning Dynamic AMOLED 2X display.",
        "image": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=1200&h=1500&fit=crop",
            "https://images.unsplash.com/photo-1585060544812-6b45742d762f?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    {
        "slug": "galaxy-s23",
        "name": "Galaxy S23",
        "category": "Smartphones",
        "price": 54999,
        "stock": 28,
        "description": "Samsung Galaxy S23 powered by Snapdragon 8 Gen 2, with Nightography camera, eco-conscious design, and all-day battery.",
        "image": "https://images.unsplash.com/photo-1678911820864-e2c567c655d7?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1678911820864-e2c567c655d7?w=1200&h=1500&fit=crop",
            "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    # ── Electronics: Laptops ──────────────────────────────────────────────────
    {
        "slug": "rog-zephyrus",
        "name": "ROG Zephyrus",
        "category": "Laptops",
        "price": 149999,
        "stock": 12,
        "description": "Asus ROG Zephyrus gaming laptop with AMD Ryzen 9, RTX 4070, 16-inch QHD+ 240Hz display, and ultra-slim magnesium-alloy chassis.",
        "image": "https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?w=1200&h=1500&fit=crop",
            "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    {
        "slug": "zenbook",
        "name": "ZenBook",
        "category": "Laptops",
        "price": 89999,
        "stock": 18,
        "description": "Asus ZenBook ultra-portable laptop with Intel Core Ultra, OLED display, NumberPad 2.0, and ErgoLift hinge for effortless productivity.",
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=1200&h=1500&fit=crop",
            "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    {
        "slug": "macbook-pro",
        "name": "MacBook Pro",
        "category": "Laptops",
        "price": 199999,
        "stock": 10,
        "description": "Apple MacBook Pro with M3 Pro chip, Liquid Retina XDR display, up to 22 hours battery life, and pro-level performance for demanding workflows.",
        "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=1200&h=1500&fit=crop",
            "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    {
        "slug": "macbook-air",
        "name": "MacBook Air",
        "category": "Laptops",
        "price": 114999,
        "stock": 15,
        "description": "Apple MacBook Air with M2 chip, 13.6-inch Liquid Retina display, fanless design, MagSafe charging, and up to 18 hours battery life.",
        "image": "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=1200&h=1500&fit=crop",
            "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    # ── Clothes: T-Shirts ─────────────────────────────────────────────────────
    {
        "slug": "polo-t-shirt",
        "name": "Polo T-Shirt",
        "category": "T-Shirts",
        "price": 999,
        "stock": 80,
        "description": "Classic cotton polo tee with a relaxed fit, ribbed collar, and two-button placket. Perfect for layering or wearing solo.",
        "image": "https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?w=1200&h=1500&fit=crop",
            "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    {
        "slug": "casual-graphic-t-shirt",
        "name": "Casual Graphic T-Shirt",
        "category": "T-Shirts",
        "price": 799,
        "stock": 100,
        "description": "Soft-washed graphic tee with bold print, crew neck, and a boxy unisex fit. Pre-shrunk 100% ring-spun cotton.",
        "image": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=1200&h=1500&fit=crop",
            "https://images.unsplash.com/photo-1562157873-818bc0726f68?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    # ── Clothes: Pants ────────────────────────────────────────────────────────
    {
        "slug": "jeans",
        "name": "Jeans",
        "category": "Pants",
        "price": 1499,
        "stock": 60,
        "description": "Selvedge-style denim jeans with a slim straight fit, five-pocket construction, and a sturdy brass button fly.",
        "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1542272604-787c3835535d?w=1200&h=1500&fit=crop",
            "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    {
        "slug": "chinos",
        "name": "Chinos",
        "category": "Pants",
        "price": 1299,
        "stock": 55,
        "description": "Tailored chinos in brushed cotton twill with a mid-rise waist, tapered leg, and hidden-stretch comfort for all-day wear.",
        "image": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=1200&h=1500&fit=crop",
            "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    # ── Household: Furniture — Sofas ──────────────────────────────────────────
    {
        "slug": "3-seater-recliner",
        "name": "3-Seater Recliner",
        "category": "Sofas",
        "price": 55999,
        "stock": 8,
        "description": "Three-seater recliner sofa in premium leatherette with adjustable headrests, cup holders, and soft-close footrests.",
        "image": "https://images.unsplash.com/photo-1601000785676-f9b0ade234d3?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1601000785676-f9b0ade234d3?w=1200&h=1500&fit=crop",
            "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    {
        "slug": "l-shaped-sofa",
        "name": "L-Shaped Sofa",
        "category": "Sofas",
        "price": 42999,
        "stock": 10,
        "description": "Modern L-shaped sectional sofa with high-density foam cushions, solid wood frame, and stain-resistant upholstery.",
        "image": "https://images.unsplash.com/photo-1680503397667-3877494708a1?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1680503397667-3877494708a1?w=1200&h=1500&fit=crop",
            "https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?auto=format&fit=crop&w=1200&q=80",
        ],
    },
    # ── Household: Kitchen — Utensils ─────────────────────────────────────────
    {
        "slug": "spoons",
        "name": "Spoons",
        "category": "Utensils",
        "price": 299,
        "stock": 150,
        "description": "Set of 6 stainless-steel tablespoons with mirror-polished finish and ergonomic handles. Dishwasher safe.",
        "image": "https://images.unsplash.com/photo-1619367300942-634bf2339af6?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1619367300942-634bf2339af6?w=1200&h=1500&fit=crop",
        ],
    },
    {
        "slug": "plates",
        "name": "Plates",
        "category": "Utensils",
        "price": 499,
        "stock": 120,
        "description": "Set of 6 ceramic dinner plates with chip-resistant glaze and minimalist design. Microwave and dishwasher safe.",
        "image": "https://images.unsplash.com/photo-1664337872259-12b178e34be8?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1664337872259-12b178e34be8?w=1200&h=1500&fit=crop",
        ],
    },
    {
        "slug": "forks",
        "name": "Forks",
        "category": "Utensils",
        "price": 249,
        "stock": 150,
        "description": "Set of 6 stainless-steel dinner forks with balanced weight and polished tines. Rust-resistant and dishwasher safe.",
        "image": "https://images.unsplash.com/photo-1690983321736-755af87b3f38?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1690983321736-755af87b3f38?w=1200&h=1500&fit=crop",
        ],
    },
    # ── Household: Kitchen — Groceries ────────────────────────────────────────
    {
        "slug": "rice",
        "name": "Rice",
        "category": "Groceries",
        "price": 199,
        "stock": 200,
        "description": "Premium long-grain basmati rice, aged for extra aroma and fluffiness. Sourced directly from farms. Per kg.",
        "image": "https://images.unsplash.com/photo-1714040292680-5a9ea419b6b5?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1714040292680-5a9ea419b6b5?w=1200&h=1500&fit=crop",
        ],
    },
    {
        "slug": "wheat",
        "name": "Wheat",
        "category": "Groceries",
        "price": 149,
        "stock": 200,
        "description": "Whole wheat grain, stone-ground quality for fresh chapatis and baking. Pesticide-free. Per kg.",
        "image": "https://images.unsplash.com/photo-1609130825188-a66b4aef2278?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1609130825188-a66b4aef2278?w=1200&h=1500&fit=crop",
        ],
    },
    {
        "slug": "vegetables",
        "name": "Vegetables",
        "category": "Groceries",
        "price": 99,
        "stock": 300,
        "description": "Fresh seasonal vegetable mix — hand-picked daily from local farms. Clean-washed and ready to cook. Per kg.",
        "image": "https://images.unsplash.com/photo-1610636996379-4d184e2ef20a?w=1200&h=1500&fit=crop",
        "gallery": [
            "https://images.unsplash.com/photo-1610636996379-4d184e2ef20a?w=1200&h=1500&fit=crop",
        ],
    },
]


def ensure_featured_products():
    for item in FEATURED_PRODUCT_CATALOG:
        category, _ = Category.objects.get_or_create(name=item["category"])
        desc = item.get("description") or DUMMY_PRODUCT_DESCRIPTION
        product, _ = Product.objects.get_or_create(
            name=item["name"],
            defaults={
                "category": category,
                "description": desc,
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
        if (product.description or "") != desc:
            product.description = desc
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
    ensure_featured_products()
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