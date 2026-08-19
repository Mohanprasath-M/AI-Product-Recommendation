import os
import csv
import uuid
import random
from datetime import datetime, timedelta, timezone

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
os.makedirs(DATA_DIR, exist_ok=True)

CATEGORIES = [
    {"name": "Electronics", "slug": "electronics", "icon": "Cpu", "desc": "Smartphones, Audio, Laptops, and Smart Home"},
    {"name": "Sports & Fitness", "slug": "sports", "icon": "Activity", "desc": "Performance Apparel, Footwear, and Equipment"},
    {"name": "Fashion & Apparel", "slug": "fashion", "icon": "ShoppingBag", "desc": "Modern Trends, Footwear, and Luxury Essentials"},
    {"name": "Home & Kitchen", "slug": "home", "icon": "Home", "desc": "Appliances, Decor, Cookware, and Smart Living"},
    {"name": "Gaming", "slug": "gaming", "icon": "Gamepad2", "desc": "Consoles, Headsets, Keyboards, and Peripherals"},
    {"name": "Beauty & Personal Care", "slug": "beauty", "icon": "Sparkles", "desc": "Skincare, Fragrances, and Wellness Products"},
    {"name": "Books & Stationery", "slug": "books", "icon": "BookOpen", "desc": "Bestsellers, Tech Guides, and Productivity Tools"},
    {"name": "Accessories", "slug": "accessories", "icon": "Watch", "desc": "Smartwatches, Bags, Eyewear, and Wallets"}
]

BRANDS = {
    "Electronics": ["Sony", "Apple", "Samsung", "Bose", "Anker", "Logitech", "Dell", "LG"],
    "Sports & Fitness": ["Nike", "Adidas", "Puma", "Under Armour", "Lululemon", "Gymshark", "Garmin"],
    "Fashion & Apparel": ["Zara", "H&M", "Levi's", "Calvin Klein", "Tommy Hilfiger", "Uniqlo"],
    "Home & Kitchen": ["Dyson", "Ninja", "Instant Pot", "Philips", "Nespresso", "KitchenAid"],
    "Gaming": ["Razer", "Corsair", "SteelSeries", "HyperX", "Logitech G", "ASUS ROG"],
    "Beauty & Personal Care": ["The Ordinary", "CeraVe", "L'Oreal", "Neutrogena", "Estee Lauder"],
    "Books & Stationery": ["Penguin", "O'Reilly", "HarperCollins", "Muji", "Moleskine"],
    "Accessories": ["Fossil", "Ray-Ban", "Herschel", "Bellroy", "Casio", "Oakley"]
}

PRODUCT_TEMPLATES = {
    "Electronics": [
        ("Noise-Cancelling Wireless Headphones", 199.99, "Premium active noise cancellation with 30-hour battery life and spatial audio.", "wireless,audio,bluetooth,noise-cancelling"),
        ("Smart 4K OLED Ultra HD TV 55-inch", 899.99, "True black OLED contrast, HDR10+, Dolby Vision and 120Hz gaming support.", "tv,4k,oled,smart-home,display"),
        ("Ultra-Slim Laptop 14-inch 16GB RAM", 1099.99, "Next-gen processor, all-day battery, vivid retina display, and aluminum chassis.", "laptop,productivity,work,ultrabook"),
        ("Compact Fast Wireless Charging Pad", 34.99, "15W Qi-certified high-speed wireless charging with LED status indicator.", "charger,wireless,accessory,mobile"),
        ("True Wireless Earbuds with ANC", 129.99, "Crystal-clear calls, IPX5 water resistance, and ergonomic fit.", "earbuds,audio,bluetooth,portable"),
        ("Smart Home Voice Assistant Speaker", 79.99, "Room-filling sound with integrated voice AI and smart home hub.", "speaker,smart-home,ai,audio"),
        ("Mechanical Gaming Keyboard RGB", 119.99, "Hot-swappable switches, per-key RGB backlighting, and aluminum frame.", "keyboard,gaming,rgb,mechanical"),
        ("High-Speed Portable SSD 1TB", 109.99, "Up to 1050MB/s transfer speeds, drop-resistant, and USB-C compatible.", "storage,ssd,portable,backup"),
        ("Wireless Over-Ear Studio Monitor", 179.99, "Hi-Res certified sound with ultra-low latency and plush memory foam.", "audio,studio,monitor,wireless"),
        ("Smart HD Security Camera 360", 69.99, "Night vision, two-way audio, and motion detection with cloud storage.", "camera,security,smarthome,video"),
    ],
    "Sports & Fitness": [
        ("Pro Running Shoes Breathable Cushion", 139.99, "Engineered mesh upper, responsive foam cushioning, and high-traction rubber outsole.", "running,shoes,footwear,cushion"),
        ("Performance Moisture-Wicking T-Shirt", 29.99, "Four-way stretch fabric designed for high-intensity training and comfort.", "apparel,fitness,workout,tshirt"),
        ("Adjustable Dumbbell Set 5-52.5 lbs", 299.99, "Space-saving rapid weight adjustment system for complete home workouts.", "weights,fitness,home-gym,workout"),
        ("High-Density Yoga Mat Non-Slip", 39.99, "Eco-friendly dual-layer cushioning with alignment lines.", "yoga,mat,fitness,wellness"),
        ("Thermal Insulated Stainless Water Bottle", 24.99, "Keeps liquids cold for 24 hours or hot for 12 hours with leakproof lid.", "hydration,bottle,outdoor,sports"),
        ("Compression Workout Leggings", 49.99, "High-waisted tummy control compression tights with side phone pockets.", "apparel,leggings,fitness,women"),
        ("Speed Jump Rope with Ball Bearings", 19.99, "Tangle-free steel cable with non-slip aluminum alloy handles.", "cardio,jumprope,fitness,crossfit"),
        ("Trail Hiking Backpack 30L", 89.99, "Ergonomic ventilation frame with rain cover and trekking pole attachments.", "hiking,outdoor,backpack,trail"),
    ],
    "Fashion & Apparel": [
        ("Classic Denim Jacket Vintage Wash", 79.99, "100% heavy cotton denim with timeless silhouette and metal buttons.", "jacket,denim,casual,vintage"),
        ("Slim-Fit Stretch Oxford Shirt", 49.99, "Breathable wrinkle-resistant cotton blend suitable for office or casual.", "shirt,oxford,business,casual"),
        ("Casual Streetwear Heavyweight Hoodie", 59.99, "Plush fleece interior with oversized kangaroo pocket and double-lined hood.", "hoodie,streetwear,casual,fleece"),
        ("Tailored Stretch Chino Pants", 54.99, "Flexible all-day comfort with modern slim tapered cut.", "pants,chinos,casual,style"),
        ("Merino Wool Crewneck Sweater", 89.99, "Ultra-soft premium Australian merino wool with natural temperature regulation.", "sweater,wool,luxury,winter"),
        ("Waterproof Trench Coat Classic", 149.99, "Double-breasted storm flap with belted waist and premium lining.", "coat,trench,outerwear,fashion"),
        ("Leather Chelsea Boots Handcrafted", 129.99, "Full-grain leather with elastic side gussets and durable rubber sole.", "boots,footwear,leather,chelsea"),
        ("Silk Satin Evening Scarf", 39.99, "100% mulberry silk with vibrant print and hand-rolled edges.", "scarf,silk,luxury,accessory"),
    ],
    "Home & Kitchen": [
        ("Multi-Functional Air Fryer 6-Quart", 119.99, "One-touch digital presets, 360 rapid air circulation, and dishwasher-safe basket.", "kitchen,airfryer,cooking,appliances"),
        ("Single-Serve Coffee & Espresso Machine", 149.99, "Fast 30-second heat-up, 19-bar extraction pressure, and compact footprint.", "coffee,espresso,kitchen,beverage"),
        ("Cordless Stick Vacuum Cleaner", 249.99, "High-torque digital motor with laser dust detection and 60-min runtime.", "vacuum,cleaning,home,cordless"),
        ("Cast Iron Dutch Oven 6-Quart", 79.99, "Enamelled heavy-duty cast iron for braising, baking, and stewing.", "cookware,dutch-oven,castiron,kitchen"),
        ("Aroma Essential Oil Diffuser Ultrasonic", 29.99, "Whisper-quiet ultrasonic mist with 7 ambient LED colors.", "home,wellness,aroma,decor"),
        ("Smart Electric Kettle Temperature Control", 69.99, "Precise 1-degree temperature setting with 60-min keep-warm mode.", "kettle,kitchen,tea,coffee"),
        ("Professional Chef Knife 8-inch Damascus", 89.99, "67-layer Japanese VG-10 high carbon stainless steel with ergonomic handle.", "knife,kitchen,chef,cooking"),
        ("Robotic Vacuum & Mop Combo LiDAR", 349.99, "Precision LiDAR mapping, 4000Pa suction, and auto-carpet boost.", "robot,vacuum,smarthome,cleaning"),
    ],
    "Gaming": [
        ("Wireless Pro Gaming Mouse 20K DPI", 99.99, "Sub-1ms wireless latency, lightweight 63g build, and optical switches.", "mouse,gaming,wireless,esports"),
        ("Surround Sound 7.1 Gaming Headset", 89.99, "Detachable noise-cancelling microphone, memory foam ear cups, and 50mm drivers.", "headset,gaming,audio,rgb"),
        ("Curved Gaming Monitor 27-inch 165Hz", 279.99, "1500R curvature, 1ms response time, AMD FreeSync Premium, and QHD 1440p.", "monitor,gaming,display,165hz"),
        ("Ergonomic High-Back Gaming Chair", 199.99, "Adjustable lumbar support, 4D armrests, and high-density cold-cure foam.", "chair,gaming,ergonomic,furniture"),
        ("Stream Deck 15-Key Macro Controller", 149.99, "Customizable LCD keys to trigger live streaming actions and integrations.", "streamer,macro,controller,gaming"),
        ("USB Condenser Microphone RGB", 79.99, "Cardioid pickup pattern with tap-to-mute sensor and shock mount.", "mic,audio,streaming,recording"),
        ("Gaming Mouse Pad Extended XL RGB", 34.99, "Micro-textured cloth surface with 14 chroma lighting zones.", "mousepad,gaming,rgb,deskmat"),
        ("Game Controller Wireless Bluetooth", 59.99, "Hall effect magnetic joysticks with dual vibration and turbo function.", "controller,gamepad,wireless,gaming"),
    ],
    "Beauty & Personal Care": [
        ("Hyaluronic Acid Hydrating Serum", 19.99, "Multi-depth hydration with pure vegan hyaluronic acid and Vitamin B5.", "skincare,serum,hydration,beauty"),
        ("Daily Facial Moisturizer SPF 30", 24.99, "Non-greasy mineral sunscreen protection with ceramides and niacinamide.", "skincare,sunscreen,moisturizer,daily"),
        ("Sonic Electric Toothbrush Smart", 69.99, "40,000 vibrations per minute, 4 cleaning modes, and pressure sensor.", "dental,oralcare,electric,hygiene"),
        ("Luxury Eau De Parfum 100ml", 89.99, "Sophisticated notes of bergamot, cedarwood, amber, and vetiver.", "fragrance,perfume,luxury,grooming"),
        ("Vitamin C Radiance Glow Serum", 29.99, "15% pure L-Ascorbic acid with Ferulic acid for brightened complexion.", "skincare,vitaminc,glow,anti-aging"),
        ("Hydrating Cleansing Oil Gentle", 22.99, "Melts stubborn makeup without stripping moisture barrier.", "cleanser,skincare,makeup,gentle"),
        ("Revitalizing Hair Mask Argan Oil", 26.99, "Deep conditioning treatment for smooth, salon-finish silky hair.", "haircare,mask,arganoil,beauty"),
        ("Professional Ionic Hair Dryer", 119.99, "Brushless motor with intelligent heat control and magnetic styling nozzles.", "hairdryer,styling,beauty,salon"),
    ],
    "Books & Stationery": [
        ("Machine Learning & AI Engineering Handbook", 49.99, "Comprehensive guide to modern neural networks, recommender systems, and MLOps.", "book,tech,ai,programming"),
        ("Hardcover Dotted Grid Journal", 18.99, "120gsm ink-proof paper with dual bookmarks and expandable rear pocket.", "stationery,journal,notebook,writing"),
        ("Atomic Habits & Mindset Masterclass", 21.99, "Proven framework for continuous improvement and personal productivity.", "book,productivity,habits,bestseller"),
        ("Clean Architecture & System Design", 44.99, "Principles of software structure, enterprise scalability, and domain design.", "book,engineering,coding,architecture"),
        ("Fine Fountain Pen with Gold Nib", 59.99, "Hand-balanced brass barrel with iridium tipped medium nib.", "pen,fountainpen,luxury,stationery"),
        ("Noise-Cancelling Desk Study Lamp LED", 39.99, "Eye-caring anti-glare light with wireless phone charging base.", "desk,lamp,stationery,office"),
        ("Executive Leather Portfolio Folder", 49.99, "Holds legal pad, tablet, cards, and pens with magnetic closure.", "portfolio,leather,business,office"),
        ("The Psychology of Money Insights", 19.99, "Timeless lessons on wealth, greed, and happiness in investing.", "book,finance,wealth,investing"),
    ],
    "Accessories": [
        ("Minimalist Slim RFID Blocking Wallet", 34.99, "Aerospace-grade aluminum and genuine top-grain leather with card quick-eject.", "wallet,rfid,minimalist,leather"),
        ("Polarized Aviator Sunglasses UV400", 69.99, "Classic stainless steel frames with anti-glare scratch-resistant lenses.", "sunglasses,eyewear,fashion,polarized"),
        ("Smart Fitness Tracker & Heart Rate Watch", 119.99, "Continuous SpO2, sleep tracking, GPS, and 10-day battery life.", "smartwatch,fitness,wearable,tech"),
        ("Water-Resistant Commuter Backpack 25L", 79.99, "Dedicated 16-inch laptop compartment, hidden passport pocket, and luggage strap.", "backpack,travel,commuter,bags"),
        ("Genuine Leather Watch Strap Band", 29.99, "Quick-release Italian calfskin leather with polished stainless buckle.", "watchstrap,leather,accessory,style"),
        ("Compact Travel Umbrella Windproof", 24.99, "Teflon coated 9-rib reinforced fiberglass canopy with auto open/close.", "umbrella,travel,weather,accessory"),
        ("Aerospace Aluminum Key Organizer", 19.99, "Holds up to 14 keys silently with pocket clip and bottle opener.", "keychain,edc,organizer,minimal"),
        ("Leather Weekender Duffle Bag 45L", 139.99, "Vintage look full-grain leather with separate ventilated shoe compartment.", "duffle,travel,leather,weekender")
    ]
}

PERSONAS = [
    ("Tech Enthusiast", ["Electronics", "Gaming", "Accessories"], ["Sony", "Apple", "Samsung", "Razer", "Corsair"], 800.0, 1800.0),
    ("Fitness & Health Buff", ["Sports & Fitness", "Accessories", "Beauty & Personal Care"], ["Nike", "Adidas", "Puma", "Garmin", "Lululemon"], 300.0, 900.0),
    ("Modern Home Cook & Decorator", ["Home & Kitchen", "Books & Stationery"], ["Dyson", "Ninja", "Instant Pot", "Philips", "Nespresso"], 400.0, 1200.0),
    ("Trend & Fashion Shopper", ["Fashion & Apparel", "Accessories", "Beauty & Personal Care"], ["Zara", "H&M", "Levi's", "Ray-Ban", "Calvin Klein"], 350.0, 1000.0),
    ("Gamer & Streamer", ["Gaming", "Electronics", "Accessories"], ["Razer", "Logitech G", "Corsair", "SteelSeries", "HyperX"], 600.0, 1500.0),
    ("Budget Conscious Shopper", ["Fashion & Apparel", "Home & Kitchen", "Books & Stationery"], ["Uniqlo", "H&M", "Casio", "Muji"], 100.0, 400.0),
    ("Luxury VIP Buyer", ["Electronics", "Fashion & Apparel", "Accessories"], ["Apple", "Dyson", "Bose", "Ray-Ban", "Tommy Hilfiger"], 1200.0, 3500.0)
]

FIRST_NAMES = ["James", "Emma", "Liam", "Olivia", "Noah", "Ava", "William", "Sophia", "Oliver", "Isabella",
               "Lucas", "Mia", "Benjamin", "Charlotte", "Henry", "Amelia", "Alexander", "Harper", "Sebastian", "Evelyn",
               "Kishore", "Aarav", "Priya", "Rahul", "Ananya", "Vikram", "Sneha", "Aditya", "Neha", "Rohan"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
              "Sharma", "Patel", "Kumar", "Singh", "Reddy", "Verma", "Rao", "Gupta", "Kapoor", "Joshi"]
CITIES = ["San Francisco, CA", "New York, NY", "Austin, TX", "Seattle, WA", "Chicago, IL", "Boston, MA", "Denver, CO", "Los Angeles, CA", "London, UK", "Toronto, CA", "Bengaluru, IN", "Mumbai, IN"]


def generate_all_datasets():
    print("Generating synthetic datasets...")

    # 1. Categories
    categories_file = os.path.join(DATA_DIR, "categories.csv")
    with open(categories_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "slug", "icon", "description"])
        for c in CATEGORIES:
            writer.writerow([str(uuid.uuid4()), c["name"], c["slug"], c["icon"], c["desc"]])

    # 2. Products (500+ items)
    products_file = os.path.join(DATA_DIR, "products.csv")
    products = []
    prod_id_counter = 1

    for cat_name, brand_list in BRANDS.items():
        templates = PRODUCT_TEMPLATES.get(cat_name, PRODUCT_TEMPLATES["Electronics"])
        for b in brand_list:
            for t_name, base_price, desc, tags in templates:
                # Add price variation & brand prefix
                price = round(base_price * random.uniform(0.85, 1.25), 2)
                stock = random.randint(15, 250)
                rating = round(random.uniform(3.8, 4.9), 1)
                rating_cnt = random.randint(12, 450)
                views = random.randint(150, 4500)
                purchases = int(views * random.uniform(0.03, 0.12))
                rev = round(purchases * price, 2)
                trend_score = round(random.uniform(-20.0, 85.0), 1)
                trend_status = "TRENDING_UP" if trend_score > 30 else ("TRENDING_DOWN" if trend_score < 0 else "STABLE")

                p_id = str(uuid.uuid4())
                p_code = f"PROD-{prod_id_counter:04d}"
                full_name = f"{b} {t_name}"

                products.append({
                    "id": p_id,
                    "product_code": p_code,
                    "name": full_name,
                    "description": f"{full_name} by {b}. {desc}",
                    "category": cat_name,
                    "brand": b,
                    "price": price,
                    "discount": random.choice([0.0, 5.0, 10.0, 15.0, 20.0]),
                    "stock": stock,
                    "rating": rating,
                    "rating_count": rating_cnt,
                    "image_url": f"https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80",
                    "tags": tags,
                    "views_count": views,
                    "purchases_count": purchases,
                    "revenue_generated": rev,
                    "trend_score": trend_score,
                    "trend_status": trend_status
                })
                prod_id_counter += 1

    with open(products_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)

    print(f"Generated {len(products)} products.")

    # 3. Customers (1,000+ customers)
    customers_file = os.path.join(DATA_DIR, "customers.csv")
    customers = []
    for i in range(1, 1050):
        c_id = str(uuid.uuid4())
        fname = random.choice(FIRST_NAMES)
        lname = random.choice(LAST_NAMES)
        name = f"{fname} {lname}"
        email = f"{fname.lower()}.{lname.lower()}{i}@example.com"
        persona_tuple = random.choice(PERSONAS)
        persona_name, fav_cats, fav_brands, min_spend, max_spend = persona_tuple

        total_orders = random.randint(1, 22)
        total_spend = round(random.uniform(min_spend, max_spend), 2)
        aov = round(total_spend / total_orders, 2)
        clv_est = round(total_spend * random.uniform(1.3, 2.5), 2)
        churn_risk = round(random.uniform(0.05, 0.85), 2)
        churn_level = "HIGH" if churn_risk >= 0.65 else ("MEDIUM" if churn_risk >= 0.35 else "LOW")

        customers.append({
            "id": c_id,
            "customer_code": f"CUST-{i:04d}",
            "name": name,
            "email": email,
            "age": random.randint(18, 65),
            "gender": random.choice(["Male", "Female", "Non-Binary"]),
            "location": random.choice(CITIES),
            "persona": persona_name,
            "total_spend": total_spend,
            "total_orders": total_orders,
            "avg_order_value": aov,
            "clv_historical": total_spend,
            "clv_estimated": clv_est,
            "churn_risk_score": churn_risk,
            "churn_risk_level": churn_level,
            "favorite_category": random.choice(fav_cats),
            "favorite_brand": random.choice(fav_brands),
            "preferred_price_min": round(aov * 0.4, 2),
            "preferred_price_max": round(aov * 2.5, 2),
            "created_at": (datetime.now(timezone.utc) - timedelta(days=random.randint(20, 365))).isoformat(),
            "last_active_at": (datetime.now(timezone.utc) - timedelta(days=random.randint(0, 45))).isoformat()
        })

    with open(customers_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=customers[0].keys())
        writer.writeheader()
        writer.writerows(customers)

    print(f"Generated {len(customers)} customers.")

    # 4. Interactions (20,000+ interactions correlated with personas)
    interactions_file = os.path.join(DATA_DIR, "interactions.csv")
    interactions = []
    event_types = ["VIEW_PRODUCT", "CLICK_PRODUCT", "ADD_TO_WISHLIST", "ADD_TO_CART", "PURCHASE", "RATING"]

    prod_by_category = {}
    for p in products:
        prod_by_category.setdefault(p["category"], []).append(p)

    for c in customers:
        num_interactions = random.randint(15, 35)
        fav_cat = c["favorite_category"]
        pool = prod_by_category.get(fav_cat, products)

        for _ in range(num_interactions):
            p = random.choice(pool) if random.random() < 0.70 else random.choice(products)
            ev = random.choices(event_types, weights=[50, 25, 10, 10, 3, 2])[0]
            weight = {"VIEW_PRODUCT": 1.0, "CLICK_PRODUCT": 2.0, "ADD_TO_WISHLIST": 3.0, "ADD_TO_CART": 4.0, "PURCHASE": 5.0, "RATING": 4.0}[ev]
            
            ts = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 60), hours=random.randint(0, 23))
            interactions.append({
                "id": str(uuid.uuid4()),
                "customer_id": c["id"],
                "product_id": p["id"],
                "event_type": ev,
                "weight": weight,
                "session_id": f"sess_{c['id'][:6]}_{random.randint(1, 10)}",
                "timestamp": ts.isoformat()
            })

    with open(interactions_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=interactions[0].keys())
        writer.writeheader()
        writer.writerows(interactions)

    print(f"Generated {len(interactions)} interactions.")

    # 5. Purchases / Orders (5,000+ purchases with market basket affinities)
    purchases_file = os.path.join(DATA_DIR, "purchases.csv")
    purchases = []
    for _ in range(5200):
        c = random.choice(customers)
        p1 = random.choice(products)
        ts = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 90), hours=random.randint(0, 23))
        
        # Basket co-purchase item
        p2 = random.choice(prod_by_category.get(p1["category"], products))
        qty1 = random.randint(1, 2)
        qty2 = random.randint(1, 2) if random.random() < 0.45 else 0

        total = round(p1["price"] * qty1 + (p2["price"] * qty2 if qty2 > 0 else 0), 2)
        order_id = str(uuid.uuid4())

        purchases.append({
            "order_id": order_id,
            "customer_id": c["id"],
            "product_id": p1["id"],
            "product_name": p1["name"],
            "quantity": qty1,
            "unit_price": p1["price"],
            "total_amount": total,
            "timestamp": ts.isoformat()
        })
        if qty2 > 0:
            purchases.append({
                "order_id": order_id,
                "customer_id": c["id"],
                "product_id": p2["id"],
                "product_name": p2["name"],
                "quantity": qty2,
                "unit_price": p2["price"],
                "total_amount": total,
                "timestamp": ts.isoformat()
            })

    with open(purchases_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=purchases[0].keys())
        writer.writeheader()
        writer.writerows(purchases)

    print(f"Generated {len(purchases)} purchase line items.")

    # 6. Reviews (5,000+ realistic reviews)
    reviews_file = os.path.join(DATA_DIR, "reviews.csv")
    POSITIVE_COMMENTS = [
        "Absolutely amazing quality and sound! Best purchase I have made in months.",
        "Super comfortable, stylish, and fits perfectly. Highly recommend to everyone.",
        "Excellent battery life and very fast performance. Surpassed all my expectations.",
        "Great value for the price. Sturdy build, easy setup, and smooth daily experience.",
        "Impressive craftsmanship! The material feels premium and durable.",
        "Works like a charm. Fast shipping, clear display, and flawless design."
    ]
    NEGATIVE_COMMENTS = [
        "Disappointed with the build quality. Battery drains way too fast and broke quickly.",
        "Poor sound and noisy microphone. Difficult to setup and constantly lagged.",
        "Cheap materials used. Stopped working after two weeks, had to request a refund.",
        "Defective unit. Had a major problem with charging and customer support was unhelpful.",
        "Uncomfortable fit and heavy. Definite waste of money, returning immediately."
    ]
    NEUTRAL_COMMENTS = [
        "Decent product for casual use. Nothing extraordinary but works as advertised.",
        "Average build quality. Expected a bit more for the price, but it does the job.",
        "Acceptable performance. Good design, though setup took longer than anticipated."
    ]

    reviews = []
    for _ in range(5100):
        c = random.choice(customers)
        p = random.choice(products)
        sentiment_type = random.choices(["POS", "NEU", "NEG"], weights=[70, 15, 15])[0]

        if sentiment_type == "POS":
            rating = float(random.choice([4.0, 4.5, 5.0]))
            comment = random.choice(POSITIVE_COMMENTS)
            label = "POSITIVE"
            score = round(random.uniform(0.65, 0.98), 2)
            pos_t = ["quality", "comfortable", "battery", "sound", "value"][:random.randint(2, 4)]
            neg_t = []
        elif sentiment_type == "NEG":
            rating = float(random.choice([1.0, 1.5, 2.0, 2.5]))
            comment = random.choice(NEGATIVE_COMMENTS)
            label = "NEGATIVE"
            score = round(random.uniform(-0.95, -0.45), 2)
            pos_t = []
            neg_t = ["battery", "microphone", "charging", "noise", "broken"][:random.randint(2, 4)]
        else:
            rating = float(random.choice([3.0, 3.5]))
            comment = random.choice(NEUTRAL_COMMENTS)
            label = "NEUTRAL"
            score = round(random.uniform(-0.15, 0.20), 2)
            pos_t = ["design"]
            neg_t = ["price"]

        ts = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 120))
        reviews.append({
            "id": str(uuid.uuid4()),
            "customer_id": c["id"],
            "product_id": p["id"],
            "rating": rating,
            "title": f"{label.capitalize()} Experience",
            "comment": comment,
            "sentiment_label": label,
            "sentiment_score": score,
            "positive_topics": ",".join(pos_t),
            "negative_topics": ",".join(neg_t),
            "timestamp": ts.isoformat()
        })

    with open(reviews_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=reviews[0].keys())
        writer.writeheader()
        writer.writerows(reviews)

    print(f"Generated {len(reviews)} reviews.")
    print("Demo dataset generation complete!")


if __name__ == "__main__":
    generate_all_datasets()
