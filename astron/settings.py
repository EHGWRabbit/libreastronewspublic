"""
Django settings for astron project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from django.test.utils import ignore_warnings
ignore_warnings(message="No directory at", module="whitenoise.base").enable()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@iq=be+$llb-xp-xs#e4u6olr6ypj036y)b=rm#+nbd8176w@o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['libreastronews.herokuapp.com']
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
      # static files deploy supports
    'whitenoise',
    'django.contrib.staticfiles',
    #local
    'main.apps.MainConfig',
    'api.apps.ApiConfig',
    #downloaded
    #css framework
    'bootstrap4',
    #remove downloaded files after remove models
    'django_cleanup',
    #supports grafics and miniatures
    'easy_thumbnails',
    #captcha
    'captcha',
    #rest_framework
    'rest_framework',
    'corsheaders',
  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    #'corsheaders.middleware.CoreMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'astron.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #add context dispatcher
                'main.middlewares.astron_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'astron.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#model for permissions django
AUTH_USER_MODEL = 'main.AstroUser'


#mail modul
EMAIL_PORT = 1025

#outload files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#base url for media
MEDIA_URL = '/media/'

#aliases for thumbnails
THUMBNAIL_ALIASES = {
    '': {
        'default': {
            'size':(96, 96),
            'crop': 'scale',
        },
    },
}


THUMBNAIL_BASEDIR = 'thumbnails'

#permissions for all host support
CORS_ORIGIN_ALLOW_ALL = True 
CORS_URLS_REGEX = r'^/api/.*$'



#email
'''
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'libreastronews@gmail.com' 
EMAIL_HOST_PASSWORD = 'x326y457z628a45b'
EMAIL_PORT = 587
EMAIL_USE_TLS = True 

'''


