"""
Django settings for ifresnoy project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

DEBUG = True

from site_settings import *  # NOQA
import datetime

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$17%$7@*^nmx&(mb)5=o9v9if&_%s67-*^-skk!iaef3%16*12'


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'pagedown',
    'haystack',
    'elasticstack',
    'polymorphic',
    'sortedm2m',
    'django_countries',
    'django_markdown',
    'ifresnoy',
    'tastypie',
    'tastypie_swagger',
    'rest_framework',
    'corsheaders',
    'common',
    'people',
    'production',
    'diffusion',
    'school',
    'assets',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',

)

ROOT_URLCONF = 'ifresnoy.urls'

WSGI_APPLICATION = 'ifresnoy.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

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
GRAPPELLI_ADMIN_TITLE = 'iFresnoy'

# TASTYPIE/API
CORS_ORIGIN_ALLOW_ALL = True
TASTYPIE_FULL_DEBUG = DEBUG
APPEND_SLASH = False
TASTYPIE_ALLOW_MISSING_SLASH = True
TASTYPIE_DEFAULT_FORMATS = ['json']
TASTYPIE_SWAGGER_API_MODULE = 'ifresnoy.urls.v1_api'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=2),
    #'JWT_AUTH_HEADER_PREFIX': 'JWT',
}


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
