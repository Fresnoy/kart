"""
Django settings for Kart project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from kart.site_settings import * # NOQA
from kart.site_settings import DEBUG as DEBUG, BASE_DIR as BASE_DIR
import datetime
import os

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$17%$7@*^nmx&(mb)5=o9v9if&_%s67-*^-skk!iaef3%16*12'

# PASSWORD_TOKEN = r'(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})'
PASSWORD_TOKEN = r'(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})'

site_name = "Kartel"
DEFAULT_FROM_EMAIL = "Le Fresnoy <selection@lefresnoy.net>"
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.postgres',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'guardian',
    'pagedown',
    'haystack',
    # 'elasticstack',
    'polymorphic',
    'taggit',
    'taggit_serializer',
    'multiselectfield',
    'django_filters',
    'grappelli',
    'django.contrib.admin',
    'sortedm2m',
    'django_countries',
    'django_cleanup',
    'django_unused_media',
    'kart',
    'tastypie',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_framework_jwt',
    'rest_framework_jwt.blacklist',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'corsheaders',
    'common',
    'people',
    'production',
    'diffusion',
    'school',
    'assets',
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


    'corsheaders.middleware.CorsMiddleware',

)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'people', 'templates')
        ],

        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # this is default
    'guardian.backends.ObjectPermissionBackend',
)

ROOT_URLCONF = 'kart.urls'

WSGI_APPLICATION = 'kart.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

SITE_ID = 2

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)


# ADMIN CUSTOM
GRAPPELLI_ADMIN_TITLE = 'Kart'

# TASTYPIE/API
CORS_ORIGIN_ALLOW_ALL = True
TASTYPIE_FULL_DEBUG = DEBUG
APPEND_SLASH = False
TASTYPIE_ALLOW_MISSING_SLASH = True
TASTYPIE_DEFAULT_FORMATS = ['json']
TASTYPIE_SWAGGER_API_MODULE = 'kart.urls.v1_api'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoObjectPermissions',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=15),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}
REST_USE_JWT = True


# SEARCH SETTINGS
ELASTICSEARCH_INDEX_SETTINGS = {
    'settings': {
        "analysis": {
            "analyzer": {
                "ngram_analyzer": {
                    "type": "custom",
                    "tokenizer": "lowercase",
                    "filter": ["standard", "asciifolding", "worddelimiter",
                               "lowercase", "stop", "haystack_ngram"]  # , "my_snow"]
                },
                "edgengram_analyzer": {
                    "type": "custom",
                    "tokenizer": "lowercase",
                    "filter": ["standard", "asciifolding", "worddelimiter",
                               "lowercase", "stop", "haystack_edgengram"]  # , "my_snow"]
                }
            },
            "tokenizer": {
                "haystack_ngram_tokenizer": {
                    "type": "nGram",
                    "min_gram": 3,
                    "max_gram": 5,
                },
                "haystack_edgengram_tokenizer": {
                    "type": "edgeNGram",
                    "min_gram": 3,
                    "max_gram": 5,
                }
            },
            "filter": {
                "haystack_ngram": {
                    "type": "nGram",
                    "min_gram": 3,
                    "max_gram": 10
                },
                "haystack_edgengram": {
                    "type": "edgeNGram",
                    "min_gram": 3,
                    "max_gram": 10
                },
                "snowball": {
                    "type": "snowball",
                    "language": "French"
                },
                "elision": {
                    "type": "elision",
                    "articles": ["l", "m", "t", "qu", "n", "s", "j", "d"]
                },
                "stopwords": {
                    "type": "stop",
                    "stopwords": "_french_",
                    "ignore_case": True
                },
                "worddelimiter": {
                    "type": "word_delimiter"
                }
            }
        }
    }
}
