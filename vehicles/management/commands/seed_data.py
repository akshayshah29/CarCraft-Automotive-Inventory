import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
from vehicles.models import Brand, Vehicle, VehicleImage, VehicleWishlist
from products.models import ProductCategory, Product, ProductWishlist
from services.models import Service, Appointment
from orders.models import Order, OrderItem, Cart, CartItem


class Command(BaseCommand):
    help = "Seed the database with rich, realistic CarCraft dealership, inventory, products, and services data."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("==> Seeding CarCraft Database..."))

        # 1. Create Superuser & Demo User
        admin_user, _ = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@carcraft.in", "first_name": "CarCraft", "last_name": "Admin", "is_staff": True, "is_superuser": True}
        )
        admin_user.set_password("admin123")
        admin_user.save()
        admin_profile, _ = Profile.objects.get_or_create(user=admin_user)
        admin_profile.phone = "+91 98765 43210"
        admin_profile.city = "Noida"
        admin_profile.state = "Uttar Pradesh"
        admin_profile.address = "CarCraft Automotive Hub, Sector 62"
        admin_profile.pincode = "201309"
        admin_profile.save()

        demo_user, _ = User.objects.get_or_create(
            username="alex",
            defaults={"email": "alex.morgan@example.in", "first_name": "Alex", "last_name": "Morgan"}
        )
        demo_user.set_password("alex123")
        demo_user.save()
        demo_profile, _ = Profile.objects.get_or_create(user=demo_user)
        demo_profile.phone = "+91 98765 43211"
        demo_profile.address = "Flat 402, Royale Towers, Sector 62"
        demo_profile.city = "Noida"
        demo_profile.state = "Uttar Pradesh"
        demo_profile.pincode = "201309"
        demo_profile.save()

        self.stdout.write(self.style.SUCCESS("[OK] Admin ('admin'/'admin123') and Demo Customer ('alex'/'alex123') verified."))

        # 2. Seed Brands
        brands_data = [
            {
                "name": "BMW",
                "country": "Germany",
                "logo_url": "https://images.unsplash.com/photo-1555353540-64580b51c258?auto=format&fit=crop&w=400&q=80",
                "description": "Bayerische Motoren Werke AG, renowned for sheer driving pleasure and precision German engineering."
            },
            {
                "name": "Audi",
                "country": "Germany",
                "logo_url": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&w=400&q=80",
                "description": "Vorsprung durch Technik. Iconic Quattro all-wheel drive, cutting-edge technology, and sculpted luxury."
            },
            {
                "name": "Mercedes-Benz",
                "country": "Germany",
                "logo_url": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=400&q=80",
                "description": "The best or nothing. Unmatched elegance, peerless ride comfort, and world-class automotive pedigree."
            },
            {
                "name": "Porsche",
                "country": "Germany",
                "logo_url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=400&q=80",
                "description": "Timeless sports car architecture with everyday usability, racing heritage, and breathtaking handling."
            },
            {
                "name": "Toyota",
                "country": "Japan",
                "logo_url": "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?auto=format&fit=crop&w=400&q=80",
                "description": "Legendary Japanese dependability, bulletproof off-road capabilities, and benchmark hybrid innovation."
            },
            {
                "name": "Hyundai",
                "country": "South Korea",
                "logo_url": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=400&q=80",
                "description": "Progress for Humanity. Bold futuristic design language, comprehensive safety suites, and feature richness."
            },
            {
                "name": "Mahindra",
                "country": "India",
                "logo_url": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=400&q=80",
                "description": "Rugged authentic SUVs engineered for commanding road presence, high safety ratings, and effortless journeys."
            },
        ]

        brand_objs = {}
        for b_info in brands_data:
            b, _ = Brand.objects.update_or_create(
                name=b_info["name"],
                defaults={
                    "country": b_info["country"],
                    "logo_url": b_info["logo_url"],
                    "description": b_info["description"]
                }
            )
            brand_objs[b_info["name"]] = b

        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(brand_objs)} Automotive Brands."))

        # 3. Seed Vehicles (10 realistic luxury & premium vehicles)
        vehicles_data = [
            {
                "brand": brand_objs["BMW"],
                "model_name": "3 Series 330i M Sport",
                "year": 2024,
                "price": Decimal("5200000.00"),
                "fuel_type": "Petrol",
                "transmission": "Automatic",
                "body_type": "Sedan",
                "mileage": 12500,
                "engine_capacity": "2.0L TwinPower Turbo Inline-4",
                "horsepower": 255,
                "color": "Mineral Grey Metallic",
                "vin": "WBA330I202400918",
                "availability": "Available",
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=1200&q=80",
                "description": "The quintessential executive sports sedan. Featuring the M Sport dynamic handling package, variable sport steering, adaptive M suspension, and the latest BMW Curved Display with iDrive 8.5.",
                "features": "M Sport Aerodynamics Package, BMW Curved Display, 19-inch M Double-Spoke Alloys, Harman Kardon Surround Sound, Head-Up Display, Wireless Apple CarPlay & Android Auto, Adaptive LED Headlights, Wireless Charging Tray"
            },
            {
                "brand": brand_objs["Audi"],
                "model_name": "A4 Sedan 45 TFSI Quattro",
                "year": 2023,
                "price": Decimal("4600000.00"),
                "fuel_type": "Petrol",
                "transmission": "Dual-Clutch",
                "body_type": "Sedan",
                "mileage": 18200,
                "engine_capacity": "2.0L TFSI Turbocharged I4 with 12V MHEV",
                "horsepower": 261,
                "color": "Glacier White Metallic",
                "vin": "WAU45TFSI2023071",
                "availability": "Available",
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&w=1200&q=80",
                "description": "Confidence in every curve with Audi's legendary Quattro all-wheel drive. Audi Virtual Cockpit Plus, Matrix LED lighting, and acoustic acoustic glazing for supreme cabin serenity.",
                "features": "Quattro All-Wheel Drive, Audi Virtual Cockpit Plus 12.3-inch, Bang & Olufsen 3D Sound System, Panoramic Sunroof, Adaptive Cruise Control with Traffic Jam Assist, Heated Leather Sport Seats, 3-Zone Climate Control"
            },
            {
                "brand": brand_objs["Mercedes-Benz"],
                "model_name": "C-Class C 300 4MATIC AMG Line",
                "year": 2024,
                "price": Decimal("5600000.00"),
                "fuel_type": "Hybrid",
                "transmission": "Automatic",
                "body_type": "Sedan",
                "mileage": 8900,
                "engine_capacity": "2.0L Turbo I4 with EQ Boost 48V Hybrid",
                "horsepower": 255,
                "color": "Obsidian Black Metallic",
                "vin": "WDD300AMG2024054",
                "availability": "Available",
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1200&q=80",
                "description": "Mini S-Class stature with cutting-edge luxury. Features a stunning portrait 11.9-inch central display, active ambient lighting with 64 colors, and AMG Line styling.",
                "features": "11.9-inch Portrait Center Display, 64-Color Ambient Lighting, AMG Bodystyling, Panoramic Sliding Sunroof, Burmester 3D Surround Audio, Active Lane Keeping Assist, 360-degree Surround Camera"
            },
            {
                "brand": brand_objs["Porsche"],
                "model_name": "Taycan 4S Cross Turismo",
                "year": 2023,
                "price": Decimal("16500000.00"),
                "fuel_type": "Electric",
                "transmission": "Automatic",
                "body_type": "Coupe",
                "mileage": 14000,
                "engine_capacity": "Dual Permanent Magnet Synchronous Motors",
                "horsepower": 522,
                "color": "Frozen Blue Metallic",
                "vin": "WP0AA2Y14PSA1102",
                "availability": "Available",
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&w=1200&q=80",
                "description": "Pure electric soul wrapped in an adventurous shooting-brake silhouette. 800-volt architecture capable of charging 5% to 80% in 22 minutes.",
                "features": "Performance Battery Plus (93.4 kWh), Porsche Active Suspension Management (PASM), Gravel Mode Chassis Lift, 16.8-inch Curved Gauge Cluster, Passenger Interactive Display, Sport Chrono Package"
            },
            {
                "brand": brand_objs["Toyota"],
                "model_name": "Fortuner Legender 4x4",
                "year": 2024,
                "price": Decimal("4950000.00"),
                "fuel_type": "Diesel",
                "transmission": "Automatic",
                "body_type": "SUV",
                "mileage": 9500,
                "engine_capacity": "2.8L D-4D Turbo Diesel (500 Nm Torque)",
                "horsepower": 204,
                "color": "Pearl White with Contrast Black Roof",
                "vin": "AHT08FL442024099",
                "availability": "Available",
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1594502184342-2e12f877aa73?auto=format&fit=crop&w=1200&q=80",
                "description": "Unrivaled road dominance and genuine go-anywhere 4WD credentials. Catamaran-inspired styling, sharp dual-beam LED projector headlamps, and ventilated front seats.",
                "features": "Part-Time 4x4 with High/Low Range, Rear Differential Lock, Ventilated Front Seats, 11-Speaker JBL Audio System, Kick-Sensor Powered Tailgate, Wireless Phone Charger, Sequential LED Indicators"
            },
            {
                "brand": brand_objs["Hyundai"],
                "model_name": "Creta N-Line N10 Turbo",
                "year": 2024,
                "price": Decimal("2080000.00"),
                "fuel_type": "Petrol",
                "transmission": "Dual-Clutch",
                "body_type": "SUV",
                "mileage": 4200,
                "engine_capacity": "1.5L Turbo GDi Petrol Engine",
                "horsepower": 160,
                "color": "Thunder Blue with Abyss Black Roof",
                "vin": "MALC81CRN2024012",
                "availability": "Available",
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1200&q=80",
                "description": "Motorsport-inspired dynamic crossover featuring tuned suspension, throaty twin-tip sports exhaust, 18-inch diamond-cut alloy wheels, and Level 2 ADAS active safety.",
                "features": "Twin-Tip Sports Exhaust, Hyundai SmartSense Level 2 ADAS (19 Safety Features), Dual 10.25-inch Curved Screens, Panoramic Sunroof, Dual-Zone Climate Control, Bose Premium 8-Speaker Audio"
            },
            {
                "brand": brand_objs["Mahindra"],
                "model_name": "XUV700 AX7 Luxury AWD",
                "year": 2023,
                "price": Decimal("2650000.00"),
                "fuel_type": "Diesel",
                "transmission": "Automatic",
                "body_type": "SUV",
                "mileage": 21000,
                "engine_capacity": "2.2L mHawk Turbocharged Diesel (450 Nm)",
                "horsepower": 185,
                "color": "Midnight Black",
                "vin": "MA1XUV7002023901",
                "availability": "Available",
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=1200&q=80",
                "description": "Flagship 7-seater SUV with intelligent All-Wheel Drive, Skyroof, ADAS Level 2 safety suite, Sony 3D Immersive audio, and smart door handles.",
                "features": "Smart ClearView ADAS Suite, Sony 12-Speaker 3D Immersive Sound, Panoramic Skyroof, Flush Smart Door Handles, Electronic Parking Brake with Auto Hold, Blind View Monitor, Alexa Built-in"
            },
            {
                "brand": brand_objs["BMW"],
                "model_name": "M4 Competition Coupe",
                "year": 2024,
                "price": Decimal("14800000.00"),
                "fuel_type": "Petrol",
                "transmission": "Automatic",
                "body_type": "Coupe",
                "mileage": 6200,
                "engine_capacity": "3.0L M TwinPower Turbo Inline-6",
                "horsepower": 503,
                "color": "Isle of Man Green",
                "vin": "WBA4M4COMP202401",
                "availability": "Available",
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?auto=format&fit=crop&w=1200&q=80",
                "description": "Pure motorsport adrenaline. 0 to 60 mph in 3.4 seconds. Carbon bucket seats, M Carbon ceramic brakes, active M differential, and forged staggered lightweight wheels.",
                "features": "M Carbon Ceramic Brakes, Carbon Fiber Bucket Seats, M Drive Professional with Drift Analyzer, Head-Up Display with Track Mode, Adaptive M Suspension, Carbon Roof"
            },
            {
                "brand": brand_objs["Mercedes-Benz"],
                "model_name": "GLE 450 4MATIC SUV",
                "year": 2023,
                "price": Decimal("9800000.00"),
                "fuel_type": "Hybrid",
                "transmission": "Automatic",
                "body_type": "SUV",
                "mileage": 16500,
                "engine_capacity": "3.0L Turbo Inline-6 with EQ Boost",
                "horsepower": 375,
                "color": "Selenite Grey Metallic",
                "vin": "WDC167GLE2023884",
                "availability": "Available",
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?auto=format&fit=crop&w=1200&q=80",
                "description": "Exemplary comfort across all terrains. AIRMATIC air suspension with adaptive damping system, intuitive MBUX Augmented Reality navigation, and generous three-row versatility.",
                "features": "AIRMATIC Air Suspension, MBUX Augmented Reality Navigation, 360 Camera with Transparent Hood view, Burmester Sound System, Multibeam LED with Ultra Range Highbeam"
            },
            {
                "brand": brand_objs["Porsche"],
                "model_name": "911 Carrera GTS (992)",
                "year": 2024,
                "price": Decimal("22500000.00"),
                "fuel_type": "Petrol",
                "transmission": "Dual-Clutch",
                "body_type": "Coupe",
                "mileage": 3800,
                "engine_capacity": "3.0L Twin-Turbo Boxer 6-Cylinder",
                "horsepower": 473,
                "color": "Carmine Red",
                "vin": "WP0AB2A97RS12903",
                "availability": "Available",
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80",
                "description": "The quintessential benchmark sports car. GTS-specific sports chassis lowered by 10mm, sports exhaust system with black dual oval tailpipes, and center-lock lightweight wheels.",
                "features": "Sport Chrono Package, Sport Exhaust System, Center-Lock Turbo S Wheels, PASM Sport Suspension, Race-Tex Interior Package, Porsche Ceramic Composite Brake (PCCB) ready"
            }
        ]

        created_vehicles = []
        for v_data in vehicles_data:
            veh, created = Vehicle.objects.update_or_create(
                vin=v_data["vin"],
                defaults=v_data
            )
            created_vehicles.append(veh)

            # Add gallery images for rich detail page
            VehicleImage.objects.get_or_create(
                vehicle=veh,
                caption="Interior cockpit & steering",
                defaults={"image_url": "https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=800&q=80"}
            )
            VehicleImage.objects.get_or_create(
                vehicle=veh,
                caption="Rear aesthetic & dual exhaust",
                defaults={"image_url": "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=800&q=80"}
            )
            VehicleImage.objects.get_or_create(
                vehicle=veh,
                caption="Alloy wheel and high-performance braking caliper",
                defaults={"image_url": "https://images.unsplash.com/photo-1541348263662-e0c8de4259ba?auto=format&fit=crop&w=800&q=80"}
            )

        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(created_vehicles)} Vehicles with complete specs & galleries."))

        # 4. Seed Product Categories (all 8 requested)
        categories_data = [
            {"name": "Engine Parts", "image_url": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=600&q=80", "description": "High-performance spark plugs, oil filters, turbochargers, gaskets, and pistons."},
            {"name": "Brake Parts", "image_url": "https://images.unsplash.com/photo-1541348263662-e0c8de4259ba?auto=format&fit=crop&w=600&q=80", "description": "Ceramic brake pads, slotted rotors, brake fluid, and multi-piston calipers."},
            {"name": "Electrical", "image_url": "https://images.unsplash.com/photo-1558441719-798c8c5c742c?auto=format&fit=crop&w=600&q=80", "description": "High-crank batteries, alternators, ignition coils, and precision engine sensors."},
            {"name": "Exterior Accessories", "image_url": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=600&q=80", "description": "Carbon diffusers, aerodynamic spoilers, mirror caps, and roof cargo boxes."},
            {"name": "Interior Accessories", "image_url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=600&q=80", "description": "All-weather floor mats, alcantara steering wraps, ambient LED kits, and seat covers."},
            {"name": "Lighting", "image_url": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=600&q=80", "description": "Bi-LED projector bulbs, sequential turn indicators, dynamic tail lamps, and fog lights."},
            {"name": "Wheels & Tyres", "image_url": "https://images.unsplash.com/photo-1578844251758-2f71da64c96f?auto=format&fit=crop&w=600&q=80", "description": "Forged alloy wheels, ultra-high-performance track tyres, and TPMS sensors."},
            {"name": "Car Care", "image_url": "https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=600&q=80", "description": "Graphene ceramic coatings, pH-neutral snow foam, microfiber towels, and interior conditioners."},
        ]

        cat_objs = {}
        for c_data in categories_data:
            cat, _ = ProductCategory.objects.update_or_create(
                name=c_data["name"],
                defaults={
                    "image_url": c_data["image_url"],
                    "description": c_data["description"]
                }
            )
            cat_objs[c_data["name"]] = cat

        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(cat_objs)} Product Categories."))

        # 5. Seed Products (16 items across all categories)
        products_data = [
            {
                "category": cat_objs["Brake Parts"],
                "name": "Brembo GT-R Slotted Brake Rotors (Pair)",
                "part_number": "BRM-992-GTR-380",
                "brand_compatibility": "BMW M3/M4, Audi RS5, Porsche Carrera",
                "price": Decimal("85000.00"),
                "original_price": Decimal("95000.00"),
                "stock": 14,
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1541348263662-e0c8de4259ba?auto=format&fit=crop&w=800&q=80",
                "description": "High-carbon cast iron two-piece floating disc system designed for zero fade under aggressive braking and high thermal load.",
                "specifications": "Diameter: 380mm\nThickness: 34mm\nVane Type: Curved Directional Vane\nHardware: Aircraft-grade Billet Aluminum Bells"
            },
            {
                "category": cat_objs["Brake Parts"],
                "name": "Ferodo Racing DS2500 Track Brake Pads",
                "part_number": "FRD-DS2500-F",
                "brand_compatibility": "Universal Calipers (Brembo/AP Racing)",
                "price": Decimal("18500.00"),
                "original_price": Decimal("21000.00"),
                "stock": 25,
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=800&q=80",
                "description": "The gold-standard hybrid track and street friction material. Consistent friction coefficient from cold up to 500°C.",
                "specifications": "Friction Coeff: 0.42\nOperating Temp: 20°C - 500°C\nLow Dust Compound\nIncludes anti-rattle shims"
            },
            {
                "category": cat_objs["Engine Parts"],
                "name": "K&N 57-Series FIPK High-Flow Cold Air Intake",
                "part_number": "KN-57-3082",
                "brand_compatibility": "BMW 330i / 430i (G20/G22 B48 Engine)",
                "price": Decimal("38900.00"),
                "original_price": Decimal("42900.00"),
                "stock": 12,
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=800&q=80",
                "description": "Guaranteed horsepower and torque gain. Free-flowing mandrel-bent aluminum intake tube with oiled cotton washable filter.",
                "specifications": "Estimated Gain: +11.2 HP @ 5400 RPM\nFilter: Washable Red Cotton Gauze\nShield: Powder-Coated Steel Heat Shield"
            },
            {
                "category": cat_objs["Engine Parts"],
                "name": "NGK Laser Iridium Spark Plugs (Set of 4)",
                "part_number": "NGK-SILZKFR8E7S",
                "brand_compatibility": "BMW, Audi, Mercedes 2.0L Turbo",
                "price": Decimal("7800.00"),
                "original_price": Decimal("9500.00"),
                "stock": 48,
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1558441719-798c8c5c742c?auto=format&fit=crop&w=800&q=80",
                "description": "OEM replacement laser-welded iridium center electrode with platinum ground electrode for optimal spark efficiency and fuel economy.",
                "specifications": "Thread: 14mm\nReach: 26.5mm\nHex: 16mm\nPre-gapped: 0.8mm"
            },
            {
                "category": cat_objs["Electrical"],
                "name": "Bosch S6 High Performance AGM Car Battery",
                "part_number": "BSH-S6585B",
                "brand_compatibility": "Universal European Luxury Fitment (Group 49/H8)",
                "price": Decimal("24500.00"),
                "original_price": Decimal("28000.00"),
                "stock": 18,
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1558441719-798c8c5c742c?auto=format&fit=crop&w=800&q=80",
                "description": "Absorbent Glass Mat (AGM) technology engineered to power high-demand start-stop systems, climate controls, and high-end car audio.",
                "specifications": "Cold Cranking Amps: 850 CCA\nReserve Capacity: 160 mins\nCapacity: 92 Ah\nWarranty: 4-Year Full Replacement"
            },
            {
                "category": cat_objs["Lighting"],
                "name": "Osram Night Breaker 220 H7 Laser Bulbs (Pair)",
                "part_number": "OSR-64210NB220",
                "brand_compatibility": "Universal H7 Headlight Sockets",
                "price": Decimal("4999.00"),
                "original_price": Decimal("5999.00"),
                "stock": 60,
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=800&q=80",
                "description": "Up to 220% more brightness compared to legal minimum standards. Provides beam reach up to 150 meters for early hazard detection.",
                "specifications": "Socket: H7\nVoltage: 12V\nWattage: 55W\nColor Temp: Up to 3900 Kelvin"
            },
            {
                "category": cat_objs["Exterior Accessories"],
                "name": "Dry Carbon Fiber M-Style Rear Trunk Spoiler",
                "part_number": "CC-CF-SPL-G20",
                "brand_compatibility": "BMW 3 Series G20 Sedan (2019-2024)",
                "price": Decimal("32000.00"),
                "original_price": Decimal("38000.00"),
                "stock": 8,
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=800&q=80",
                "description": "100% pre-preg dry carbon fiber finished in UV-resistant glossy clear coat. Mounts seamlessly via genuine 3M automotive acrylic foam tape.",
                "specifications": "Material: 2x2 Weave Pre-Preg Dry Carbon\nWeight: 420 grams\nFinish: UV Protective Clear Gloss\nInstallation: No drilling required"
            },
            {
                "category": cat_objs["Exterior Accessories"],
                "name": "Thule Motion XT XL Aerodynamic Roof Cargo Box",
                "part_number": "THU-629801",
                "brand_compatibility": "Fits all crossbars (Thule, Yakima, OEM)",
                "price": Decimal("95000.00"),
                "original_price": Decimal("105000.00"),
                "stock": 6,
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=800&q=80",
                "description": "Optimized design for best space efficiency, aerodynamics, and vehicle fit. Dual-side opening with PowerClick quick-mount system.",
                "specifications": "Volume: 500 Liters\nLoad Capacity: 75 kg\nDimensions: 215 x 91.5 x 44 cm\nWeight: 23.5 kg"
            },
            {
                "category": cat_objs["Interior Accessories"],
                "name": "Custom 3D All-Weather Floor Mats (Full Set)",
                "part_number": "MAT-3D-PRO-01",
                "brand_compatibility": "Laser-measured for BMW / Mercedes / Audi Models",
                "price": Decimal("12500.00"),
                "original_price": Decimal("15000.00"),
                "stock": 35,
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80",
                "description": "High-walled laser-scanned thermoplastic elastomer floor liners that contain mud, snow, spills, and sand with zero slippage.",
                "specifications": "Material: Eco-friendly Odorless TPE\nLayers: 3-Ply Waterproof Core\nCoverage: Front, Rear & Central Hump"
            },
            {
                "category": cat_objs["Interior Accessories"],
                "name": "Alcantara & Carbon Sport Steering Wheel Trim",
                "part_number": "STR-ALC-M01",
                "brand_compatibility": "Audi A4 / S4 / RS4 B9 Platform",
                "price": Decimal("21000.00"),
                "original_price": Decimal("25000.00"),
                "stock": 10,
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=800&q=80",
                "description": "Hand-stitched genuine Italian Alcantara with matching motorsport burnt-orange center 12-o'clock stripe and real carbon fiber bezel.",
                "specifications": "Material: Genuine Italian Alcantara & Toray Carbon\nStitching: Burnt Orange Contrast\nFeel: Sweat-resistant High Grip"
            },
            {
                "category": cat_objs["Wheels & Tyres"],
                "name": "BBS FI-R Ultralight Forged Monobloc 19x9.5",
                "part_number": "BBS-FIR-1995-5112",
                "brand_compatibility": "5x112 Bolt Pattern (BMW G20, Audi B9)",
                "price": Decimal("210000.00"),
                "original_price": Decimal("235000.00"),
                "stock": 8,
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1578844251758-2f71da64c96f?auto=format&fit=crop&w=800&q=80",
                "description": "The pinnacle of wheel engineering. Features relief-drilled channels directly through the spokes to reduce unsprung rotational weight.",
                "specifications": "Size: 19 x 9.5J ET25\nBolt Pattern: 5x112\nWeight: Only 7.7 kg per wheel\nFinish: Satin Titanium"
            },
            {
                "category": cat_objs["Wheels & Tyres"],
                "name": "Michelin Pilot Sport 4S Tyre (255/35 ZR19)",
                "part_number": "MCH-PS4S-2553519",
                "brand_compatibility": "Universal 19-inch performance wheels",
                "price": Decimal("31500.00"),
                "original_price": Decimal("34500.00"),
                "stock": 20,
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1578844251758-2f71da64c96f?auto=format&fit=crop&w=800&q=80",
                "description": "Maximum combined performance in dry and wet handling. Bi-compound technology providing extreme grip and extended tread endurance.",
                "specifications": "Speed Rating: Y (up to 300 km/h)\nLoad Index: 96Y XL\nUTQG: 300 AA A\nRim Protector Flange"
            },
            {
                "category": cat_objs["Car Care"],
                "name": "CarCraft Apex 10H Graphene Ceramic Coating Kit",
                "part_number": "CC-APEX-GR-50",
                "brand_compatibility": "All automotive paint, glass, and chrome surfaces",
                "price": Decimal("12999.00"),
                "original_price": Decimal("15999.00"),
                "stock": 40,
                "is_featured": True,
                "image_url": "https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=800&q=80",
                "description": "True 10H hardness infused with reduced graphene oxide matrix. Unmatched hydrophobic contact angle, swirl resistance, and deep mirror gloss for 5 years.",
                "specifications": "Volume: 50ml Bottle\nHardness: 10H Pencil Scale\nDurability: Up to 5+ Years\nIncludes: Applicator Block, 5 Suede Cloths, Prep Spray"
            },
            {
                "category": cat_objs["Car Care"],
                "name": "Chemical Guys Mr. Pink Super Suds Car Wash (1 Gal)",
                "part_number": "CG-CWS402-128",
                "brand_compatibility": "Safe for ceramic coatings, wraps, and waxes",
                "price": Decimal("3999.00"),
                "original_price": Decimal("4800.00"),
                "stock": 50,
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=800&q=80",
                "description": "High-foaming surface cleanser that creates billions of lubricating suds to lift and guide dirt away from delicate clear coats safely.",
                "specifications": "Volume: 1 Gallon (128 oz)\nFormula: pH-balanced biodegradable\nApplication: Foam Cannon or 2-Bucket Wash"
            },
            {
                "category": cat_objs["Electrical"],
                "name": "Vantrue N4 Pro 3-Channel 4K Voice Control Dash Cam",
                "part_number": "VAN-N4PRO-4K",
                "brand_compatibility": "Universal 12V/24V vehicles",
                "price": Decimal("29999.00"),
                "original_price": Decimal("35999.00"),
                "stock": 15,
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1558441719-798c8c5c742c?auto=format&fit=crop&w=800&q=80",
                "description": "Triple-lens 4K Sony STARVIS 2 camera covering front, interior cabin, and rear. 24/7 buffered parking mode with 5GHz Wi-Fi and GPS.",
                "specifications": "Resolution: Front 4K + Cabin 1080P + Rear 1080P\nSensor: Dual Sony STARVIS 2 IMX678\nStorage: Up to 512GB MicroSD support"
            },
            {
                "category": cat_objs["Lighting"],
                "name": "Dynamic OLED Smoke Matrix LED Tail Lights",
                "part_number": "LGT-OLED-F30-SMK",
                "brand_compatibility": "BMW 3 Series F30 / F80 M3 (2012-2018)",
                "price": Decimal("48000.00"),
                "original_price": Decimal("56000.00"),
                "stock": 7,
                "is_featured": False,
                "image_url": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=800&q=80",
                "description": "GTS dragon-scale OLED styling with startup scanning light animation and progressive sweeping sequential amber indicators.",
                "specifications": "Style: GTS OLED Dragon Scale\nPlug & Play: Direct OEM Harness fitment\nCertifications: SAE & DOT compliant"
            }
        ]

        created_products = []
        for p_data in products_data:
            prod, _ = Product.objects.update_or_create(
                part_number=p_data["part_number"],
                defaults=p_data
            )
            created_products.append(prod)

        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded {len(created_products)} Genuine Products."))

        # 6. Seed Services (All 8 mandatory services)
        services_data = [
            {
                "name": "General Service",
                "tagline": "Comprehensive 60-point mechanical and safety inspection.",
                "description": "A thorough health check for your vehicle covering engine diagnostics, fluid top-ups, suspension inspection, brake safety tests, and a computer system scan.",
                "price": Decimal("4999.00"),
                "duration": "2 - 3 Hours",
                "icon_class": "bi-wrench-adjustable",
                "image_url": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=800&q=80",
                "what_is_included": "Comprehensive 60-Point Vehicle Inspection\nEngine Oil Level & Quality Inspection\nCoolant, Brake & Power Steering Fluid Top-Up\nAir Filter & Cabin Filter Inspection\nBattery Voltage & Health Test\nUnderbody Chassis & Suspension Check\nFull Exterior Pressure Wash & Vacuum",
                "is_featured": True
            },
            {
                "name": "Oil Change",
                "tagline": "Premium synthetic engine oil replacement and OEM filter service.",
                "description": "Protect critical engine components from friction and thermal breakdown with factory-approved full synthetic oils (Mobil 1, Castrol Edge, or Motul) and OEM filters.",
                "price": Decimal("2999.00"),
                "duration": "45 Minutes",
                "icon_class": "bi-droplet-half",
                "image_url": "https://images.unsplash.com/photo-1613214149922-f1809c99b414?auto=format&fit=crop&w=800&q=80",
                "what_is_included": "Drain Old Oil & Environmental Disposal\nUp to 6 Quarts Premium Full Synthetic Motor Oil\nNew OEM Specification Engine Oil Filter\nCrush Washer & Drain Plug Gasket Replacement\nMulti-Point Visual Check\nService Interval Computer Reset",
                "is_featured": True
            },
            {
                "name": "Brake Service",
                "tagline": "Precision rotor resurfacing, brake pad replacement and line flush.",
                "description": "Your safety is paramount. Our brake service guarantees factory stopping distances with precision caliper servicing, rotor inspection, and premium pad replacement.",
                "price": Decimal("5499.00"),
                "duration": "1.5 - 2 Hours",
                "icon_class": "bi-disc",
                "image_url": "https://images.unsplash.com/photo-1541348263662-e0c8de4259ba?auto=format&fit=crop&w=800&q=80",
                "what_is_included": "Brake Pad Thickness & Rotor Runout Measurement\nBrake Caliper Slide Pin Cleaning & High-Temp Lubrication\nBrake Fluid Moisture Testing & Hydraulic Pressure Check\nAnti-Squeal Paste Application\nRoad Test & Deceleration Verification",
                "is_featured": True
            },
            {
                "name": "Engine Diagnostics",
                "tagline": "OEM level ECU diagnostics, sensor calibration, and live data logging.",
                "description": "Resolve Check Engine lights, limp modes, rough idling, and fuel economy drops using manufacturer-grade diagnostic scanners (ISTA+, ODIS, Xentry).",
                "price": Decimal("2499.00"),
                "duration": "1 - 1.5 Hours",
                "icon_class": "bi-cpu",
                "image_url": "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=800&q=80",
                "what_is_included": "Full OBD-II & Proprietary ECU Fault Code Scan\nLive Sensor Parameter Analysis (Fuel Trims, O2 Sensors, Boost Pressure)\nMisfire Counter & Ignition Timing Verification\nClearing Resolved DTC Fault Codes\nDetailed Diagnostic PDF Report with Technical Recommendations",
                "is_featured": True
            },
            {
                "name": "AC Service",
                "tagline": "Refrigerant recovery, leak detection, and evaporator antibacterial cleaning.",
                "description": "Restore icy cabin cooling and eliminate foul bacterial odors with automated R134a/R1234yf recovery, vacuum testing, and compressor oil replenishment.",
                "price": Decimal("3999.00"),
                "duration": "1 - 2 Hours",
                "icon_class": "bi-snow",
                "image_url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80",
                "what_is_included": "AC System Pressure & Vent Temperature Test\nUV Dye Leak Detection Inspection\nRefrigerant Extraction & Precise Scale Re-charge\nCompressor Lubricant PAG Oil Injection\nEvaporator Core Ozone Disinfection & Deodorizing\nCabin Microfilter Inspection",
                "is_featured": True
            },
            {
                "name": "Wheel Alignment",
                "tagline": "Computerized 3D laser camber, caster, and toe angle calibration.",
                "description": "Prevent uneven tyre wear and steering drift with our ultra-precise Hunter Hawkeye 3D digital laser alignment rack.",
                "price": Decimal("1499.00"),
                "duration": "1 Hour",
                "icon_class": "bi-compass",
                "image_url": "https://images.unsplash.com/photo-1578844251758-2f71da64c96f?auto=format&fit=crop&w=800&q=80",
                "what_is_included": "Hunter 3D Laser Alignment System Sensor Setup\nFront & Rear Toe Angle Adjustment\nFront & Rear Camber Angle Calibration\nCaster Angle Inspection\nTyre Pressure & Tread Depth Inspection\nBefore-and-After Printed Alignment Geometry Spec Sheet",
                "is_featured": True
            },
            {
                "name": "Battery Service",
                "tagline": "CCA conductance testing, terminal cleaning, and charging health check.",
                "description": "Never get stranded with a dead battery. Includes computerized load testing, terminal corrosion removal, and alternator voltage regulator analysis.",
                "price": Decimal("999.00"),
                "duration": "30 - 45 Minutes",
                "icon_class": "bi-lightning-charge",
                "image_url": "https://images.unsplash.com/photo-1558441719-798c8c5c742c?auto=format&fit=crop&w=800&q=80",
                "what_is_included": "Digital Conductance Health & Cranking Capacity Test\nTerminal Post Cleaning & Anti-Corrosion Sealant Spray\nAlternator Charging Voltage & Ripple Test\nStarter Motor Amp-Draw Assessment\nBattery Registration in Car ECU (for AGM batteries)",
                "is_featured": True
            },
            {
                "name": "Periodic Maintenance",
                "tagline": "Complete factory scheduled 10,000 / 20,000 / 40,000 km service package.",
                "description": "Adheres strictly to your manufacturer warranty service schedule. Preserves resale value and optimal mechanical longevity with all scheduled fluid and filter changes.",
                "price": Decimal("8999.00"),
                "duration": "3 - 4 Hours",
                "icon_class": "bi-calendar-check",
                "image_url": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=800&q=80",
                "what_is_included": "Synthetic Engine Oil & Filter Change\nTransmission Fluid & Differential Fluid Check\nEngine Air Filter & Cabin Pollen Filter Replacement\nBrake System Inspection & Cleaning\nSpark Plug Condition Inspection\nExhaust & Fuel Lines Integrity Check\nFull Car Detailing Wash & Interior Vacuum",
                "is_featured": True
            }
        ]

        created_services = []
        for s_data in services_data:
            srv, _ = Service.objects.update_or_create(
                name=s_data["name"],
                defaults=s_data
            )
            created_services.append(srv)

        self.stdout.write(self.style.SUCCESS(f"[OK] Seeded all {len(created_services)} Mandatory Automotive Services."))

        # 7. Seed Sample Appointments for Demo User
        Appointment.objects.get_or_create(
            user=demo_user,
            vehicle_model="2023 BMW 330i M Sport",
            preferred_date=datetime.date.today() + datetime.timedelta(days=2),
            defaults={
                "service": created_services[0],  # General Service
                "vehicle_reg_number": "UP-16-CC-2024",
                "preferred_time": "09:00 AM - 11:00 AM",
                "customer_name": "Alex Morgan",
                "customer_email": "alex.morgan@example.in",
                "customer_phone": "+91 98765 43211",
                "notes": "Slight squeak from front left when going over speed bumps. Please check suspension bushings.",
                "status": "Confirmed"
            }
        )
        Appointment.objects.get_or_create(
            user=demo_user,
            vehicle_model="2024 Audi A4 45 TFSI",
            preferred_date=datetime.date.today() + datetime.timedelta(days=5),
            defaults={
                "service": created_services[1],  # Oil Change
                "vehicle_reg_number": "DL-01-AU-4589",
                "preferred_time": "02:00 PM - 04:00 PM",
                "customer_name": "Alex Morgan",
                "customer_email": "alex.morgan@example.in",
                "customer_phone": "+91 98765 43211",
                "notes": "Regular 10,000 km synthetic oil change with Castrol Edge.",
                "status": "Pending"
            }
        )

        # 8. Seed Sample Order for Demo User
        sample_order, o_created = Order.objects.get_or_create(
            user=demo_user,
            full_name="Alex Morgan",
            email="alex.morgan@example.in",
            phone="+91 98765 43211",
            address="Flat 402, Royale Towers, Sector 62",
            city="Noida",
            state="Uttar Pradesh",
            pincode="201309",
            subtotal=Decimal("97999.00"),
            tax=Decimal("11759.88"),
            total_amount=Decimal("109758.88"),
            status="Confirmed",
            defaults={"payment_status": "Paid"}
        )
        if o_created:
            OrderItem.objects.create(
                order=sample_order,
                product=created_products[0],
                product_name=created_products[0].name,
                price=created_products[0].price,
                quantity=1
            )
            OrderItem.objects.create(
                order=sample_order,
                product=created_products[12],  # Graphene coating
                product_name=created_products[12].name,
                price=created_products[12].price,
                quantity=1
            )

        # 9. Seed Wishlists for Demo User
        VehicleWishlist.objects.get_or_create(user=demo_user, vehicle=created_vehicles[0])
        VehicleWishlist.objects.get_or_create(user=demo_user, vehicle=created_vehicles[3])
        ProductWishlist.objects.get_or_create(user=demo_user, product=created_products[0])

        self.stdout.write(self.style.SUCCESS("[OK] Seeded sample appointments, orders, and wishlists for demo customer."))
        self.stdout.write(self.style.SUCCESS("==> CarCraft Database Seeding Completed Successfully!"))
