from datetime import datetime
from decimal import Decimal

import environ
import pytz

env = environ.Env()

root = environ.Path(__file__) - 3
apps_root = root.path('aqua_airdrop_checker')

BASE_DIR = root()


# Base configurations
# --------------------------------------------------------------------------

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Application definition
# --------------------------------------------------------------------------

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

THIRD_PARTY_APPS = [
    'constance',
    'constance.backends.database',
]

LOCAL_APPS = [
    'aqua_airdrop_checker.airdrop',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# Middleware configurations
# --------------------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Template configurations
# --------------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('aqua_airdrop_checker', 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]


# Fixture configurations
# --------------------------------------------------------------------------

FIXTURE_DIRS = [
    root('aqua_airdrop_checker', 'fixtures'),
]


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
# --------------------------------------------------------------------------

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/
# --------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# --------------------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = root('static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

STATICFILES_DIRS = [
    root('aqua_airdrop_checker', 'assets'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = root('media')


# Rest framework configuration
# http://www.django-rest-framework.org/api-guide/settings/
# --------------------------------------------------------------------------

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# Constance
# --------------------------------------------------------------------------

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'BOOST_TRADES_COUNT': (10, 'Minimum number of trades for boost', int),
    'BOOST_CREATED_AT': (datetime(2019, 1, 1, tzinfo=pytz.UTC), 'Creation date limit for boost', datetime),

    'BASE_REWARD': (Decimal(11222), 'Reward for account without boost', Decimal),

    'PHASE_1_START': (datetime(2021, 8, 16, 10, tzinfo=pytz.UTC), 'First phase start', datetime),
    'PHASE_1_END': (datetime(2021, 9, 15, tzinfo=pytz.UTC), 'First phase end', datetime),

    'PHASE_2_START': (datetime(2021, 9, 16, 10, tzinfo=pytz.UTC), 'First phase start', datetime),
    'PHASE_2_END': (datetime(2021, 10, 16, tzinfo=pytz.UTC), 'First phase end', datetime),

    'PHASE_3_START': (datetime(2021, 10, 16, 10, tzinfo=pytz.UTC), 'First phase start', datetime),
    'PHASE_3_END': (datetime(2021, 11, 15, tzinfo=pytz.UTC), 'First phase end', datetime),

    'PHASE_4_START': (datetime(2021, 11, 16, 10, tzinfo=pytz.UTC), 'First phase start', datetime),
    'PHASE_4_END': (datetime(2021, 12, 16, tzinfo=pytz.UTC), 'First phase end', datetime),

    'PHASE_5_START': (datetime(2021, 12, 16, 10, tzinfo=pytz.UTC), 'First phase start', datetime),
    'PHASE_5_END': (datetime(2022, 1, 15, tzinfo=pytz.UTC), 'First phase end', datetime),
}

CONSTANCE_CONFIG_FIELDSETS = {
    'Boost limits': ('BOOST_TRADES_COUNT', 'BOOST_CREATED_AT'),
    'Reward config': ('BASE_REWARD', ),
    'Phases config': (
        'PHASE_1_START', 'PHASE_1_END', 'PHASE_2_START', 'PHASE_2_END',
        'PHASE_3_START', 'PHASE_3_END', 'PHASE_4_START', 'PHASE_4_END',
        'PHASE_5_START', 'PHASE_5_END',
    ),
}


HORIZON_URL = 'https://horizon.stellar.lobstr.co'
