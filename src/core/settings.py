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
    "test.example.com",
]

THIRD_PARTY = [
    "django_cotton.apps.SimpleAppConfig",
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
    "qr_code",
]


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
    "jazzmin",  # jaazmin
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
            "builtins": [
                "purchases.templatetags.length_is",
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

JAZZMIN_SETTINGS = {
    "site_title": "Ghato Admin",
    "site_header": "Ghato",
    "site_brand": "Ghato",
}

# GRAPH_MODELS = {
#     "all_applications": True,
#     "group_models": True,
# }
# GRAPH_MODELS = {
#     "app_labels": ["myapp1", "myapp2", "auth"],
# }


# JAZZMIN_SETTINGS = {
#     # title of the window (Will default to current_admin_site.site_title if absent or None)
#     "site_title": "Library Admin",
#     # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
#     "site_header": "Library",
#     # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
#     "site_brand": "Library",
#     # Logo to use for your site, must be present in static files, used for brand on top left
#     "site_logo": "books/img/logo.png",
#     # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
#     "login_logo": None,
#     # Logo to use for login form in dark themes (defaults to login_logo)
#     "login_logo_dark": None,
#     # CSS classes that are applied to the logo above
#     "site_logo_classes": "img-circle",
#     # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
#     "site_icon": None,
#     # Welcome text on the login screen
#     "welcome_sign": "Welcome to the library",
#     # Copyright on the footer
#     "copyright": "Acme Library Ltd",
#     # List of model admins to search from the search bar, search bar omitted if excluded
#     # If you want to use a single search field you dont need to use a list, you can use a simple string
#     "search_model": ["auth.User", "auth.Group"],
#     # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
#     "user_avatar": None,
#     ############
#     # Top Menu #
#     ############
#     # Links to put along the top menu
#     "topmenu_links": [
#         # Url that gets reversed (Permissions can be added)
#         {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
#         # external url that opens in a new window (Permissions can be added)
#         {
#             "name": "Support",
#             "url": "https://github.com/farridav/django-jazzmin/issues",
#             "new_window": True,
#         },
#         # model admin to link to (Permissions checked against model)
#         {"model": "auth.User"},
#         # App with dropdown menu to all its models pages (Permissions checked against models)
#         {"app": "books"},
#     ],
#     #############
#     # User Menu #
#     #############
#     # Additional links to include in the user menu on the top right ("app" url type is not allowed)
#     "usermenu_links": [
#         {
#             "name": "Support",
#             "url": "https://github.com/farridav/django-jazzmin/issues",
#             "new_window": True,
#         },
#         {"model": "auth.user"},
#     ],
#     #############
#     # Side Menu #
#     #############
#     # Whether to display the side menu
#     "show_sidebar": True,
#     # Whether to aut expand the menu
#     "navigation_expanded": True,
#     # Hide these apps when generating side menu e.g (auth)
#     "hide_apps": [],
#     # Hide these models when generating side menu (e.g auth.user)
#     "hide_models": [],
#     # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
#     "order_with_respect_to": ["auth", "books", "books.author", "books.book"],
#     # Custom links to append to app groups, keyed on app name
#     "custom_links": {
#         "books": [
#             {
#                 "name": "Make Messages",
#                 "url": "make_messages",
#                 "icon": "fas fa-comments",
#                 "permissions": ["books.view_book"],
#             }
#         ]
#     },
#     # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
#     # for the full list of 5.13.0 free icon classes
#     "icons": {
#         "auth": "fas fa-users-cog",
#         "auth.user": "fas fa-user",
#         "auth.Group": "fas fa-users",
#     },
#     # Icons that are used when one is not manually specified
#     "default_icon_parents": "fas fa-chevron-circle-right",
#     "default_icon_children": "fas fa-circle",
#     #################
#     # Related Modal #
#     #################
#     # Use modals instead of popups
#     "related_modal_active": False,
#     #############
#     # UI Tweaks #
#     #############
#     # Relative paths to custom CSS/JS scripts (must be present in static files)
#     "custom_css": None,
#     "custom_js": None,
#     # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
#     "use_google_fonts_cdn": True,
#     # Whether to show the UI customizer on the sidebar
#     "show_ui_builder": False,
#     ###############
#     # Change view #
#     ###############
#     # Render out the change view as a single form, or in tabs, current options are
#     # - single
#     # - horizontal_tabs (default)
#     # - vertical_tabs
#     # - collapsible
#     # - carousel
#     "changeform_format": "horizontal_tabs",
#     # override change forms on a per modeladmin basis
#     "changeform_format_overrides": {
#         "auth.user": "collapsible",
#         "auth.group": "vertical_tabs",
#     },
#     # Add a language dropdown into the admin
#     "language_chooser": True,
# }
