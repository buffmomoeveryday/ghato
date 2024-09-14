from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition
ALLOWED_HOSTS = [
    "127.0.0.1",
    ".buffmomo.xyz",
    "buffmomo.xyz",
    "localhost",
    ".localhost",
    "siddharthakhanal.top",
]

THIRD_PARTY = [
    "django_cotton",
    "django_unicorn",
    "template_partials",
    "django_celery_results",
    "debug_toolbar",
    "django_filters",
    "django_pandas",
    "widget_tweaks",
    "active_link",
    "compressor",
    "django_extensions",
    "django_tasks",
    "django_tasks.backends.database",
    "qr_code",
]

TASKS = {
    "default": {
        "BACKEND": "django_tasks.backends.database.DatabaseBackend",
        "ENQUEUE_ON_COMMIT": False,
    }
}


USER = [
    "purchases",
    "dashboard",
    "accounts",
    "sales",
    "analytics",
]

INSTALLED_APPS = [
    "daphne",
    "tenant",
    "users",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS += THIRD_PARTY
INSTALLED_APPS += USER


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # WHITENOISE
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # tenant middlewares
    "tenant.middlewares.APIKeyMiddleware",
    "tenant.middlewares.TenantMiddleware",
    # debug toolbar
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "core.urls"

import os

COMPONENT_TEMPLATE = [
    os.path.join(BASE_DIR, "purchase/components"),
]

INTERNAL_IPS = [
    "127.0.0.1",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "core/templates"),
            os.path.join(BASE_DIR, "accounts/components"),
            os.path.join(BASE_DIR, "analytics/components"),
            os.path.join(BASE_DIR, "core/templates"),
            os.path.join(BASE_DIR, "dashboard/components"),
            os.path.join(BASE_DIR, "purchases/components"),
            os.path.join(BASE_DIR, "sales/components"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


TENANT_LOGIN_REDIRECT = "/"
BASE_URL = "buffmomo.xyz"
AUTH_USER_MODEL = "users.CustomUser"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "core/templates/components"),
    os.path.join(BASE_DIR, "core/static"),
]

from decouple import config

DEBUG = config("DEBUG", default=False, cast=bool)
SECRET_KEY = config("SECRET_KEY")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "OPTIONS": {
            "transaction_mode": "EXCLUSIVE",
        },
    },
}


# Redis
REDIS_URL = config("REDIS_URL")

# Celery configuration
CELERY_BROKER_URL = REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Kathmandu"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
CELERY_BROKER_REDIS_URL = REDIS_URL


# settings.py
UNICORN = {
    "CACHE_ALIAS": "default",
    "MINIFY_HTML": False,
    "MINIFIED": True,
    "SERIAL": {
        "ENABLED": True,
        "TIMEOUT": 60,
    },
    "SCRIPT_LOCATION": "after",
    "MORPHER": {
        "NAME": "morphdom",
        "RELOAD_SCRIPT_ELEMENTS": True,
    },
}


THOUSAND_SEPARATOR = ","
USE_THOUSAND_SEPARATOR = True


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "core/staticfiles")
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

HUGGING_FACE_TOKEN = config("HUGGING_FACE_TOKEN")


DB_SCHEMA = {
    """
    CREATE TABLE IF NOT EXISTS "tenant_tenantmodel" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(255) NOT NULL UNIQUE, "domain" varchar(10) NOT NULL UNIQUE);
    CREATE TABLE IF NOT EXISTS "purchases_stockmovement" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" date NOT NULL, "movement_type" varchar(3) NOT NULL, "quantity" integer NOT NULL, "date" datetime NOT NULL, "description" text NULL, "product_id" bigint NOT NULL REFERENCES "purchases_product" ("id") DEFERRABLE INITIALLY DEFERRED, "tenant_id" bigint NULL REFERENCES "tenant_tenantmodel" ("id") DEFERRABLE INITIALLY DEFERRED, "created_by_id" bigint NULL REFERENCES "users_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
    CREATE TABLE IF NOT EXISTS "purchases_supplier" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" date NOT NULL, "name" varchar(100) NOT NULL, "contact_person" varchar(100) NULL, "email" varchar(254) NULL, "phone_number" varchar(15) NULL, "address" text NULL, "tenant_id" bigint NULL REFERENCES "tenant_tenantmodel" ("id") DEFERRABLE INITIALLY DEFERRED, "created_by_id" bigint NULL REFERENCES "users_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
    CREATE TABLE IF NOT EXISTS "purchases_purchaseinvoice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" date NOT NULL, "invoice_number" varchar(10) NULL, "purchase_date" datetime NOT NULL, "total_amount" decimal NOT NULL, "received_date" datetime NULL, "tenant_id" bigint NULL REFERENCES "tenant_tenantmodel" ("id") DEFERRABLE INITIALLY DEFERRED, "supplier_id" bigint NOT NULL REFERENCES "purchases_supplier" ("id") DEFERRABLE INITIALLY DEFERRED, "created_by_id" bigint NULL REFERENCES "users_customuser" ("id") DEFERRABLE INITIALLY DEFERRED, "order_date" datetime NULL);
    CREATE TABLE IF NOT EXISTS "purchases_purchaseitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" date NOT NULL, "price" decimal NOT NULL, "product_id" bigint NOT NULL REFERENCES "purchases_product" ("id") DEFERRABLE INITIALLY DEFERRED, "purchase_id" bigint NOT NULL REFERENCES "purchases_purchaseinvoice" ("id") DEFERRABLE INITIALLY DEFERRED, "tenant_id" bigint NULL REFERENCES "tenant_tenantmodel" ("id") DEFERRABLE INITIALLY DEFERRED, "quantity" integer NOT NULL, "created_by_id" bigint NULL REFERENCES "users_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
    CREATE TABLE IF NOT EXISTS "purchases_paymentmade" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" date NOT NULL, "amount" decimal NOT NULL, "payment_method" varchar(50) NOT NULL, "payment_date" datetime NOT NULL, "transaction_id" varchar(50) NOT NULL UNIQUE, "supplier_id" bigint NOT NULL REFERENCES "purchases_supplier" ("id") DEFERRABLE INITIALLY DEFERRED, "tenant_id" bigint NULL REFERENCES "tenant_tenantmodel" ("id") DEFERRABLE INITIALLY DEFERRED, "created_by_id" bigint NULL REFERENCES "users_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
    CREATE TABLE IF NOT EXISTS "accounts_account" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(255) NOT NULL, "tenant_id" bigint NULL REFERENCES "tenant_tenantmodel" ("id") DEFERRABLE INITIALLY DEFERRED, "balance" decimal NOT NULL);
    CREATE TABLE IF NOT EXISTS "accounts_bankaccount" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(255) NOT NULL, "tenant_id" bigint NULL REFERENCES "tenant_tenantmodel" ("id") DEFERRABLE INITIALLY DEFERRED, "accounttype" varchar(25) NOT NULL, "balance" decimal NOT NULL);
    CREATE TABLE IF NOT EXISTS "accounts_cashaccount" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(255) NULL, "tenant_id" bigint NULL REFERENCES "tenant_tenantmodel" ("id") DEFERRABLE INITIALLY DEFERRED, "balance" decimal NOT NULL);
    CREATE TABLE IF NOT EXISTS "purchases_unitofmeasurements" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" date NOT NULL, "name" varchar(100) NOT NULL, "tenant_id" bigint NULL REFERENCES "tenant_tenantmodel" ("id") DEFERRABLE INITIALLY DEFERRED, "field" varchar(255) NULL, "created_by_id" bigint NULL REFERENCES "users_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
    CREATE TABLE IF NOT EXISTS "sales_customer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" date NOT NULL, "first_name" varchar(50) NOT NULL, "last_name" varchar(50) NOT NULL, "email" varchar(254) NOT NULL UNIQUE, "phone_number" varchar(15) NULL, "address" text NULL, "tenant_id" bigint NULL REFERENCES "tenant_tenantmodel" ("id") DEFERRABLE INITIALLY DEFERRED, "created_by_id" bigint NULL REFERENCES "users_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
    CREATE TABLE IF NOT EXISTS "sales_paymentreceived" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" date NOT NULL, "amount" decimal NOT NULL, "payment_method" varchar(50) NOT NULL, "payment_date" datetime NOT NULL, "transaction_id" varchar(100) NOT NULL UNIQUE, "customer_id" bigint NOT NULL REFERENCES "sales_customer" ("id") DEFERRABLE INITIALLY DEFERRED, "tenant_id" bigint NULL REFERENCES "tenant_tenantmodel" ("id") DEFERRABLE INITIALLY DEFERRED, "created_by_id" bigint NULL REFERENCES "users_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
    CREATE TABLE IF NOT EXISTS "sales_sales" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" date NOT NULL, "total_amount" decimal NOT NULL, "customer_id" bigint NOT NULL REFERENCES "sales_customer" ("id") DEFERRABLE INITIALLY DEFERRED, "tenant_id" bigint NULL REFERENCES "tenant_tenantmodel" ("id") DEFERRABLE INITIALLY DEFERRED, "created_by_id" bigint NULL REFERENCES "users_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
    CREATE TABLE IF NOT EXISTS "sales_salesitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" date NOT NULL, "quantity" integer NOT NULL, "price" decimal NOT NULL, "vat" integer NOT NULL, "vat_amount" decimal GENERATED ALWAYS AS ((CAST(((CAST(((CAST(("price" * "quantity") AS NUMERIC)) * "vat") AS NUMERIC)) / 100) AS NUMERIC))) STORED, "product_id" bigint NOT NULL REFERENCES "purchases_product" ("id") DEFERRABLE INITIALLY DEFERRED, "sales_id" bigint NOT NULL REFERENCES "sales_sales" ("id") DEFERRABLE INITIALLY DEFERRED, "tenant_id" bigint NULL REFERENCES "tenant_tenantmodel" ("id") DEFERRABLE INITIALLY DEFERRED, "stock_snapshot" integer NULL, "created_by_id" bigint NULL REFERENCES "users_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
    CREATE TABLE IF NOT EXISTS "sales_salesinvoice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" date NOT NULL, "billing_address" text NOT NULL, "total_amount" decimal NOT NULL, "payment_status" varchar(20) NOT NULL, "tenant_id" bigint NULL REFERENCES "tenant_tenantmodel" ("id") DEFERRABLE INITIALLY DEFERRED, "sales_id" bigint NOT NULL UNIQUE REFERENCES "sales_sales" ("id") DEFERRABLE INITIALLY DEFERRED, "created_by_id" bigint NULL REFERENCES "users_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
    CREATE TABLE IF NOT EXISTS "purchases_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" date NOT NULL, "name" varchar(100) NOT NULL, "sku" varchar(50) NOT NULL UNIQUE, "tenant_id" bigint NULL REFERENCES "tenant_tenantmodel" ("id") DEFERRABLE INITIALLY DEFERRED, "uom_id" bigint NULL REFERENCES "purchases_unitofmeasurements" ("id") DEFERRABLE INITIALLY DEFERRED, "opening_stock" integer NULL, "stock_quantity" real NULL, "created_by_id" bigint NULL REFERENCES "users_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);
"""
}


# GRAPH_MODELS = {
#     "all_applications": True,
#     "group_models": True,
# }
# GRAPH_MODELS = {
#     "app_labels": ["myapp1", "myapp2", "auth"],
# }
