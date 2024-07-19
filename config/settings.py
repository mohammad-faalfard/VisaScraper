# Import necessary modules
from pathlib import Path
import os
import environ

env = environ.Env()
environ.Env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# Set secret key for production
SECRET_KEY = os.environ.get(
    "SECRET_KEY", default="@^y_yto4ighco4+4+=b2e@g_##s@rml6!*+934$vm1!^kaz*+g"
)

# Set debug mode
DEBUG = int(os.environ.get("DEBUG", default=0))

# Set allowed hosts
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "192.168.159.128",
]

# Set installed apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app1",
]

# Set middleware settings
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

# Set root URL configuration
ROOT_URLCONF = "config.urls"

# Set template settings
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

# Set WSGI and ASGI configuration
WSGI_APPLICATION = "config.wsgi.application"
# ASGI_APPLICATION = "config.asgi.application"

# Set database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Set password validation settings

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 6,
        },
    },
]
# Set internationalization settings
prefix_default_language = False
LANGUAGE_CODE = "en"
LANGUAGES = [
    # ("fa", ("Farsi")),
    ("en", ("English")),
]
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

# Set static files settings
STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Set default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Set user model
# AUTH_USER_MODEL = "accounts.User"

# Set media settings
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR.joinpath("mediafiles"))



# Set login URL
LOGIN_URL = "/api/account/login/"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAdminUser",),

}

# Set Celery and Redis settings
# use redis database 1
CELERY_BROKER_URL = os.environ.get("BROKER_URL", "redis://redis:6379/1")
CELERY_RESULT_BACKEND = os.environ.get("RESULT_BACKEND", "redis://redis:6379/1")
CELERY_TIMEZONE = TIME_ZONE




