from __future__ import unicode_literals
from datetime import datetime
import dateutil.parser
import json
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from tempfile import NamedTemporaryFile

from remote_fixtures.utils import S3Mixin


class Command(BaseCommand, S3Mixin):
    def get_fixture_file(self, dumpdata_args):
        file = NamedTemporaryFile(suffix='.json')
        data = call_command('dumpdata', *dumpdata_args, stdout=file)
        file.seek(0)
        return file

    def get_file_name(self):
        now = datetime.utcnow()
        return 'fixture_%s.json' % slugify(unicode(now.isoformat()))

    def upload_file(self, file, filename):
        bucket = self.get_bucket()
        key = bucket.new_key(filename)
        key.set_contents_from_file(file)
        return key

    def handle(self, *args, **options):
        file = self.get_fixture_file(args)
        filename = self.get_file_name()
        key = self.upload_file(file, filename)
        if len(args):
            contents = json.dumps(args)
        else:
            contents = '["all"]'
        key.set_metadata('x-amz-meta-contents', contents)

        print 'filename: %s' % filename
