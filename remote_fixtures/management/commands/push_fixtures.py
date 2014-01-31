from __future__ import unicode_literals
from datetime import datetime
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from gzip import GzipFile
from tempfile import NamedTemporaryFile
from optparse import make_option

from remote_fixtures.conf import settings
from remote_fixtures.utils import S3Mixin


class Command(BaseCommand, S3Mixin):
    option_list = BaseCommand.option_list + (
        make_option(
            '--nocompress',
            action='store_false',
            dest='compress',
            default=True,
        ),
    )

    def get_fixture_file(self, dumpdata_args):
        fixture_file = NamedTemporaryFile(suffix='.json')
        call_command('dumpdata', *dumpdata_args, stdout=fixture_file)
        fixture_file.seek(0)
        return fixture_file

    def compress_fixture_file(self, fixture_file):
        compressed_file = NamedTemporaryFile(suffix='.json.gz')
        gzip_file = GzipFile(compresslevel=9, fileobj=compressed_file)
        gzip_file.write(fixture_file.read())
        gzip_file.close()
        compressed_file.seek(0)
        return compressed_file


    def get_file_name(self, compress):
        now = datetime.utcnow()
        return 'fixture_{}.json{}'.format(
            slugify(unicode(now.isoformat())),
            '.gz' if compress else ''
        )

    def upload_file(self, fixture_file, filename):
        bucket = self.get_bucket()
        key = bucket.new_key(filename)
        key.set_contents_from_file(fixture_file)

    def handle(self, *args, **options):
        filename = self.get_file_name(options['compress'])
        fixture_file = self.get_fixture_file(args)

        if settings.REMOTE_FIXTURES_ENABLE_CACHE:
            self.cache_fixture_file(fixture_file, self.remove_gz_suffix(filename))

        if options['compress']:
            fixture_file = self.compress_fixture_file(fixture_file)

        self.upload_file(fixture_file, filename)

        print 'filename: %s' % filename
