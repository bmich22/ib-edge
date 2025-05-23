import os
import dj_database_url
if os.path.exists("env.py"):
    import env

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = 'DEVELOPMENT' in os.environ

DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'ib-edge-5d506d674ecb.herokuapp.com'
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    'django_extensions',
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "home",
    "packages",
    "contact",
    "checkout",
    "tutoring_sessions",
    "user_profiles.apps.UserProfilesConfig",
    'crispy_forms',
    'crispy_bootstrap5',
    'storages',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "ib_edge.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "templates", "allauth"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 4

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = '/user_profile/profile/'

WSGI_APPLICATION = "ib_edge.wsgi.application"


if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    # Disabled to avoid admin/static
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY")

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

STRIPE_WH_SECRET = os.environ.get("STRIPE_WH_SECRET")

DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL', 'ib-edge@example.com')
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', DEFAULT_FROM_EMAIL)

if 'DEVELOPMENT' in os.environ:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = os.environ.get(
        'DEFAULT_FROM_EMAIL', 'ib-edge@example.com')

else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASS')
    DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
    # DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SECURE = False
