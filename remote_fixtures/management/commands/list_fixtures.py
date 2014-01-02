from __future__ import unicode_literals
from datetime import datetime
import dateutil.parser
from django.core.management.base import BaseCommand
from django.contrib.humanize.templatetags.humanize import naturaltime
from clint.textui import columns

from remote_fixtures.utils import S3Mixin, humanize_filesize


class Command(BaseCommand, S3Mixin):
    def handle(self, *args, **options):
        bucket = self.get_bucket()

        fixtures = list(bucket.list('fixture_'))
        for fixture in fixtures:
            fixture.last_modified_dt = dateutil.parser.parse(fixture.last_modified)

        fixtures.sort(key=lambda x: x.last_modified_dt)

        for fixture in fixtures:
            print columns(
                [fixture.name, 38],
                [humanize_filesize(fixture.size), 9],
                [fixture.last_modified_dt.strftime('%d %b %G'), 12],
                [naturaltime(fixture.last_modified_dt), 25],
            )
