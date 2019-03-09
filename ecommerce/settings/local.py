import os
from ..config import Config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = '*o(aj(#l+u-i#j8-#=8e2qc&ax58@6w-&*&6)jx6%t5j3lbctk'

DEBUG = True

ALLOWED_HOSTS = []

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = Config.EMAIL_HOST_USER 
EMAIL_HOST_PASSWORD = Config.EMAIL_HOST_PASSWORD
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Python eCommerce <{}>'.format(Config.EMAIL_HOST_USER)
BASE_URL = '127.0.0.1:8000'
DEFAULT_ACTIVATION_DAYS = 7

MANAGERS = (
    ("OSAMA MOHAMED", Config.EMAIL_HOST_USER),
)

ADMINS = MANAGERS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'products.apps.ProductsConfig',
    'search.apps.SearchConfig',
    'tags.apps.TagsConfig',
    'carts.apps.CartsConfig',
    'orders.apps.OrdersConfig',
    'billing.apps.BillingConfig',
    'addresses.apps.AddressesConfig',
    'analytics.apps.AnalyticsConfig',
    'marketing.apps.MarketingConfig',
    'contact.apps.ContactConfig'
]

AUTH_USER_MODEL = 'accounts.User'
LOGOUT_REDIRECT_URL = '/account/login/'
LOGIN_URL = '/account/login'
# LOGIN_REDIRECT_URL = '/'
# LOGOUT_URL = '/logout/'

SUB_TOTAL_PERCENTAGE = 1.08

FORCE_SESSION_TO_ONE = False
FORCE_INACTIVE_USER_ENDSESSION = False

STRIPE_SECRET_KEY = Config.STRIPE_SECRET_KEY
STRIPE_PUB_KEY = Config.STRIPE_PUB_KEY

MAILCHIMP_API_KEY           = Config.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER       = Config.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID     = Config.MAILCHIMP_EMAIL_LIST_ID

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'e_commerce',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'OSAMA',
        'PASSWORD': 'OSAMA',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Cairo'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_local")
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "static_root")

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "media_root")

PROTECTED_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "protected_media")

CORS_REPLACE_HTTPS_REFERER      = False
HOST_SCHEME                     = "http://"
SECURE_PROXY_SSL_HEADER         = None
SECURE_SSL_REDIRECT             = False
SESSION_COOKIE_SECURE           = False
CSRF_COOKIE_SECURE              = False
SECURE_HSTS_SECONDS             = None
SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
SECURE_FRAME_DENY               = False
