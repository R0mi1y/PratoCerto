import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-qsd8rbl#n!f4)s6$1q1e3ipih)9h-gd2w7607irvs)fr9nn7ki"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Django role-permissions
    "rolepermissions",
    # meus apps
    "caixas",
    "clientes",
    "garcons",
    "cozinhas",
    "pedidos",
    "pratos",
    "eventos",
    "django_cron",
    "main",
    "admin_gerente",
    #  Django all-auth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

SITE_ID = 1

#  Django all-auth
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
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

ROOT_URLCONF = "PratoCerto.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "PratoCerto.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "pratocerto",
        "USER": "root",
        "OPTIONS": {
            "sql_mode": "traditional",
        },
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "3306",
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

LANGUAGE_CODE = "pt-BR"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

LOGIN_REDIRECT_URL = "/home"
LOGOUT_REDIRECT_URL = "/accounts/login"

AUTH_USER_MODEL = 'clientes.Cliente'

ROLEPERMISSIONS_MODULE = "PratoCerto.roles"

# Configurações de emails

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "edielromily01@gmail.com"
EMAIL_HOST_PASSWORD = "pvgybzhcgmltvbhh"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# precisam estar em 2, o primeiro é o valor que será salvo no BD
# o segundo é o q vai aparecer para o usuário
# as imagens de cada um tem q estar no formato do primeiro .jpeg
AUX = {
    "Categorias": [
        ("entradas", "Entradas"),
        ("pratos_principais", "Pratos Principais"),
        ("massas_risotos", "Massas e Risotos"),
        ("sanduiches_hamburgueres", "Sanduíches e Hambúrgueres"),
        ("sobremesas", "Sobremesas"),
        ("bebidas", "Bebidas"),
        ("especiais_chef", "Especiais do Chef"),
    ],
    "pontos": {
        "indicação": 20,
        "indicado": 10,
        "por_compra": 10,
        "por_rs": 1,
    },
    "horario_abertura": "9:00",
    "horario_encerramento": "21:00",
    "data_limite_reserva": 9,
    'horario_pulo': 1, # 24 para desativar o campo horário
}
