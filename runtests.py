#!/usr/bin/env python
import sys

from django.conf import settings
from django.core.management import execute_from_command_line


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        USE_TZ=True,
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'remote_fixtures',
        ),
        TEST_RUNNER='django_nose.NoseTestSuiteRunner',
        AWS_ACCESS_KEY_ID='my access key',
        AWS_SECRET_ACCESS_KEY='my secret key',
        REMOTE_FIXTURE_BUCKET='my remote fixture bucket name',
        NOSE_ARGS=[
            '--with-coverage',
            '--cover-package=remote_fixtures',
        ]
    )


def runtests():
    argv = sys.argv[:1] + ['test', 'remote_fixtures']
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()
