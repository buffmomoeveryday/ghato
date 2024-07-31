from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition

THIRD_PARTY = [
    "django_unicorn",
    "django_htmx",
    "template_partials",
    "django_celery_results",
    "debug_toolbar",
    "django_filters",
]


USER = [
    "purchases",
    "dashboard",
    "accounts",
    "sales",
    "analytics",
]

INSTALLED_APPS = [
    "tenant",
    "users",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # "django.contrib.staticfiles",
    "django_components",
    "django_components.safer_staticfiles",
]

INSTALLED_APPS += THIRD_PARTY
INSTALLED_APPS += USER


MIDDLEWARE = [
    "django_htmx.middleware.HtmxMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "tenant.middlewares.TenantMiddleware",
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
            os.path.join(BASE_DIR, "purchases/components"),
            os.path.join(BASE_DIR, "sales/components"),
        ],
        # "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": [
                # "slippers.templatetags.slippers",
                "django_components.templatetags.component_tags",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                        "django_components.template_loader.Loader",
                    ],
                )
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


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
    }
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
    "MINIFY_HTML": True,
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
