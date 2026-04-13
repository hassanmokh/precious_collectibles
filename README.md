# 💎 Precious Collectibles — Backend API

> A production-ready Django REST API powering a precious metals marketplace (Gold & Silver). Built with a clean, modular app architecture, token-based authentication, live pricing, and Docker-ready deployment.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Apps & Modules](#-apps--modules)
- [API Endpoints](#-api-endpoints)
- [Authentication Flow](#-authentication-flow)
- [Data Models](#-data-models)
- [Configuration & Settings](#-configuration--settings)
- [Getting Started](#-getting-started)
  - [Local Development](#local-development)
  - [Docker](#docker)
- [Running Tests](#-running-tests)
- [Environment Variables](#-environment-variables)
- [Logging](#-logging)
- [API Documentation](#-api-documentation)

---

## 🧭 Overview

**Precious Collectibles** is a marketplace backend for gold and silver jewelry and collectibles. It provides:

- **User management** with email verification and role-based access
- **Product catalog** with metal type, karat, weight, and live pricing integration
- **Real-time pricing** for gold and silver (local buy/sell + world market)
- **Favorites, gallery, reviews, sliders, and FAQs** for a full storefront experience
- **Celery + Redis** for async task processing (email delivery, live price polling)
- **Swagger/ReDoc** API docs available in debug mode

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.11 |
| **Framework** | Django 4.x + Django REST Framework |
| **Authentication** | Knox (token-based, SHA-512) |
| **Database** | SQLite (dev) / PostgreSQL-ready (psycopg-binary) |
| **Cache / Broker** | Redis 6.2.8 (via Bitnami image) |
| **Task Queue** | Celery with Redis broker |
| **Email** | Gmail SMTP via Django's mail backend |
| **Containerisation** | Docker + Docker Compose |
| **API Docs** | drf-yasg (Swagger + ReDoc) |
| **Testing** | pytest + pytest-django + pytest-cov + mixer |
| **Filtering** | django-filter |
| **CORS** | django-cors-headers |
| **Password Reset** | django-rest-passwordreset |

---

## 📁 Project Structure

```
pcs/
├── precious_collectibles/        # Django project core
│   ├── settings/
│   │   ├── base.py               # Shared settings
│   │   ├── local.py              # Development overrides
│   │   ├── stag.py               # Staging overrides
│   │   ├── prod.py               # Production overrides
│   │   ├── test.py               # Test-specific settings
│   │   └── celery.py             # Celery app config
│   ├── urls.py                   # Root URL config
│   ├── templates/                # Global HTML templates
│   ├── wsgi.py
│   └── asgi.py
│
├── api/                          # API v1 gateway
│   ├── urls.py                   # Aggregated route table
│   ├── filters.py                # Shared DRF filter classes
│   ├── permissions.py            # Custom DRF permissions
│   ├── swagger.py                # drf-yasg schema config
│   └── tests.py
│
├── utils/                        # Shared utilities
│   ├── abstract.py               # Abstract model mixins
│   ├── choices.py                # TypeMetal enum (Gold/Silver)
│   └── validate_email.py         # AbstractAPI email validation
│
├── users/                        # Custom user model & management
├── authentication/               # Register, login, logout, verification
├── balances/                     # User wallet / balance tracking
├── brands/                       # Brand management
├── products/                     # Product catalog + photos
├── metal_types/                  # Metal type definitions
├── manufacture_fees/             # Weight-based manufacturing fees
├── pricing/                      # Live gold & silver pricing
├── charts/                       # Price history / charting data
├── favorites/                    # User product wishlists
├── gallery/                      # Media gallery
├── sliders/                      # Homepage slider banners
├── testimonies/                  # Customer reviews / testimonials
├── faqs/                         # Frequently asked questions
├── locations/                    # Governorates & cities (Egypt)
├── logs/                         # Runtime log output
│
├── Dockerfile
├── docker-compose.yml
├── Pipfile / Pipfile.lock
├── pytest.ini
└── .coveragerc
```

---

## 📦 Apps & Modules

### `utils` — Shared Abstractions
Reusable building blocks used across all apps.

| Export | Description |
|---|---|
| `AbstractTimeCreation` | Adds `created_at` to any model |
| `AbstractTimeCreateUpdate` | Adds `created_at` + `updated_at` |
| `AbstractIsDeleted` | Soft-delete flag (`is_deleted`) |
| `TypeMetal` | `IntegerChoices`: `GOLD=1`, `SILVER=2` |
| `validate_domain_email` | Validates email via AbstractAPI |

### `users` — User Model
Custom `AbstractBaseUser` extending Django's defaults with:
- Email uniqueness enforced
- Email verification via 6-digit code (expires in configurable minutes)
- Soft-delete (`is_deleted`) instead of hard deletes
- Async email dispatch via Celery (`send_email.delay`)

### `authentication` — Auth Flows
| Feature | Detail |
|---|---|
| Registration | Creates user + triggers email verification |
| Login | Returns Knox token |
| Logout | Invalidates Knox token |
| Email Verify | Validates time-limited 6-digit code |
| Resend Verification | Re-sends code email |
| Password Reset | 3-step: request → validate token → confirm |

### `products` — Product Catalog
- UUID primary keys throughout
- Links to `Brands`, `MetalTypes`, `ManufactureFees`
- `weight`, `kirat`, `fitness` fields for precise metal specs
- `is_available` / `is_popular` flags for storefront filtering
- **Soft-delete** via `is_deleted` with `.live()` custom QuerySet
- `live_photos` property returns only non-deleted photos
- On-the-fly price computation via `get_live_gold_price` / `get_live_silver_price`
- `get_manufacture_fees` fetches applicable fee by metal type + weight

### `pricing` — Live Price Engine
- Stores local `buy`/`sell` and world market `buy`/`sell` per metal type
- `old` flag marks superseded records — inserting a new entry auto-archives previous
- `Pricing.live_pricing()` always returns only the current, active prices

### `locations` — Egyptian Geography
- Governorates and Cities lookup tables
- Exposed as global lookup routes at `/api/v1/governorates/` and `/api/v1/cities/`

### `manufacture_fees` — Fee Calculator
- Fee + cashback lookup by `(metal_type, weight)`
- Used directly in product pricing computation

---

## 🌐 API Endpoints

All routes are prefixed with `/api/v1/`.

| Prefix | Module | Description |
|---|---|---|
| `auth/` | `authentication` | Register, login, logout, verify, reset password |
| `users/` | `users` | User profile management |
| `balances/` | `balances` | Wallet / balance operations |
| `metals/` | `metal_types` | Metal type catalogue |
| `brands/` | `brands` | Brand listings |
| `faqs/` | `faqs` | FAQ CRUD |
| `favorites/` | `favorites` | Wishlist management |
| `locations/` | `locations` | Location-specific routes |
| `products/` | `products` | Product catalogue |
| `testimonies/` | `testimonies` | Customer testimonials |
| `pricing/` | `pricing` | Live price data |
| `gallery/` | `gallery` | Media gallery |
| `slider/` | `sliders` | Homepage banners |
| `cities/all/` | `locations` | All cities lookup |
| `cities/create/` | `locations` | Create city |
| `governorates/all/` | `locations` | All governorates lookup |
| `governorates/create/` | `locations` | Create governorate |

> 📄 **Swagger UI** is available at `/api/v1/docs/` and **ReDoc** at `/api/v1/redoc/` — only when `DEBUG=True` (local environment).

---

## 🔐 Authentication Flow

This API uses **Knox token authentication** with SHA-512 hashing.

```
POST /api/v1/auth/register/          → Creates account, sends verification email
POST /api/v1/auth/verify/email/      → Verifies 6-digit code (expires in 10 min)
POST /api/v1/auth/verification/resend/ → Resend code
POST /api/v1/auth/login/             → Returns Knox token
POST /api/v1/auth/logout/            → Invalidates token

POST /api/v1/auth/password-reset/              → Request reset token
POST /api/v1/auth/password-reset/validate-token/ → Validate received token
POST /api/v1/auth/password-reset/confirm/      → Set new password
```

Include the token in all authenticated requests:
```http
Authorization: Token <your-knox-token>
```

Knox tokens have **no TTL** (`TOKEN_TTL = None`) and are **not auto-refreshed** — clients must explicitly logout to invalidate.

---

## 🗃 Data Models

### Key Relationships

```
User
 └── Balance (1:1)
 └── Favorites → Products

Products
 ├── Brand
 ├── MetalType
 ├── ManufactureFees  (type + weight)
 └── ProductPhotos (1:N)

Pricing
 └── type: GOLD | SILVER
 └── local_buy / local_sell
 └── world_buy / world_sell
 └── old (auto-archived on new insert)
```

### Soft Delete Pattern
Most entities use `is_deleted = BooleanField(default=False)` instead of physical deletion. Custom QuerySets expose a `.live()` method:

```python
Products.objects.live()         # is_deleted=False
ProductPhotos.objects.live()    # is_deleted=False
```

---

## ⚙️ Configuration & Settings

The settings are split by environment:

| Module | Usage |
|---|---|
| `settings/base.py` | Shared defaults (installed apps, DRF, Knox, logging, email, CORS) |
| `settings/local.py` | Development — extends base, enables `DEBUG=True` |
| `settings/stag.py` | Staging — restricted CORS headers |
| `settings/prod.py` | Production — minimal overrides |
| `settings/test.py` | Test runner — disables migrations, uses test DB |

### DRF Configuration (base.py)
- **Authentication**: Knox + Session
- **Pagination**: `LimitOffsetPagination`, `PAGE_SIZE=50`
- **Parsers**: JSON + MultiPart (for image uploads)
- **Renderers**: JSON only

### Knox Token Settings
- Hash: SHA-512
- Token length: 64 characters
- No expiry, no auto-refresh
- Token limit per user: unlimited

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11
- `pipenv` installed (`pip install pipenv`)
- Docker & Docker Compose (for containerized setup)
- Redis (for Celery — included in Docker Compose)

### Local Development

```bash
# 1. Clone the repo
git clone <repo-url>
cd pcs

# 2. Install dependencies
pipenv install --dev

# 3. Activate the virtual environment
pipenv shell

# 4. Apply migrations
python manage.py migrate --settings=precious_collectibles.settings.local

# 5. Create a superuser
python manage.py createsuperuser --settings=precious_collectibles.settings.local

# 6. Start the development server
python manage.py runserver --settings=precious_collectibles.settings.local
```

The API will be available at: **http://localhost:8000**
Swagger docs at: **http://localhost:8000/api/v1/docs/**

### Docker

The Docker Compose setup spins up three services:

| Service | Description | Port |
|---|---|---|
| `web` | Django app with auto-migrate on startup | `8000` |
| `celery` | Celery worker + beat scheduler | — |
| `redis` | Redis broker (Bitnami 6.2.8) | `6379` |

```bash
# Build and start all services
docker compose up --build

# Run in detached mode
docker compose up -d --build

# View logs
docker compose logs -f web

# Stop all services
docker compose down
```

> ⚠️ The `web` container auto-runs `makemigrations` and `migrate` on start.
> Logs are persisted to `./logs/` on the host machine.

---

## 🧪 Running Tests

Tests use **pytest** with **mixer** for factory-based fixture generation.

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov

# Run specific app tests
pytest users/
pytest products/

# Generate HTML coverage report
pytest --cov --cov-report=html
```

Coverage is configured in `.coveragerc` to omit migrations, settings, URLs, WSGI/ASGI, and test files themselves.

The test configuration (`settings/test.py`) uses `--nomigrations` to speed up test runs.

---

## 🔧 Environment Variables

The following should be configured per environment (ideally via `.env` file or secrets manager):

| Variable | Description | Default (base.py) |
|---|---|---|
| `DJANGO_SETTINGS_MODULE` | Active settings module | `precious_collectibles.settings.local` |
| `SECRET_KEY` | Django secret key | ⚠️ Hardcoded in base — **change in prod** |
| `EMAIL_HOST_USER` | SMTP sender email | `djangodeveloper123@gmail.com` |
| `EMAIL_HOST_PASSWORD` | SMTP app password | set in base.py |
| `ABSTRACT_API_KEY` | Email validation API key | set in base.py |
| `LIVE_PRICE_URL` | Live gold/silver price endpoint | `https://dahabmasr.com/...` |
| `CELERY_BROKER_URL` | Redis URL for Celery | `redis://localhost:6379` |

> 🔴 **Security Notice**: The `SECRET_KEY`, `EMAIL_HOST_PASSWORD`, and `ABSTRACT_API_KEY` are currently hardcoded in `base.py`. These **must be moved to environment variables** before any production deployment.

---

## 📋 Logging

Logging is configured in `base.py` with two outputs:

| Handler | Level | Destination |
|---|---|---|
| `console` | DEBUG | stdout |
| `file` | INFO | `logs/system.log` |
| `mail_admins` | ERROR | Email to Django admins |

The `logs/` directory is auto-created on startup and mounted as a Docker volume for persistence.

---

## 📖 API Documentation

When running locally with `DEBUG=True`:

| URL | Interface |
|---|---|
| `/api/v1/docs/` | Swagger UI |
| `/api/v1/redoc/` | ReDoc |
| `/api/v1/swagger.json/` | Raw OpenAPI JSON |

The schema is generated automatically by **drf-yasg** from DRF views and serializers.

---

## 🏗 Architecture Notes

- **Modular apps**: Each domain (products, pricing, authentication, etc.) is a self-contained Django app.
- **Shared abstractions**: The `utils/` package provides model mixins and enums used across all apps to reduce duplication.
- **Soft deletes**: Entities are never hard-deleted; `.live()` QuerySet managers filter `is_deleted=False`.
- **UUID PKs**: Products and Pricing use UUID primary keys (`uuid4`) to avoid enumeration attacks.
- **Async email**: All transactional emails go through `send_email.delay()` via Celery to avoid blocking the request cycle.
- **Live pricing**: The `Pricing` model automatically archives previous prices on insert using `force_insert`.

---

## 📄 License

This project is proprietary. All rights reserved.
