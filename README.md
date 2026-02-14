# StyloKart

**One of the Biggest Online Shopping Platform** — A full-featured e-commerce web application built with Django.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Acknowledgment](#acknowledgment)
- [License](#license)

---

## Overview

StyloKart is a Django-based e-commerce platform that provides product catalog, user accounts, shopping cart, checkout, and order management. It supports both local development (SQLite) and production deployment on **AWS Elastic Beanstalk** with **PostgreSQL** and **Amazon S3** for media storage.

**Live project:** [http://stylokart-env.eba-pydmw3zp.ap-south-1.elasticbeanstalk.com/](http://stylokart-env.eba-pydmw3zp.ap-south-1.elasticbeanstalk.com/)

---

## Features

| Area | Features |
|------|----------|
| **Store** | Product listing, category filtering, search, price range filter, product detail with variations (color/size), reviews & ratings, product gallery |
| **Accounts** | Custom user model (email login), registration with email verification, login/logout, forgot/reset password, user dashboard, profile edit, change password, order history |
| **Cart** | Add/remove items, quantity update, cart persistence (session + user), checkout flow |
| **Orders** | Place order, PayPal integration, order confirmation, order status (New/Accepted/Completed/Cancelled), order detail & history |
| **Security** | Admin honeypot (fake admin URL), CSRF & XSS protection, secure session handling |
| **Infrastructure** | Optional PostgreSQL, optional S3 for media, SMTP for transactional emails, environment-based config |

---

## Tech Stack

- **Backend:** Django 5.2
- **Database:** SQLite (dev) / PostgreSQL (production)
- **Storage:** Local media (dev) / Amazon S3 (production)
- **Payments:** PayPal SDK (client-side integration)
- **Email:** SMTP (configurable via environment)
- **Deployment:** AWS Elastic Beanstalk (Python 3.14, Amazon Linux 2023), Gunicorn
- **Config:** `python-decouple` for `.env` and `os.environ`

### Main Dependencies

- `Django` — Web framework  
- `python-decouple` — Environment/config management  
- `Pillow` — Image handling  
- `django-storages` + `boto3` — S3 media storage  
- `psycopg2-binary` — PostgreSQL adapter  
- `gunicorn` — WSGI server  
- `django-admin-honeypot-updated-2021` — Fake admin login trap  

See `requirements.txt` for pinned versions.

---

## Project Structure

```
StyloKart/
├── manage.py
├── requirements.txt
├── .gitignore
├── .elasticbeanstalk/          # AWS EB config (deploy/aws → stylokart-env)
│   └── config.yml
├── stylokart/                   # Project package
│   ├── __init__.py
│   ├── settings.py              # Django settings (env-aware)
│   ├── urls.py                  # Root URLconf
│   ├── views.py                 # Home view
│   ├── wsgi.py
│   ├── asgi.py
│   └── static/                  # Project-level static assets
│       ├── css/                 # bootstrap, ui, custom, responsive
│       ├── js/                  # jQuery, Bootstrap, script.js
│       ├── fonts/               # Font Awesome, Roboto
│       └── images/
├── category/                    # Product categories
│   ├── models.py                # category (name, slug, description, image)
│   ├── views.py, urls.py, admin.py
│   ├── context_processors.py   # menu_links (categories in templates)
│   └── migrations/
├── accounts/                    # User auth & profile
│   ├── models.py                # Account (custom user), UserProfile
│   ├── views.py                 # register, login, activate, forgot/reset password, dashboard, orders
│   ├── urls.py, forms.py, admin.py
│   └── migrations/
├── store/                       # Products & catalog
│   ├── models.py                # Product, Variation, ReviewRating, ProductGallery
│   ├── views.py                 # store, product_detail, search, submit_review
│   ├── urls.py, forms.py, admin.py
│   └── migrations/
├── carts/                       # Shopping cart
│   ├── models.py                # Cart, CartItem (with variations)
│   ├── views.py                 # cart, add_cart, remove_cart, checkout
│   ├── urls.py, context_processors.py  # counter (cart count in templates)
│   └── migrations/
├── orders/                      # Checkout & orders
│   ├── models.py                # Payment, Order, OrderProduct
│   ├── views.py                 # place_order, payments (PayPal), order_complete
│   ├── urls.py, forms.py, admin.py
│   └── migrations/
└── templates/                   # Global templates
    ├── base.html
    ├── home.html
    ├── includes/                # navbar, footer, alerts, paypal
    ├── store/                   # store, product_detail, cart, checkout
    ├── accounts/                # login, register, dashboard, profile, orders, emails
    └── orders/                  # payments, order_complete, order_received_email
```

**Note:** Sensitive files such as `.env`, `db.sqlite3`, and `media/` are excluded from version control (see `.gitignore`). Do not commit them.

---

## Getting Started

### Prerequisites

- Python 3.10+ (project uses Python 3.14 on Elastic Beanstalk)
- pip and optional: virtualenv/venv

### 1. Clone and virtual environment

```bash
git clone <repository-url>
cd StyloKart
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment variables

Create a `.env` file in the project root (see [Configuration](#configuration)). For local run you need at least:

- `SECRET_KEY`
- `DEBUG=True`
- SMTP settings if you use registration/password reset

### 4. Database and migrations

```bash
python manage.py migrate
```

### 5. Create superuser (optional)

```bash
python manage.py createsuperuser
```

Use the **custom admin URL** in production: `/secureloginsite/` (default `/admin/` is a honeypot).

### 6. Run development server

```bash
python manage.py runserver
```

- Home: `http://127.0.0.1:8000/`
- Store: `http://127.0.0.1:8000/store/`
- Admin: `http://127.0.0.1:8000/secureloginsite/`

---

## Configuration

Settings are read from **environment variables** (e.g. on Elastic Beanstalk) or from a **`.env`** file via `python-decouple`. Do not commit `.env`.

### Required (minimal local run)

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` / `False` (default: True if omitted) |

### Email (for verification & password reset)

| Variable | Description |
|----------|-------------|
| `EMAIL_HOST` | SMTP host |
| `EMAIL_PORT` | SMTP port (integer) |
| `EMAIL_USE_TLS` | `True` / `False` |
| `EMAIL_HOST_USER` | SMTP user |
| `EMAIL_HOST_PASSWORD` | SMTP password |

### Production (optional)

When these are set, the app switches to PostgreSQL and/or S3:

**Database (PostgreSQL)**

- `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT` (default `5432`)

**Media storage (S3)**

- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_REGION_NAME`

**Hosts**

- `ALLOWED_HOSTS` is set in `settings.py` (e.g. Elastic Beanstalk host). Adjust for your domain if needed.

---

## Deployment

- **Platform:** AWS Elastic Beanstalk  
- **Region:** `ap-south-1`  
- **Application:** StyloKart  
- **Environment:** `stylokart-env`  
- **Config:** `.elasticbeanstalk/config.yml` (per-branch defaults; `main` and `deploy/aws` point to `stylokart-env`)

Set the required environment variables in the Elastic Beanstalk console (or via `.ebextensions`) for:

- `SECRET_KEY`, `DEBUG`
- `DB_*` for RDS PostgreSQL
- `AWS_*` for S3 media (if used)
- `EMAIL_*` for SMTP

Static files are collected to `static/` and served as configured (e.g. from app or via S3/CloudFront if you add that). Media in production use S3 when `AWS_STORAGE_BUCKET_NAME` is set.

---

## Acknowledgment

This project was developed as part of my learning journey in Django, inspired by the educational content of [TechWithRathan](https://www.youtube.com/@rathankumar).

While the core e-commerce structure was learned through guided instruction, the application logic refinements, feature enhancements, and full production deployment on AWS (Elastic Beanstalk, RDS PostgreSQL, and S3 for media storage) were implemented independently.

---

## License

This project is for learning and portfolio use. Adjust license as needed for your case.

---

**StyloKart** — Django E-commerce · Categories · Cart · Orders · PayPal · AWS EB
