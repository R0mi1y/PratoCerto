import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

APP_ICON = env('APP_ICON')
APP_NAME = env('APP_NAME')
BOT_NAME = env('BOT_NAME')
FORCE_SCRIPT_NAME = env("FORCE_SCRIPT_NAME")

# CRONJOBS = [
#     (env('CRON_SCHEDULE'), 'notifications.cron.send_random_motivation_notifications')
# ]

DB_CONNECTION = env('DB_CONNECTION', default='sqlite')  # Valor default para sqlite
DB_HOST = env('DB_HOST', default='127.0.0.1')
DB_PORT = env('DB_PORT', default=3306)
DB_DATABASE = env('DB_DATABASE', default='flavor_fit')
DB_USERNAME = env('DB_USERNAME', default='root')
DB_PASSWORD = env('DB_PASSWORD', default='root')

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
EMAIL_SENDER_NAME = env('EMAIL_SENDER_NAME')

if DB_CONNECTION == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DB_DATABASE,
            'USER': DB_USERNAME,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS').split(',')

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
    "pagamentos",
    #  Django all-auth
    # "django-mercadopago",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    
    'corsheaders',
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
    "allauth.account.middleware.AccountMiddleware",
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = "PratoCerto.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "PratoCerto.context_processors.global_variables",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "PratoCerto.wsgi.application"

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

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = FORCE_SCRIPT_NAME + "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

LOGIN_REDIRECT_URL = FORCE_SCRIPT_NAME + "/"
LOGOUT_REDIRECT_URL = FORCE_SCRIPT_NAME + "/clientes/home"

AUTH_USER_MODEL = 'clientes.Cliente'

ROLEPERMISSIONS_MODULE = "PratoCerto.roles"

# Configurações de emails

MEDIA_URL = FORCE_SCRIPT_NAME + "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# precisam estar em 2, o primeiro é o valor que será salvo no BD
# o segundo é o q vai aparecer para o usuário
# as imagens de cada um tem q estar no formato do primeiro .jpeg
AUX = {
    "Categorias": [
        ("entradas", "Entradas"),
        ("pratos_principais", "Pratos Principais"),
        ("massas_risotos", "Massas e Risotos"),
        ("sanduiches_hamburgueres", "Lanches"),
        ("sobremesas", "Sobremesas"),
        ("bebidas", "Bebidas"),
        ("especiais_chef", "Especiais do Chef"),
        ("frutos_do_mar", "Frutos do mar"),
        ("vegetariano", "Vegetariano"),
    ],
    "pontos": {
        "indicação": 20,
        "indicado": 10,
        "por_valor_compra": 10,
        "por_rs": 1,
        "valor_rs": 0.2,
    },
    "horario_abertura": "9:00",
    "horario_encerramento": "21:00",
    "data_limite_reserva": 9,
    'horario_pulo': 1, # 24 para desativar o campo horário
    'frete_entrega':8,
}

MERCADOPAGO_PUBLIC_KEY = "APP_USR-d3aa1835-6e08-417b-aaf1-4e7eb7623102"
MERCADOPAGO_ACCESS_TOKEN = 'APP_USR-4147311653907718-071021-d4636e2f103e1d55546819b03e8c141d-1336869796'
CLIENT_ID = '4147311653907718'
CLIENT_SECRET = 'kvAxR7bd8Xtb87ThC5CjEqpCVWbHJKy9'

CORS_ORIGIN_ALLOW_ALL = True