from __future__ import unicode_literals
from datetime import datetime
import dateutil.parser
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from tempfile import NamedTemporaryFile

from remote_fixtures.utils import S3Mixin


class Command(BaseCommand, S3Mixin):
    def get_fixture_file(self, dumpdata_args):
        fixture_file = NamedTemporaryFile(suffix='.json')
        call_command('dumpdata', *dumpdata_args, stdout=fixture_file)
        fixture_file.seek(0)
        return fixture_file

    def get_file_name(self):
        now = datetime.utcnow()
        return 'fixture_%s.json' % slugify(unicode(now.isoformat()))

    def upload_file(self, fixture_file, filename):
        bucket = self.get_bucket()
        key = bucket.new_key(filename)
        key.set_contents_from_file(fixture_file)

    def handle(self, *args, **options):
        fixture_file = self.get_fixture_file(args)
        filename = self.get_file_name()
        self.upload_file(fixture_file, filename)

        print 'filename: %s' % filename
