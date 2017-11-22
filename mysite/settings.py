import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'SECRET_KEY'

DEBUG = True

ALLOWED_HOSTS = []
#ALLOWED_HOSTS = ['railwaybot.pythonanywhere.com']

# Security Measures:
'''
#SECURE_SSL_HOST                = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SECURE_SSL_REDIRECT             = True
#SESSION_COOKIE_AGE              = 600
SECURE_CONTENT_TYPE_NOSNIFF     = True
SECURE_BROWSER_XSS_FILTER       = True
CSRF_COOKIE_HTTPONLY            = True
X_FRAME_OPTIONS                 = 'DENY'
'''

# Application definition
INSTALLED_APPS = (
    'flat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Bot',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Email details:
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = 'password!'
EMAIL_HOST_USER     = 'email@gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True