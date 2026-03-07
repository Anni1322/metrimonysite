




"""
Django settings for wedding_site project.
Django 6.0
"""

import os
from pathlib import Path

# --------------------------------------------------
# BASE CONFIG
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'  # Use .env in production

DEBUG = True

ALLOWED_HOSTS = [
    
]
# CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]



EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ORGANIZATION_EMAIL = "anilwasisth@gmail.com"
EMAIL_PASSWORD = "Anni@2222"


# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'anilwasisth@gmail.com'
EMAIL_HOST_PASSWORD = 'Anni@222'


# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    # 'django.contrib.gis',        # GIS / PostGIS
    'accounts',
    'matrimony',
    'weddings',
    'biodata',
]

# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wedding_site.urls'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------
from pathlib import Path
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
            ],
        },
    },
]

WSGI_APPLICATION = 'wedding_site.wsgi.application'

# --------------------------------------------------
# DATABASE CONFIG (MULTIPLE SWITCH)
# --------------------------------------------------

# Set DB_ENGINE value:
# sqlite | mysql | postgres | postgis
DB_ENGINE = os.getenv('DB_ENGINE', 'sqlite')

# -------- SQLITE --------
if DB_ENGINE == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# -------- MYSQL --------
elif DB_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'wedding_db',
            'USER': 'root',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            }
        }
    }

# -------- POSTGRES --------
elif DB_ENGINE == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'wedding_db',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# -------- POSTGIS (DEFAULT) --------
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'wedding_db',
            'USER': 'postgres',
            'PASSWORD': 'nic',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# --------------------------------------------------
# COMMENTED DATABASE REFERENCES (FOR QUICK SWITCH)
# --------------------------------------------------

# SQLITE
# ENGINE: django.db.backends.sqlite3

# MYSQL
# ENGINE: django.db.backends.mysql

# POSTGRES
# ENGINE: django.db.backends.postgresql

# POSTGIS
# ENGINE: django.contrib.gis.db.backends.postgis

# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# STATIC & MEDIA
# --------------------------------------------------

# settings.py

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --------------------------------------------------
# DEFAULT SETTINGS
# --------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --------------------------------------------------
# CUSTOM USER MODEL
# --------------------------------------------------

AUTH_USER_MODEL = 'accounts.User'


LOGIN_URL = '/biodata/login/'
LOGIN_REDIRECT_URL = '/biodata/'
















# # """
# # Django settings for wedding_site project.

# # Generated by 'django-admin startproject' using Django 6.0.

# # For more information on this file, see
# # https://docs.djangoproject.com/en/6.0/topics/settings/

# # For the full list of settings and their values, see
# # https://docs.djangoproject.com/en/6.0/ref/settings/
# # """

# # from pathlib import Path

# # # Build paths inside the project like this: BASE_DIR / 'subdir'.
# # BASE_DIR = Path(__file__).resolve().parent.parent


# # # Quick-start development settings - unsuitable for production
# # # See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# # # SECURITY WARNING: keep the secret key used in production secret!
# # SECRET_KEY = 'django-insecure-1l%%3(^jtg+5by%51ovpzk^p=(!^dm(efv9c_&#)^bepaza5)@'

# # # SECURITY WARNING: don't run with debug turned on in production!
# # DEBUG = True

# # ALLOWED_HOSTS = []


# # # Application definition

# # INSTALLED_APPS = [
# #     'django.contrib.admin',
# #     'django.contrib.auth',
# #     'django.contrib.contenttypes',
# #     'django.contrib.sessions',
# #     'django.contrib.messages',
# #     'django.contrib.staticfiles',
# #      'accounts',
# #     'matrimony',
# #     'weddings',
# #     'django.contrib.gis',  # For geolocation (if using GIS)
# # ]

# # MIDDLEWARE = [
# #     'django.middleware.security.SecurityMiddleware',
# #     'django.contrib.sessions.middleware.SessionMiddleware',
# #     'django.middleware.common.CommonMiddleware',
# #     'django.middleware.csrf.CsrfViewMiddleware',
# #     'django.contrib.auth.middleware.AuthenticationMiddleware',
# #     'django.contrib.messages.middleware.MessageMiddleware',
# #     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# # ]

# # ROOT_URLCONF = 'wedding_site.urls'

# # TEMPLATES = [
# #     {
# #         'BACKEND': 'django.template.backends.django.DjangoTemplates',
# #         'DIRS': [],
# #         'APP_DIRS': True,
# #         'OPTIONS': {
# #             'context_processors': [
# #                 'django.template.context_processors.request',
# #                 'django.contrib.auth.context_processors.auth',
# #                 'django.contrib.messages.context_processors.messages',
# #             ],
# #         },
# #     },
# # ]

# # WSGI_APPLICATION = 'wedding_site.wsgi.application'


# # # Database
# # # https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# # DATABASES = {
# #     'default': {
# #         'ENGINE': 'django.db.backends.sqlite3',
# #         'NAME': BASE_DIR / 'db.sqlite3',
# #     }
# # }


# # # Password validation
# # # https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

# # AUTH_PASSWORD_VALIDATORS = [
# #     {
# #         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
# #     },
# #     {
# #         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
# #     },
# #     {
# #         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
# #     },
# #     {
# #         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
# #     },
# # ]


# # # Internationalization
# # # https://docs.djangoproject.com/en/6.0/topics/i18n/

# # LANGUAGE_CODE = 'en-us'

# # TIME_ZONE = 'UTC'

# # USE_I18N = True

# # USE_TZ = True


# # # Static files (CSS, JavaScript, Images)
# # # https://docs.djangoproject.com/en/6.0/howto/static-files/

# # STATIC_URL = 'static/'




















# import os
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = 'your-secret-key-here'  # Use .env for production

# DEBUG = True

# ALLOWED_HOSTS = []

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'django.contrib.gis',  # For GIS/geolocation
#     'accounts',
#     'matrimony',
#     'weddings',
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'wedding_site.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',  # Use PostGIS for GIS
#         'NAME': 'wedding_db',
#         'USER': '',
#         'PASSWORD': 'nic',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# # Database
# # https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# # DATABASES = {
# #     'default': {
# #         'ENGINE': 'django.db.backends.sqlite3',
# #         'NAME': BASE_DIR / 'db.sqlite3',
# #     }
# # }


# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# STATIC_URL = 'static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # Custom user model
# AUTH_USER_MODEL = 'accounts.User'










