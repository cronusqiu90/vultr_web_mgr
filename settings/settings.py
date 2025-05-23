"""
Django settings for settings project.

Generated by 'django-admin startproject' using Django 4.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv

load_dotenv(".env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-rrb1lud%9svbec$vi$-%!v#q_s&3)z&(0nl^+ft7($dq#uggb!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "simpleui",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_beat",
    "dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "settings.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "settings.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "data" / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True
TIME_FORMAT = "Y-m-d H:i:s"
DATE_FORMAT = "Y-m-d"
DATETIME_FORMAT = "Y-m-d H:i:s"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# celery broker 使用 sqlite
CELERY_BROKER_URL = "sqla+sqlite:///data/tasks.db"
CELERY_RESULT_BACKEND = "rpc://"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = False
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"


# d
SIMPLEUI_HOME_QUICK = False
SIMPLEUI_HOME_ACTION = False
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
SIMPLEUI_HOME_TITLE = "Dashboard"  # 首页标题
SIMPLEUI_STATIC_OFFLINE = False
SIMPLEUI_LOADING = False
SIMPLEUI_LOGIN_PARTICLES = False

SIMPLEUI_CONFIG = {
    "system_keep": True,
    "dynamic": True,
    "menus": [
        {
            "app": "auth",
            "name": "权限认证",
            "icon": "fas fa-user-shield",
            "models": [
                {"name": "用户列表", "icon": "fa fa-user", "url": "auth/user/"},
                {"name": "用户组", "icon": "fa fa-th-list", "url": "auth/group/"},
            ],
        },
    ],
}
