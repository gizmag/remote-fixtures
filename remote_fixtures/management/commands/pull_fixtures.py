from __future__ import unicode_literals
import os
import dateutil.parser
from django.core.management import call_command
from django.core.management.base import BaseCommand
from tempfile import NamedTemporaryFile
from gzip import GzipFile

from remote_fixtures.conf import settings
from remote_fixtures.utils import S3Mixin, FixtureSource


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

    def decompress_file(self, gzipped_file):
        decompressed_file = NamedTemporaryFile(suffix='fixture.json')
        gzip_file = GzipFile(gzipped_file.name, mode='r')

        decompressed_file.write(gzip_file.read())
        decompressed_file.seek(0)

        return decompressed_file

    def get_file(self, key):
        fixture_file = None
        if settings.REMOTE_FIXTURES_ENABLE_CACHE:
            path = self.get_cache_path(self.remove_gz_suffix(key.name))
            if os.path.exists(path):
                fixture_file = open(path, 'r')
                source = FixtureSource.CACHE

        if not fixture_file:
            fixture_file = NamedTemporaryFile(suffix='fixture.json', mode='w+')
            source = FixtureSource.S3
            key.get_contents_to_file(fixture_file)
            fixture_file.seek(0)

            if key.name.endswith('.gz'):
                return (self.decompress_file(fixture_file), source)

        return (fixture_file, source)

    def load_fixture(self, fixture_file):
        call_command('loaddata', fixture_file.name)

    def handle(self, *args, **options):
        if len(args) > 0:
            # get fixture from supplied filename
            fixture_key = self.get_fixture_key_for_filename(args[0])
        else:
            # find latest fixture file
            fixture_key = self.get_latest_fixture_key()

        # download file
        fixture_file, source = self.get_file(fixture_key)
        print source

        # cache if requested
        if settings.REMOTE_FIXTURES_ENABLE_CACHE:
            if source == FixtureSource.S3:
                self.cache_fixture_file(fixture_file, self.remove_gz_suffix(fixture_key.name))

        # load it in
        self.load_fixture(fixture_file)
