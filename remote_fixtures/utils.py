import os
from boto.s3.connection import S3Connection
from remote_fixtures.conf import settings


class FixtureSource(object):
    S3 = 's3'
    CACHE = 'cache'


class S3Mixin(object):
    def get_bucket(self):
        if not hasattr(self, 'bucket'):
            conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            self.bucket = conn.get_bucket(settings.REMOTE_FIXTURES_BUCKET_NAME)

        return self.bucket

    def remove_gz_suffix(self, filename):
        if filename.endswith('.gz'):
            return filename[:-3]
        return filename

    def get_base_cache_path(self):
        base_path = os.getenv(
            'REMOTE_FIXTURES_CACHE_PATH',
            settings.REMOTE_FIXTURES_BASE_CACHE_PATH
        )

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        return base_path

    def get_cache_path(self, filename):
        return '{}/{}_{}'.format(
            self.get_base_cache_path(),
            self.get_bucket().name,
            filename
        )

    def cache_fixture_file(self, fixture_file, filename):
        path = self.get_cache_path(filename)

        with open(path, 'w+') as cache_file:
            for line in fixture_file:
                cache_file.write(line)

        fixture_file.seek(0)


def humanize_filesize(byte_count):
    if byte_count < 1024:
        if byte_count == 1:
            return '1 byte'
        return '{} bytes'.format(byte_count)
    else:
        byte_count /= 1024.0
        for x in ['KB', 'MB', 'GB']:
            if byte_count < 1024.0 and byte_count > -1024.0:
                return "%3.1f%s" % (byte_count, x)
            byte_count /= 1024.0
        return "%3.1f%s" % (byte_count, 'TB')
