"""
Django settings for webtrust project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from collections import OrderedDict
from decouple import config, Csv


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'frontend',
    'grappelli_extras',
    'grappelli',
    'import_export',
    'adminactions',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admindocs',
    'simple_history',
    'mathfilters',

    'crispy_forms',
    'djangobower',
    'easy_thumbnails',
    'image_cropping',
    'django_extensions',
    'easy_pdf',

    'home',
    'utils',
    'backend',
    'accounts',
    'reports',
    'api',
    'travel_bridge',

    'adminlte',
    'django_user_agents',
    'constance',
    'constance.backends.database',
    'rest_framework',
    'knox',
    'django_crontab',
    'captcha',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'knox.auth.TokenAuthentication',
    ),
    'DATETIME_FORMAT': "%m/%d/%Y %H:%M:%S",
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }
#
# USER_AGENTS_CACHE = 'default'

CONSTANCE_ADDITIONAL_FIELDS = {
    'image_field': ['django.forms.ImageField', {'initial': 'cotizador/images/aseguradoras/assa.png'}],
    'aseguradora_field': ['backend.forms.AseguradoraField', {}],
    'ramo_field': ['backend.forms.RamoField', {}],
    'subramo_field': ['backend.forms.SubRamoField', {}],
    'cliente_field': ['backend.forms.ClienteField', {}],
}

CONSTANCE_CONFIG = OrderedDict([
    ('EMAIL_TRUST', ('gcarrion@trustcorreduria.com,',
                     'Lista de correos de Trust usados para las notificaciones del sistema')),
])

CONSTANCE_CONFIG_FIELDSETS = {
    'Configuración envio de reportes': ('EMAIL_TRUST', 'EMAIL_BANPRO', 'EMAIL_DEBITO_AUTOMATICO',
                                        'DIAS_DEBITO_AUTOMATICO'),
}

GRAPPELLI_SWITCH_USER = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'adminlte.middleware.PutParsingMiddleware',
    'adminlte.middleware.DeleteParsingMiddleware',
    'adminlte.middleware.JSONParsingMiddleware',
]

ROOT_URLCONF = 'webtrust.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'grappelli_extras.context_processors.applist',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'backend.context_processors.Entidades',
                'utils.context_processors.Utils',
            ],
        },
    },
]

WSGI_APPLICATION = 'webtrust.wsgi.application'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

LOGOUT_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/cotizador/"

AUTHENTICATION_BACKENDS = (
    # 'social_core.backends.github.GithubOAuth2',
    # 'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'webtrust',
        'USER': 'postgres',
        'PASSWORD': '141115',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'es-ni'

TIME_ZONE = 'America/Managua'

USE_I18N = True

USE_L10N = True

USE_TZ = False

USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'components', 'bower_components')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

GRAPPELLI_ADMIN_TITLE = 'TRUST'

from easy_thumbnails.conf import Settings as thumbnail_settings

THUMBNAIL_PROCESSORS = (
                           'image_cropping.thumbnail_processors.crop_corners',
                       ) + thumbnail_settings.THUMBNAIL_PROCESSORS

# django-bower

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'components')

# BOWER_PATH = '/usr/local/bin/bower'

BOWER_INSTALLED_APPS = ['bootstrap#4.2.1',
                        'bootstrap-select#1.13.15',
                        'bootstrap-validator#0.11.9',
                        'chart.js#2.6.0',
                        'd3#5.16.0',
                        'd3-arrays#2.5.0',
                        'datatables#1.10.19',
                        'datatables.net#1.10.20',
                        'datatables.net-bs#2.1.1',
                        'datatables.net-bs4#3.2.2',
                        'datatables.net-buttons#1.5.4',
                        'datatables.net-buttons-bs#1.5.4',
                        'eonasdan-bootstrap-datetimepicker#4.17.47',
                        'eve-raphael#0.5.0',
                        'flexslider#2.7.2',
                        'fontAwesome#5.7.0',
                        'fullcalendar#3.10.0',
                        'glyphicons#0.0.2',
                        'growl#1.3.5',
                        'inputmask#4.0.8',
                        'izimodal#1.5.1',
                        'jquery#2.1.4',
                        'jquery-mask-plugin#1.14.15',
                        'jquery-ui#1.12.1',
                        'js-beautify#1.5.10',
                        'js-xlsx#0.16.2',
                        'lodash#4.17.15',
                        'mocha#1.17.1',
                        'moment#2.24.0',
                        'morris.js#0.5.1',
                        'mustache.js#3.0.1',
                        'raphael#2.2.7',
                        'simditor#2.3.28',
                        'simditor-html#1.1.1',
                        'smartwizard#4.3.1',
                        'sweetalert2#7.33.1',
                        'tipsy#0.1.7']

# GRAPH_MODELS = {
#     'all_applications': True,
#     'group_models': True,
# }


DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 * 24  #

DATE_INPUT_FORMATS = [
    '%d/%m/%y',  # '25/10/06'
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',  # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',  # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',  # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',  # '25 October 2006', '25 October, 2006'
]

CRONJOBS = [
    ('7 * * * *', 'backend.cron.notificaciones_polizas_vencidas'),
    ('0 2 * * *', 'backend.cron.renovacion_automatica'),
    ('0 5 * * *', 'backend.cron.notificacion_pagos_por_vencer'),
    ('0 6 * * *', 'backend.cron.notificacion_pagos_vencidos'),
    ('0 1 * * *', 'backend.cron.polizas_por_vencer_30'),
    ('0 2 * * *', 'backend.cron.polizas_por_vencer_60'),
    ('0 3 * * *', 'backend.cron.polizas_por_vencer_cliente'),
    ('0 4 * * *', 'backend.cron.polizas_vencidas'),
]

TWILIO_SID = "AC0473e376e14a6e31a50034be50123e8e"
TWILIO_TOKEN = "155e060c7d78c6298e714880cedf5041"
TWILIO_PHONE_NUMBER = "+16067160455"

TRAVEL_URL = 'https://clubdeprotecciontotal.com.mx/api/banpro/'
TRAVEL_KEY = 'd2ec2eb4-8002-4957-9059-3018bd1b606e'

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# Configuración de correo
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
