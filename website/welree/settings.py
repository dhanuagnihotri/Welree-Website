# Global settings for welree project.
import os
import sys

PROJECT_DIR = os.path.dirname(__file__)
WEBSITE_DIR = os.path.dirname(PROJECT_DIR)
PUBLIC_DIR = os.path.join(WEBSITE_DIR, 'public')

DEBUG = sys.platform == 'darwin'
TASTYPIE_FULL_DEBUG = DEBUG
TESTING = 'test' in sys.argv
TEMPLATE_DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# the meta nginx.conf handles this for us.
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/uploads/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django_jinja.loaders.FileSystemLoader',
    'django_jinja.loaders.AppLoader',
)
DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.jinja'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'welree.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'welree.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'welree.context_processors.processor',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

FIXTURE_DIRS = (
    os.path.join(PROJECT_DIR, 'fixtures'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'haystack',
    'gunicorn',
    'compressor',
    'django_nose',
    'django_jinja',
    'django_forms_bootstrap',
    'sorl.thumbnail',
    'welree',
    'social.apps.django_app.default',
    'tastypie',
    'tastypie_swagger',
    'markupfield',
    'adminsortable',
)
if not (DEBUG or TESTING):
    INSTALLED_APPS += (
        'raven.contrib.django',
    )

import markdown
MARKUP_FIELD_TYPES = (
    ('markdown', markdown.markdown),
)

TASTYPIE_SWAGGER_API_MODULE = 'welree.api.v1'

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
URL_PATH = ''
if DEBUG:
    SOCIAL_AUTH_FACEBOOK_KEY = '1538527306401099'
    SOCIAL_AUTH_FACEBOOK_SECRET = '91a93feed5351fa471d97b23d7ef05c0'
else:
    SOCIAL_AUTH_FACEBOOK_KEY = '1538526893067807'
    SOCIAL_AUTH_FACEBOOK_SECRET = '5482c01cacf9d877865bde102fb4d684'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SENTRY_DSN_PATH = os.path.join(WEBSITE_DIR, 'sentry.dsn')
if not os.path.exists(SENTRY_DSN_PATH):
    print "!!! WARNING SENTRY_DSN_PATH does not exist; no Sentry logging can occur !!!"
else:
    SENTRY_DSN = open(SENTRY_DSN_PATH).read().strip()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(WEBSITE_DIR, 'run', 'gunicorn.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'welree': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_DIR, 'welree.db'), # Or path to database file if using sqlite3.
        'USER': '',                             # Not used with sqlite3.
        'PASSWORD': '',                         # Not used with sqlite3.
        'HOST': '',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:{0}/run/memcached.sock'.format(WEBSITE_DIR),
    }
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJPDYLUAPY2TAV2OA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'djangostorages-welree'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1w*!f7srzy(lq%6m&y!uhz1rrl#id6qzzlqyl-i8t$rmi59+if'

JINJA2_EXTENSIONS = [
    'compressor.contrib.jinja2ext.CompressorExtension',
    'jinja2htmlcompress.SelectiveHTMLCompress',
]
COMPRESS_ENABLED = True
COMPRESS_PARSER = 'compressor.parser.LxmlParser'
import jinja2
from django_forms_bootstrap.templatetags.bootstrap_tags import as_bootstrap, as_bootstrap_inline, as_bootstrap_horizontal
jinja2.filters.FILTERS['as_bootstrap'] = as_bootstrap
jinja2.filters.FILTERS['as_bootstrap_inline'] = as_bootstrap_inline
jinja2.filters.FILTERS['as_bootstrap_horizontal'] = as_bootstrap_horizontal

if DEBUG and False:
    # Show emails in the console during developement.
    DEFAULT_FROM_EMAIL = "mrooney@gmail.com"
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    DEFAULT_FROM_EMAIL = "support@welree.com"
    EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
    EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
    EMAIL_PORT = 465
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'AKIAJ5TFOHLOCRWWP62Q'
    EMAIL_HOST_PASSWORD = 'AljcIns2RYU/kjPyHPxxtnSv1bDDGMBHB/0qUx+4lQXK'

AUTH_USER_MODEL = "welree.CustomUser"
LOGIN_URL = "login"

WEBSITE_NAME = "Welree"
from settings_deploy import SERVICES
if DEBUG:
    WEBSITE_URL = "http://local.welree.com:{}".format(SERVICES['nginx']['port'])
else:
    WEBSITE_URL = "http://dev.welree.com"

DISQUS_SECRET_KEY = "UaIHspmVvrI3e0Qx0lungWUcchma4xt738aTUs3KrFwUUMkb2lnlGNco1bJXWZLI" if DEBUG else "OIouch7retta9dXKxrTw64RmepoPB6PlJ8KpUgzRiWHuH62ltpVmx2BsgDZ6jvOE"
DISQUS_PUBLIC_KEY = "PzrHccuSRYo6f4ZwzTh3g88ZUDkWqPKsKwFsMGH2G46qWI6WhKuXC2dSWSfk4Cd1" if DEBUG else "gXbIO1RSYF9ezEXElmf1H9vNV8dxuKoGsTXTBZhNHadW4hWhuV457ARXVExtK9E6"
DISQUS_SHORTNAME = "welreeapp" if not DEBUG else "welreelocal"

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine' if not TESTING else 'haystack.backends.simple_backend.SimpleEngine',
        'URL': 'http://127.0.0.1:33102/solr/welree',
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

