import os,sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
HERE=os.path.dirname(os.path.dirname(__file__))

ADMINS = (
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'monit',                      
        'USER': 'monit',
        'PASSWORD': '123456',
        'HOST': '',                      
        'PORT': '',                    
    }
}

ALLOWED_HOSTS = []

TIME_ZONE = 'Asia/Shanghai'

LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = ''

MEDIA_URL = ''


STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static').replace('\\','/')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(HERE,'app/static/').replace('\\','/'),
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'hyc*qbz@t!$)ki-6d3+dj5!0(=@gk3q14u9&som!v_*ocpi8yi'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

SESSION_COOKIE_AGE=60*300

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'


SITE_ROOT = os.path.realpath(os.path.dirname(__file__)) 
TEMPLATE_DIRS = (
	os.path.join(SITE_ROOT, 'templates'),
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'south',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
