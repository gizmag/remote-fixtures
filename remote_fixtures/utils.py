from boto.s3.connection import S3Connection
from django.conf import settings

class S3Mixin(object):
    def get_bucket(self):
        if not hasattr(self, 'bucket'):
            conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            self.bucket = conn.get_bucket(settings.REMOTE_FIXTURE_BUCKET)

        return self.bucket


def humanize_filesize(bytes):
    for x in [' bytes','KB','MB','GB']:
        if bytes == 0:
            return '0 bytes'
        if bytes < 1024.0 and bytes > -1024.0:
            return "%3.1f%s" % (bytes, x)
        bytes /= 1024.0
    return "%3.1f%s" % (bytes, 'TB')
