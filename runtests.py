#!/usr/bin/env python
import os
import sys
import warnings
from optparse import OptionParser

import django
from django.conf import settings
from django.core.management import call_command


def runtests(test_path='bi'):
    if not settings.configured:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        }

        # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(BASE_DIR, 'bi/tests/fixtures/objects')],
                'APP_DIRS': True,
            },
        ]

        # Configure test environment
        settings.configure(
            DATABASES=DATABASES,
            TEMPLATES=TEMPLATES,
            INSTALLED_APPS=(
                'django.contrib.contenttypes',
                'django.contrib.auth',
                'bi',
            ),
            ROOT_URLCONF='test_urls',
            LANGUAGES=(
                ('en', 'English'),
            ),
            MIDDLEWARE_CLASSES=(),
            OBJECTS_PATH='bi/tests/fixtures/objects',
        )

    django.setup()
    warnings.simplefilter('always', DeprecationWarning)
    failures = call_command(
        'test', test_path, interactive=False, failfast=False, verbosity=2)

    sys.exit(bool(failures))


if __name__ == '__main__':
    parser = OptionParser()

    (options, args) = parser.parse_args()
    runtests(*args)
