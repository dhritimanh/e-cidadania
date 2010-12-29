# Django settings for e_cidadania project.

# Get the current directory
import os
cwd = os.path.dirname(os.path.realpath(__file__))

# Django settings
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Extending the user profile a bit more
AUTH_PROFILE_MODULE = "accounts.UserProfile"
ACCOUNT_ACTIVATION_DAYS = 2
LOGIN_REDIRECT_URL = '/accounts/profile'
GOOGLE_MAPS_API_KEY = 'ABQIAAAATqrYeRgzMa92HeAJ337iJhRIU2G0euEtM3XnBHtmv6MD_woHxRSapJw6ROu7OKaPDPIwetftitHBcw'

# Registration mail settings
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'accounts@cidadania.coop'


ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db/sqlite.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Madrid'
LANGUAGE_CODE = 'es-ES'
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = cwd + '/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8nwcwmtau*bnu0u=shmdkda^-tpn55ch%qeqc8xn#-77r8c*0a'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'e_cidadania.urls'

TEMPLATE_DIRS = (
    cwd + '/templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'registration',
    'tagging',
    
    'e_cidadania.userprofile',
    'e_cidadania.accounts',
    'e_cidadania.proposals',
)
