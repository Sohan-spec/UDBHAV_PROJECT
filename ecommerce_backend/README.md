# UDBHAV - REVA University Novelty Store

Udbhav is a premium, feature-rich, and secure E-commerce platform custom-engineered for **REVA University's Novelty Store (Bengaluru)**. Built on a robust Django backend, it features a state-of-the-art glassmorphic frontend styled using the official REVA brand identity, dynamic product catalogs, a fully-workable interactive shopping cart, a database-driven promotional gift selector, and a fortified two-level security scheme.

---

## 🎨 Brand Identity & Design System

The platform strictly complies with the official REVA University brand design guidelines to ensure an elite, academic, and premium digital experience:

* ** harmonized Brand Palette:**
  * **REVA Orange (`#ff6b00`)**: Dominates primary brand headers, call-to-actions (CTAs), primary active buttons, highlight alerts, and important links.
  * **Professional Black (`#000000`)**: Provides structural headers, borders, key navigation tabs, and solid body text contrast.
  * **Sleek White (`#ffffff`)**: Provides bright container panels, product detail backdrops, and input field bases.
  * **Accent Yellow (`#FFC107`)**: Accents highlighted texts, promotional warning stars, and active badges.
  * **Persian Green (`#0096A1`)**: Mid-tone accenting for seasonal tags, category chips, and soft banners.
  * **Sushi Green (`#85AF35`)**: Secondary accent elements and green tags.
  * **Provincial Pink (`#FDEBE7`)**: Applied as soft background radial glows, container shadows, and subtle card hover backgrounds.
* **Premium Typography:**
  * **Prata (Serif)**: Serves elegant, classic headings, topbar branding titles, and page section headers.
  * **Aleo (Sans Serif)**: Serves highly legible, contemporary body copies, dynamic descriptors, labels, and text fields.
* **Advanced Aesthetics:**
  * Consistent layout grids utilizing premium **glassmorphism** (`backdrop-filter: blur()`), translucent background gradients, card depth shadows, and interactive micro-animations.

---

## 🌟 Core Features

### 1. Unified Authentication Architecture
* **Translucent Form Modals:** Login and Registration screens styled with glassmorphism overlays and ambient REVA-brand glowing borders.
* **Dual Authorization Pipeline:**
  * **JSON REST APIs** handle frontend AJAX validations (login, cart updates, order creation) using secure **JWT (JSON Web Tokens)** stored in `localStorage`.
  * **Standard Django Page Redirects** (like `/dashboard/`) utilize authenticated Django session cookies (`sessionid`) synced during API login so page transitions are seamless.

### 2. Interactive Storefront & Real-time Search
* **Dynamic Header Search:** Submitting searches dynamically queries backend endpoints (`/api/products/?search=...`) to filter catalogs in real time.
* **Featured Deals Carousel:** Renders dynamic product cards featuring review stars, price tag displays, and automatic custom countdown clocks.
* **Dynamic Category Chips:** Active filters let shoppers narrow down catalog lists with single clicks.

### 3. Fully Workable Shopping Bag & Checkout Drawer
* **Cart Drawer Overlays:** Interactive slide-out drawer that loads items dynamically, processes stock adjustments, calculates dynamic subtotal price displays, and handles deletions.
* **Secure Checkout Flow:** Structured checkout sheets that load bag summaries, calculate shipping lines, and support Cash on Delivery (COD) and UPI radio selections.

### 4. Interactive "Pick Your Gift" Promotion
* **Promotional Dialog Trigger:** Clicking the seasonal "Pick your gifts" banner opens a beautiful custom overlay showcasing free promotional gifts (like mini skincare vials or university keyrings).
* **Database-Driven Mechanics:** The dialog queries products under category "Gifts" or priced at `₹0.00` directly from the database. Claiming a gift inserts the selected item into the user's cart at `₹0.00` and dynamically updates cart badges.

### 5. Dynamic Category Catalogs (Beds, Clothes, Electronics)
* **API-Driven Listings:** Standard category routing templates (e.g. `beds.html`) query the dynamic `/api/products/?size=100` catalog API to render live inventory databases, completely replacing legacy static placeholder lists.
* **Integrated CTAs:** Features functional add-to-cart pipelines, dynamic pricing, and individual product page transitions.

### 6. Premium Glassmorphic Admin Dashboard
* **3D Glass Visuals:** Powered by slow-floating 3D glass bubbles in the background, neon glowing radial background blobs (Orange & Persian Green), and active glow borders.
* **Dynamic Category datalist:** Integrated drop-down selectors fed directly from category databases, allowing administrators to pick from existing records or type a brand new one.
* **Local Media Upload:** Built-in standard file inputs to upload product images (`models.ImageField`) alongside detailed description textareas.
* **Balanced Responsive Grid:** Aligns inventory tables and product forms side-by-side on large screens, utilizing empty space effectively.

---

## 🛡️ Fortified Two-Level Security Framework

To secure the platform's transactions and database writes, a robust two-layer security framework is implemented:

1. **Level 1: Core System Hardening**
   * **Secure Headers:** Enabled Django's built-in secure middleware filters inside [settings.py](file:///c:/Users/rishi/UDBHAV_PROJECT/ecommerce_backend/ecommerce_backend/settings.py):
     * `SECURE_BROWSER_XSS_FILTER = True` (intercepts XSS injections)
     * `SECURE_CONTENT_TYPE_NOSNIFF = True` (prevents MIME-sniffing bypasses)
     * `X_FRAME_OPTIONS = 'DENY'` (completely blocks clickjacking attempts)
     * `CSRF_COOKIE_HTTPONLY = True` (guards CSRF cookies from client scripts)
   * **API Validation:** Rigorous schema constraints ensuring input parameters are sanitized.
2. **Level 2: Administrative Multi-Factor PIN Verification**
   * **X-Admin-Pin Interception:** Administrative product additions require a secure, custom 6-digit `Operations Security PIN` configured inside [.env](file:///c:/Users/rishi/UDBHAV_PROJECT/ecommerce_backend/.env).
   * **Endpoint Protection:** The `/api/products/create/` POST endpoint intercepts all requests, reading the `X-Admin-Pin` header. Any mismatch yields an immediate `403 Forbidden` response, rendering compromised session hijacking useless.

---

## 📁 Technical Architecture & Project Structure

The project follows clean, decoupled Django conventions:

* **`ecommerce_backend/`**: System settings and primary URL patterns.
  * `settings.py`: Contains configurations for standard SQLite database, static/media file mappings, SMTP mail, and security headers.
  * `urls.py`: Routes primary URLs and hooks dynamic local media serving during development.
* **`backend/`**: Core application logic.
  * `models.py`: Defines database schemas for `User`, `Category`, `Product`, `Cart`, `CartItem`, `Order`, `OrderItem`, and `Review`.
  * `views.py`: Controls template views, loads page headers, and seeds standard mock catalogs on initialization.
  * `api.py`: Implements REST API actions for user profiles, cart transactions, security checks, and database updates.
  * `templates/`: Implements glassmorphism UI files (homepage, detail page, cart, admin dashboard).
  * `static/`: Contains central assets (`anand-style.css`, dynamic JavaScript hooks, logo images).

---

## 🚀 Getting Started & Installation

Follow these steps to run the Udbhav storefront locally:

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### 2. Clone and Setup Environment
Navigate to your project root and create a Python virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate
```

### 3. Install Dependencies
Install all required libraries from `requirements.txt`:
```bash
pip install -r requirements.txt
```
*(This automatically installs `Django`, `PyJWT` for token authentication, `python-dotenv` for env loading, and `Pillow` for administrative image uploads).*

### 4. Configure Local Secrets
Create a secure `.env` file in the root folder (use `.env.example` as a reference):
```ini
# Operations security secondary PIN
ADMIN_SECURITY_PIN=your-strong-admin-pin-here
```

### 5. Apply Migrations & Seeding
Initialize the database tables and apply schema updates:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin Account)
To log into the Admin Dashboard, create an administrator account:
```bash
python manage.py createsuperuser
```
*Follow the prompts in your terminal to set a username, email, and password. (Note: standard superusers are automatically granted administrative permissions by the backend security filters).*

### 7. Run the Server
Launch the local development server:
```bash
python manage.py runserver
```
Open `http://127.0.0.1:8000/` in your web browser. Visiting the homepage for the first time automatically seeds your database with default featured catalog items and free promo gifts!
