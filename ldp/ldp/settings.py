# encoding: utf-8
"""
Django settings for ldp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
import json 

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# nicked from the djangoproject website repository.
# Far too clever trick to know if we're running on the deployment server.
PRODUCTION = ('WINGDB_ACTIVE' not in os.environ)

# It's a secret to everybody
with open(os.path.join(BASE_DIR, '../secrets.json')) as handle:
    SECRETS = json.load(handle)

DEBUG = not PRODUCTION

TEMPLATE_DEBUG = DEBUG

if PRODUCTION:
    FORCE_SCRIPT_NAME = ''
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    INTERNAL_IPS = ('127.0.0.1',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': SECRETS.get('db_name', 'db.sqlite'),
        'USERNAME': SECRETS.get('db_username', ''),
        'PASSWORD': SECRETS.get('db_password', ''),
    } if PRODUCTION else { 
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite'),
        }
}

SECRET_KEY = SECRETS.get('secret_key')

ALLOWED_HOSTS = SECRETS.get('allowed_hosts', []) + ['localhost', '127.0.0.1']

ANONYMOUS_USER_ID = -1

AUTH_PROFILE_MODULE = 'skater.SkaterProfile'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'template_utils',
    'easy_thumbnails',
    'markdown_deux',
    'floppyforms',
    'foundation',
    'guardian',
    'userena',
    'skater',
    'trip',
    'flatblocks',
    'south',
    'piwik',
    'actstream',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'ldp.urls'

WSGI_APPLICATION = 'ldp.wsgi.application'

PIWIK_SITE_ID = 1
PIWIK_URL = 'http://p.adi.io/'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = ( os.path.join(BASE_DIR, 'templates'),) 

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

USERENA_REGISTER_PROFILE = False
USERENA_SIGNIN_REDIRECT_URL = '/skater/%(username)s/'
USERENA_FORBIDDEN_USERNAMES = ('signup', 'signout', 'signin', 
                               'activate', 'me', 'password') + ('a', 'admin', 'trips', 'trip', 'skater')

LOGIN_REDIRECT_URL = '/skater/%(username)s/'
LOGIN_URL = '/skater/signin/'
LOGOUT_URL = '/skater/signout/'

MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
        },
        # Allow raw HTML (WARNING: don't use this for user-generated
        # Markdown for your site!).
        "safe_mode": False,
    }
}

ACTSTREAM_SETTINGS = {
    'MODELS': ('auth.user', 'comments.comment', 'trip.Trip'),
    'USE_JSONFIELD': True,
}

