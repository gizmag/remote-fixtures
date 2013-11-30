from __future__ import unicode_literals
import dateutil.parser
from django.core.management import call_command
from django.core.management.base import BaseCommand
from tempfile import NamedTemporaryFile

from remote_fixtures.utils import S3Mixin


class Command(BaseCommand, S3Mixin):
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

    def get_fixture_key_for_filename(self, filename):
        bucket = self.get_bucket()
        key = bucket.get_key(filename)

        if key is None:
            raise Exception('filename could not be found on S3')

        return key

    def get_file(self, key):
        file = NamedTemporaryFile(suffix='fixture.json')
        key.get_contents_to_file(file)
        file.seek(0)
        return file

    def load_fixture(self, file):
        call_command('loaddata', file.name)

    def handle(self, *args, **options):
        if len(args) > 0:
            # get fixture from supplied filename
            fixture_key = self.get_fixture_key_for_filename(args[0])
        else:
            # find latest fixture file
            fixture_key = self.get_latest_fixture_key()

        # download file
        file = self.get_file(fixture_key)

        # load it in
        self.load_fixture(file)
