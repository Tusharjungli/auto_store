import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai  # ✅ Import Google AI SDK

# ✅ Load Environment Variables
load_dotenv()

# ✅ Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Security Settings
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("❌ SECRET_KEY is missing. Set it in your environment.")

DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"  # Keep False in production
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# ✅ Installed Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # ✅ Custom Apps
    "auth_system",
    "cart",
    "feedback",
    "store",
    "chatbot",  # ✅ Added Chatbot App

    # ✅ Extensions & AI
    "django_extensions",  # Debugging tools
]

# ✅ Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ✅ Root URL Configuration
ROOT_URLCONF = "auto_store.urls"

# ✅ Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # ✅ Ensures Django can find template files
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cart.context_processors.cart_context",
            ],
        },
    },
]

# ✅ WSGI Application
WSGI_APPLICATION = "auto_store.wsgi.application"

# ✅ Database Configuration (Using SQLite for now)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ✅ Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ✅ Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ✅ Static & Media Files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ✅ Default Primary Key Field Type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ✅ Login Redirection
LOGIN_URL = "/auth/login/"

# ✅ Email Configuration (Move credentials to .env for security)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "your-email@gmail.com")  # 🔴 Replace in .env
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "your-app-password")  # 🔴 Replace in .env
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ✅ Pinecone AI Configuration (Move API Key to .env)
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise ValueError("❌ PINECONE_API_KEY is missing. Set it in your environment.")

PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")  # Example: "us-east-1"
PINECONE_INDEX_NAME = "auto-store-ai"

# ✅ Google Gemini AI Configuration
GENAI_API_KEY = os.getenv("GENAI_API_KEY", "your-google-api-key-here")  # 🔴 Replace in .env

# ✅ Configure Google AI with API Key
genai.configure(api_key=GENAI_API_KEY)
