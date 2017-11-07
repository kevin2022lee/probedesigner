"""
Django settings for MySiteWithPython project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#4h69i#vu+rd)l5cc8zrjydqv4o2u(8#&1)@oidsu0)b2igrco'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition
TEMPLATE_CONTEXT_PROCESSORS = (
#    'django.contrib.auth.context_processors.csrf',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'MyBlog',
    'django.contrib.sites',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'MySiteWithPython.urls'

WSGI_APPLICATION = 'MySiteWithPython.wsgi.application'

SESSION_COOKIE_AGE=86400
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

import os

if 'SERVER_SOFTWARE' in os.environ:
    from sae.const import (
        MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
    )
else:
    # Make `python manage.py syncdb` works happy!
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = '3306'
    MYSQL_USER = 'root'
    MYSQL_PASS = '8588027'
    MYSQL_DB   = 'app_kkds1314'

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     MYSQL_DB,
        'USER':     MYSQL_USER,
        'PASSWORD': MYSQL_PASS,
        'HOST':     MYSQL_HOST,
        'PORT':     MYSQL_PORT,
    }
}
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR,'AppData/db.sqlite'),
#        'USER': '',
#        'PASSWORD': '',
#        'HOST': '',
#        'PORT': '',
#    }
#}# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

CODEING = 'utf-8'

SITE_ID = 1

TIME_ZONE = 'Etc/GMT-8'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
HTML_URL = '/html/'

MEDIA_ROOT=os.path.join( BASE_DIR , 'static').replace('\\','/')
STATICFILES_DIRS = (
       os.path.join(BASE_DIR,'static').replace('\\','/'),
)

HTML_ROOT=os.path.join(BASE_DIR,'html').replace('\\','/')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  

EMAIL_HOST = 'smtp.163.com'  

EMAIL_PORT = 25  

EMAIL_HOST_USER='13803863098@163.com'  

EMAIL_HOST_PASSWORD='8588027   '