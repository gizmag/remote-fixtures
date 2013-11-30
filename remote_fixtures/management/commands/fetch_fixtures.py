from boto.s3.connection import S3Connection
import dateutil.parser
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings
from tempfile import NamedTemporaryFile


class Command(BaseCommand):
    def get_bucket(self):
        if not hasattr(self, 'bucket'):
            conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            self.bucket = conn.get_bucket(settings.REMOTE_FIXTURE_BUCKET)

        return self.bucket

    def get_latest_fixture_key(self):
        bucket = self.get_bucket()
        fixtures = bucket.list('fixture_')
        latest_fixture = None
        for fixture in fixtures:
            fixture.last_modified_dt = dateutil.parser.parse(fixture.last_modified)
            if latest_fixture is None:
                latest_fixture = fixture
            elif fixture.last_modified_dt > latest_fixture.last_modified_dt:
                latest_fixture = fixture

        return latest_fixture

    def get_file(self, key):
        file = NamedTemporaryFile(suffix='fixture.json')
        key.get_contents_to_file(file)
        file.seek(0)
        return file

    def load_fixture(self, file):
        call_command('loaddata', file.name)

    def handle(self, *args, **options):
        # open connection to s3
        bucket = self.get_bucket()

        # find latest fixture file
        fixture_key = self.get_latest_fixture_key()

        # download file
        file = self.get_file(fixture_key)

        # load it in
        self.load_fixture(file)
