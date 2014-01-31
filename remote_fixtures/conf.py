import os
from django.conf import settings
from appconf import AppConf


class RemoteFixturesConf(AppConf):
    ENABLE_CACHE = False
    BUCKET_NAME = None
    BASE_CACHE_PATH = '{}/.remote_fixture_cache'.format(os.getenv('HOME'))

    class Meta:
        prefix = 'remote_fixtures'
