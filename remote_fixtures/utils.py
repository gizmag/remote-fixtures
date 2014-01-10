from boto.s3.connection import S3Connection
from django.conf import settings

class S3Mixin(object):
    def get_bucket(self):
        if not hasattr(self, 'bucket'):
            conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            self.bucket = conn.get_bucket(settings.REMOTE_FIXTURE_BUCKET)

        return self.bucket


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
