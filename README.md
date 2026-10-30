# CARCRAFT — Full-Stack Automotive Inventory & Dealership Suite

![CarCraft Banner](https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=1600&q=80)

**CARCRAFT** is an enterprise-grade, modern full-stack automotive platform delivering a unified ecosystem for **luxury vehicle inventory management**, **genuine OEM spare parts & accessories e-commerce**, and **certified automotive service appointment scheduling**.

Designed with a high-end luxury aesthetic (Graphite, Charcoal, Burnt Orange accents), cinematic HTML5 video backgrounds, transparent-to-solid navbar transitions, and a rock-solid Django backend powered by MySQL.

---

## Key Features

### 1. Cinematic Video Hero & Brand Experience
- Full-viewport HTML5 video hero element (`autoplay`, `muted`, `loop`, `playsinline`, `object-fit: cover`).
- Integrated transparent navbar at load that seamlessly transitions into a frosted dark graphite bar on scroll.
- Refined automotive brand typography and 3 massive visual business panels (**Cars**, **Parts**, **Services**).

### 2. Vehicle Inventory Management (`vehicles` app)
- Real-time vehicle search across models, brands, VINs, and descriptors.
- Multi-faceted filters: Brand, Price range, Fuel type (Petrol, Diesel, Hybrid, Electric), Transmission (Automatic, Manual, Dual-Clutch), Body type (Sedan, SUV, Coupe, etc.), and Availability.
- Dynamic sorting: Price (Low to High, High to Low), Newest/Oldest year, and Mileage.
- Rich vehicle detail pages with multi-angle image galleries, technical spec matrices, factory equipment lists, and a dedicated dealership test-drive enquiry form.
- Real user wishlist integration.

### 3. Spare Parts & Accessories E-Commerce (`products` app)
- 8 Core automotive categories: *Engine Parts*, *Brake Parts*, *Electrical*, *Exterior Accessories*, *Interior Accessories*, *Lighting*, *Wheels & Tyres*, *Car Care*.
- Real-time stock status monitoring (In-Stock badges, live quantity availability).
- Product details with technical specifications, compatibility verification, and quantity selectors.

### 4. Real Django-Backed Cart & Order System (`orders` app)
- Database-backed shopping cart supporting both authenticated users and guest sessions.
- Dynamic quantity adjustment (+/-) and line-item removals.
- Automatic calculation of subtotal, 12% standard automotive goods tax, and complimentary shipping.
- Simulated checkout with recipient shipping form, order confirmation, and order history dashboard.

### 5. Certified Workshop Service Booking (`services` app)
- All 8 essential automotive services:
  1. *General Service* (60-point multi-system inspection)
  2. *Oil Change* (Full synthetic & OEM filter)
  3. *Brake Service* (Pad replacement & rotor resurfacing)
  4. *Engine Diagnostics* (OEM ECU scanner analysis)
  5. *AC Service* (R134a/R1234yf evacuation & recharge)
  6. *Wheel Alignment* (Hunter 3D laser calibration)
  7. *Battery Service* (CCA conductance & alternator test)
  8. *Periodic Maintenance* (Factory scheduled milestone service)
- Interactive appointment booking with vehicle model, plate number, date picker (guarded against past dates), and preferred time slots.
- Appointment confirmation and client history tracking with cancellation controls.

### 6. Authentication & User Profile (`accounts` app)
- Django authentication with password hashing, CSRF protection, and server-side validation.
- User registration, login, logout, and profile management with delivery address and phone numbers.
- Unified customer dashboard displaying recent orders, appointments, and saved vehicles/parts.

### 7. Staff & Dealership Administration (`carcraft` dashboard & Django Admin)
- Custom Staff Portal (`/dashboard/`) displaying 6 core dealership metrics:
  - *Total Vehicles*, *Available Vehicles*, *Total Products*, *Pending Orders*, *Pending Appointments*, *Registered Users*.
  - Live tables for recent customer orders, service bookings, showroom fleet, and critical low-stock alerts.
- Full access to Django's native administrative panel (`/admin/`).

---

## Technology Stack

- **Frontend**: HTML5, CSS3, Bootstrap 5.3.3, Bootstrap Icons 1.11.3, Vanilla JavaScript (ES6+)
- **Backend**: Python 3.13 / Django 5.2 (MVT Architecture)
- **Database**: MySQL (via PyMySQL / Django ORM) with intelligent SQLite dev fallback
- **Dependencies**: `Pillow`, `python-dotenv`, `cryptography`

---

## Project Structure

```
CarCraft/
│
├── manage.py                       # Django management utility
├── requirements.txt                # Python project dependencies
├── .env.example                    # Environment variable template
├── .env                            # Active environment configuration
├── README.md                       # Comprehensive guide
│
├── carcraft/                       # Core project orchestrator
│   ├── __init__.py                 # PyMySQL MySQLdb driver installation
│   ├── settings.py                 # MySQL database & Django settings
│   ├── urls.py                     # Global URL routing & media serving
│   ├── views.py                    # Home, search, wishlist & staff dashboard
│   ├── context_processors.py       # Dynamic navbar counts (cart, wishlist)
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                       # Authentication & Customer Profiles
│   ├── models.py                   # Profile model with auto-create signals
│   ├── forms.py                    # Registration & profile update forms
│   ├── views.py                    # Register, login, logout, profile
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── vehicles/                       # Dealership Inventory & Enquiries
│   ├── models.py                   # Brand, Vehicle, VehicleImage, VehicleWishlist, VehicleEnquiry
│   ├── views.py                    # Vehicle list, filters, sorting, detail, wishlist
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   └── management/commands/        # Seed command (seed_data.py)
│
├── products/                       # Spare Parts & Accessories E-Commerce
│   ├── models.py                   # ProductCategory, Product, ProductWishlist
│   ├── views.py                    # Catalog list, category filter, detail, wishlist
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── orders/                         # Cart, Simulated Checkout & Invoicing
│   ├── models.py                   # Cart, CartItem, Order, OrderItem
│   ├── views.py                    # Cart operations, checkout, confirmation, history
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── services/                       # Certified Workshop Appointment Scheduling
│   ├── models.py                   # Service, Appointment
│   ├── views.py                    # Services list, detail, booking, appointments
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── static/
│   ├── css/
│   │   ├── style.css               # Luxury automotive design system
│   │   └── responsive.css          # Responsive fine-tuning (mobile/tablet)
│   ├── js/
│   │   └── main.js                 # Vanilla JS: navbar scroll, AJAX wishlist, cart
│   └── video/
│       ├── README.txt              # Video placement instructions
│       └── carcraft-hero.mp4       # [Place your MP4 hero video here]
│
└── templates/
    ├── base.html                   # Master layout with video-integrated navbar & footer
    ├── home.html                   # Cinematic homepage with video hero & panels
    ├── wishlist.html               # Unified saved vehicle & parts wishlist
    ├── search_results.html         # Multi-entity global search results
    ├── 404.html & 500.html         # Error pages
    ├── accounts/                   # Register, login, profile, edit profile
    ├── vehicles/                   # Vehicle inventory & vehicle detail
    ├── products/                   # Parts catalog & product detail
    ├── orders/                     # Cart, checkout, order confirmation, history
    ├── services/                   # Services catalog, detail, booking, confirmation
    └── admin/                      # Custom Dealership Management Dashboard
```

---

## Installation & Setup Guide

### 1. Clone or Open the Workspace
Open terminal or PowerShell in the project directory:
```bash
cd CarCraft
```

### 2. Set Up Virtual Environment
Create and activate a Python virtual environment:

**Windows (PowerShell / Command Prompt):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Packages
Install Django, PyMySQL, Pillow, cryptography, and dotenv:
```bash
pip install -r requirements.txt
```

---

## Database Configuration (MySQL)

CarCraft is configured for **MySQL**.

### Setting Up MySQL:
1. Start your MySQL service (e.g. WampServer, XAMPP, or standalone MySQL).
2. Configure your credentials in the `.env` file (or set environment variables):
   ```env
   DB_NAME=carcraft_db
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   USE_SQLITE=False
   ```
3. *Note on Resilience*: If MySQL server is not currently running or reachable on your machine during development, CarCraft automatically falls back to SQLite so you can test and present without crashes. Once MySQL is started, it will seamlessly connect to MySQL.

---

## Migrations & Sample Data

### 1. Run Database Migrations
Apply all database tables for accounts, vehicles, products, orders, and services:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Populate Realistic Sample Data
Run the built-in seed command to instantly populate the database with 10 luxury vehicles, 16 genuine parts across all 8 categories, 8 automotive services, demo orders, appointments, and user accounts:
```bash
python manage.py seed_data
```

### Pre-Configured Demo Accounts:
| Role | Username | Password | Purpose |
|---|---|---|---|
| **Superuser / Staff** | `admin` | `admin123` | Full access to Django Admin & Dealership Dashboard |
| **Demo Customer** | `alex` | `alex123` | Pre-populated profile, past orders, and service bookings |

*(You can also create a new custom superuser at any time using: `python manage.py createsuperuser`)*

---

## Hero Video Setup

The homepage has been built specifically for a cinematic automotive hero video.

1. Ensure your MP4 video file is named:
   ```
   carcraft-hero.mp4
   ```
2. Place the video directly in the folder:
   ```
   static/video/carcraft-hero.mp4
   ```
3. The video will immediately play in the background behind the navbar upon loading the homepage.

---

## Running the Application

Start the Django local development server:
```bash
python manage.py runserver
```

Open your browser and navigate to:
- **Storefront & Homepage**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Vehicle Showroom**: [http://127.0.0.1:8000/cars/](http://127.0.0.1:8000/cars/)
- **Parts E-Commerce**: [http://127.0.0.1:8000/parts/](http://127.0.0.1:8000/parts/)
- **Service Center**: [http://127.0.0.1:8000/services/](http://127.0.0.1:8000/services/)
- **Staff Dealership Dashboard**: [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/) (login as `admin`)
- **Django Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Running Automated Tests

Run the complete automated test suite verifying all 5 apps:
```bash
python manage.py test
```

---

## Presentation & Viva Highlights

- **Genuine Django MVT Architecture**: Completely modular apps (`accounts`, `vehicles`, `products`, `orders`, `services`).
- **MySQL Integration**: Standard MySQL connector via PyMySQL with `.env` configuration.
- **Real Backend Cart & Checkout**: Database-backed cart persistence with subtotal, tax calculation, and order tracking.
- **Cinematic Frontend**: Custom CSS luxury styling, avoiding generic templates while leveraging responsive Bootstrap 5 and vanilla JavaScript.
- **Appointment Scheduling**: End-to-end service appointment booking with status lifecycle (`Pending`, `Confirmed`, `Completed`, `Cancelled`).
