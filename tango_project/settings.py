"""
Django settings for tango_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#Project Path
PROJECT_PATH = BASE_DIR
TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    TEMPLATE_PATH,
    '../registration/templates/',
)

#template dir
# TEMPLATE_DIRS = [os.path.join(BASE_DIR,'templates')]
# TEMPLATE_DIRS = ('../rango/templates/',
#                 '../registration/templates/',)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$&nri+e$3!#s=f846lwhz&0v1&g+nj)b$p()mjg&i(&f#n+%#u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'registration',
    'bootstrap3',
    'rango',
)

#Enable site framework
# SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tango_project.urls'

WSGI_APPLICATION = 'tango_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        #  sqlite settings
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        # MySQL Settings
        'ENGINE'    : 'django.db.backends.mysql',
        'NAME'      : 'rangoDB',
        'USER'      : 'root',
        'PASSWORD'  : 'J4ck3Fr4nk07',
        'HOST'      :  'localhost',
        'PORT'      : '3306',

        #Other Settings
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

# LANGUAGE_CODE = 'en-us'

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

from django.utils.translation import ugettext_lazy as _
LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
)

# Definimos el procesador de contexto para i18n
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
)

# Definimos la ruta de los archivos de idiomas
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

#static dir
STATIC_PATH = os.path.join(PROJECT_PATH,'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    STATIC_PATH,
     '../rango/static/',
     '../registration/static/',
)

#
# Output emails to console for demo purposes.
#
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# This is the number of days users will have to activate their accounts after registering.
# If a user does not activate within that period, the account will remain permanently inactive
# and may be deleted by maintenance scripts provided in django-registration.
ACCOUNT_ACTIVATION_DAYS = 7


#media dir
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media') # Absolute path to the media directory

# URL to redirect user to that are not logged in
LOGIN_URL = "/accounts/login/"



