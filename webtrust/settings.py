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

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!9*w%_k@mo0j&uvfu2f6k-l%g2h(h5&qd6uocwk-(s60)rjc&#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
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
    'frontend',
    'accounts',
    'api',

    'adminlte',
    'django_user_agents',
    'constance',
    'constance.backends.database',
    'rest_framework',
    'knox',

]

REST_FRAMEWORK = {  # added
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.AllowAny'
    # ],
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

    ('EMAIL_BANPRO', ('arlenperez@banpro.com.ni,',
                      'Lista de correos de Banpro usados para las notificaciones del sistema')),

    ('EMAIL_DEBITO_AUTOMATICO', ('ysevilla@assanet.com,pdavila@assanet.com,zvanegas@assanet.com',
                                 'Lista de correos de sepelio usados para las notificaciones de debitos automaticos')),
    ('DIAS_DEBITO_AUTOMATICO',
     ('10,20', 'Dias del mes en los que se enviará el reporte de debito automático.')),

    ('ASEGURADORA', (None, 'Aseguradora', 'aseguradora_field')),
    ('RAMO', (None, 'Ramo', 'ramo_field')),
    ('SUBRAMO', (None, 'Sub ramo', 'subramo_field')),
    ('CONTRATANTE', (None, 'Contratante', 'cliente_field')),
    ('LOGO_AUTOMOVIL', ('cotizador/images/aseguradoras/assa.png', 'Logo de la compañia de seguros de Accidentes.',
                        'image_field')),
    ('TASA_AUTOMOVIL', (10.4, 'Tarifa para el seguro de prima de vehículo')),
    ('SOA_AUTOMOVIL', (55.0, 'Tarifa para el seguro obligatorio de vehículo')),
    ('PORCENTAJE_DEDUCIBLE', (0.2,
                              'Porcentaje deducible global. Puede ir a la seccion de marcas con recargo para cambiar este valor a una marca en específico')),
    ('PORCENTAJE_DEDUCIBLE_EXTENSION_TERRITORIAL', (0.3,
                                                    'Porcentaje deducible solo para la cobertura de extensión territorial. Para aplicar regargo vaya a Marcas con recargo.')),
    ('MINIMO_DEDUCIBLE', (100.0,
                          'Mínimo deducible global. Puede ir a la seccion de marcas con recargo para cambiar este valor a una marca en específico')),
    ('SOA_DESCUENTO', (
        0.05, 'Descuento del Seguro Obligatorio de Vehículo. Por favor usar notación decimal (0.05 = 5%)')),
    ('EMAIL_AUTOMOVIL', ('gcarrion@trustcorreduria.com,',
                         'Lista de correos de automovil usados para las notificaciones del sistema')),

    ('ASEGURADORA_SEPELIO', (None, 'Aseguradora', 'aseguradora_field')),
    ('RAMO_SEPELIO', (None, 'Ramo', 'ramo_field')),
    ('SUBRAMO_SEPELIO', (None, 'Sub ramo', 'subramo_field')),
    ('CONTRATANTE_SEPELIO', (None, 'Contratante', 'cliente_field')),
    ('POLIZA_SEPELIO', ('CF - 000521 - 0', 'Número de Póliza para Seguros del Titular.')),
    ('POLIZA_SEPELIO_DEPENDIENTE', ('CF - 000564 - 0', 'Número de Póliza para Seguros del Dependiente.')),
    ('COSTO_SEPELIO', (3.75, 'Costo del Seguro de Sepelio para empleados Banpro.')),
    ('SUMA_SEPELIO', (1000.0, 'Suma asegurada para Seguros de Sepelio empleados Banpro.')),
    ('LOGO_SEPELIO',
     ('cotizador/images/aseguradoras/seguros_america.png', 'Logo de la compañia de seguros de Sepelio.')),
    ('EMAIL_SEPELIO', ('asanchez@segurosamerica.com,',
                       'Lista de correos de sepelio usados para las notificaciones del sistema')),

    ('ASEGURADORA_ACCIDENTE', (None, 'Aseguradora', 'aseguradora_field')),
    ('RAMO_ACCIDENTE', (None, 'Ramo', 'ramo_field')),
    ('SUBRAMO_ACCIDENTE', (None, 'Sub ramo', 'subramo_field')),
    ('CONTRATANTE_ACCIDENTE', (None, 'Contratante', 'cliente_field')),
    ('POLIZA_ACCIDENTE', ('APC - 13359 - 30977', 'Número de Póliza para Seguros de Accidente Banpro.')),
    ('COSTO_ACCIDENTE', (18.0, 'Costo del Seguro de Accidentes para empleados Banpro.')),
    ('COSTO_CARNET_ACCIDENTE', (1.85, 'Costo del carnet para seguros de Accidente')),
    ('SUMA_ACCIDENTE', (15000.0, 'Suma asegurada para Seguros de Accidentes del Titular.')),
    ('SUMA_ACCIDENTE_DEPENDIENTE', (10000.0, 'Suma asegurada para Seguros de Accidentes del Dependiente.')),
    ('LOGO_ACCIDENTE', ('cotizador/images/aseguradoras/mapfre.png', 'Logo de la compañia de seguros de Accidentes.')),
    ('EMAIL_ACCIDENTE', ('luis.collado@mapfre.com.ni,',
                         'Lista de correos de accidente usados para las notificaciones del sistema')),

    ('ASEGURADORA_VIDA', (None, 'Aseguradora', 'aseguradora_field')),
    ('RAMO_VIDA', (None, 'Ramo', 'ramo_field')),
    ('SUBRAMO_VIDA', (None, 'Sub ramo', 'subramo_field')),
    ('CONTRATANTE_VIDA', (None, 'Contratante', 'cliente_field')),
    ('POLIZA_VIDA', ('CV-000209-0', 'Número de Póliza para Seguros de Vida Banpro.')),
    ('SUMA_VIDA', ("22 veces el salario", 'Suma asegurada para Seguros de Accidentes del Titular.')),
    ('LOGO_VIDA', ('cotizador/images/aseguradoras/iniser.png', 'Logo de la compañia de seguros de Accidentes.')),

    ('COSTO_REMESA_ROBO', (3.0, 'Costo de la cobertura de robo en producto de remesas.')),
    ('COSTO_REMESA_SEPELIO', (7.0, 'Costo de la cobertura de repatriación y sepelio.')),
])

CONSTANCE_CONFIG_FIELDSETS = {
    'Configuración envio de reportes': ('EMAIL_TRUST', 'EMAIL_BANPRO', 'EMAIL_DEBITO_AUTOMATICO',
                                        'DIAS_DEBITO_AUTOMATICO'),

    'Configuración cotizador automovil': (
        'ASEGURADORA', 'RAMO', 'SUBRAMO', 'CONTRATANTE', 'TASA_AUTOMOVIL', 'SOA_AUTOMOVIL', 'PORCENTAJE_DEDUCIBLE',
        'PORCENTAJE_DEDUCIBLE_EXTENSION_TERRITORIAL',
        'MINIMO_DEDUCIBLE', 'SOA_DESCUENTO', 'EMAIL_AUTOMOVIL'
    ),

    'Configuración cotizador sepelio': (
        'ASEGURADORA_SEPELIO', 'RAMO_SEPELIO', 'SUBRAMO_SEPELIO', 'CONTRATANTE_SEPELIO',
        'POLIZA_SEPELIO', 'POLIZA_SEPELIO_DEPENDIENTE', 'COSTO_SEPELIO',
        'SUMA_SEPELIO', 'LOGO_SEPELIO', 'EMAIL_SEPELIO'),

    'Configuración cotizador accidente': (
        'ASEGURADORA_ACCIDENTE', 'RAMO_ACCIDENTE', 'SUBRAMO_ACCIDENTE', 'CONTRATANTE_ACCIDENTE',
        'POLIZA_ACCIDENTE', 'COSTO_ACCIDENTE', 'COSTO_CARNET_ACCIDENTE',
        'SUMA_ACCIDENTE', 'SUMA_ACCIDENTE_DEPENDIENTE', 'LOGO_ACCIDENTE',
        'EMAIL_ACCIDENTE'),

    'Configuración cotizador vida': (
        'ASEGURADORA_VIDA', 'RAMO_VIDA', 'SUBRAMO_VIDA', 'CONTRATANTE_VIDA',
        'POLIZA_VIDA', 'SUMA_VIDA', 'LOGO_VIDA'),

    'Configuración BANCASEGUROS remesas': ('COSTO_REMESA_ROBO', 'COSTO_REMESA_SEPELIO'),
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
        'PASSWORD': 'ABC123#$',
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

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
                        'bootstrap-select#1.13.12',
                        'bootstrap-validator#0.11.9',
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
                        'jquery#3.4.1',
                        'jquery-mask-plugin#1.14.15',
                        'jquery-ui#1.12.1',
                        'js-xlsx#0.15.5',
                        'mocha#1.17.1',
                        'moment#2.24.0',
                        'morris.js#0.5.1',
                        'mustache.js#3.0.1',
                        'raphael#2.2.7',
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
