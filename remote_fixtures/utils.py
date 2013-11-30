from boto.s3.connection import S3Connection
from django.conf import settings

class S3Mixin(object):
    def get_bucket(self):
        if not hasattr(self, 'bucket'):
            conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            self.bucket = conn.get_bucket(settings.REMOTE_FIXTURE_BUCKET)

        return self.bucket
