import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'dev-secret-key-change-me'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'subtrack',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'subtrack_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'subtrack.context_processors.currency',
            ],
        },
    },
]

WSGI_APPLICATION = 'subtrack_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
SMTP_HOST = os.environ.get('SMTP_HOST', '')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USER = os.environ.get('SMTP_USER', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
SMTP_USE_TLS = os.environ.get('SMTP_USE_TLS', 'true').strip().lower() in {'1', 'true', 'yes', 'on'}
SMTP_USE_SSL = os.environ.get('SMTP_USE_SSL', 'false').strip().lower() in {'1', 'true', 'yes', 'on'}
DEFAULT_FROM_EMAIL = os.environ.get('SMTP_FROM_EMAIL', 'no-reply@subtrack.local')
EMAIL_FAIL_SILENTLY = os.environ.get('EMAIL_FAIL_SILENTLY', 'false').strip().lower() in {
    '1',
    'true',
    'yes',
    'on',
}
CURRENCY_SYMBOL = 'MMK'
CURRENCY_PREFIX = 'MMK '

if SMTP_HOST:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = SMTP_HOST
    EMAIL_PORT = SMTP_PORT
    EMAIL_HOST_USER = SMTP_USER
    EMAIL_HOST_PASSWORD = SMTP_PASSWORD
    EMAIL_USE_TLS = SMTP_USE_TLS
    EMAIL_USE_SSL = SMTP_USE_SSL
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
