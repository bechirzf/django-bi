import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = '^^ku2l=3c$i@g!@s26x$th#%zlqs%-50do*^noaffi7*z#p0s&'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'fixtures/objects')],
        'APP_DIRS': True,
        'OPTIONS': {
            'builtins': ['bi.templatetags.report'],
        },
    }
]

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'bi'
]

ROOT_URLCONF = 'tests.urls'

LANGUAGES = (
    ('en', 'English'),
)

MIDDLEWARE_CLASSES = ()

OBJECTS_PATH = 'tests/fixtures/objects'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
