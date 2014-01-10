from mock import patch, Mock
from django.test import TestCase
from django.conf import settings

from .utils import humanize_filesize, S3Mixin
from .management.commands.pull_fixtures import Command as PullFixturesCommand
from .management.commands.push_fixtures import Command as PushFixturesCommand
from .management.commands.list_fixtures import Command as ListFixturesCommand


class HumanizeFilesizeTests(TestCase):
    def test_returns_0_for_input_0(self):
        self.assertEqual(
            humanize_filesize(0),
            '0 bytes'
        )

    def test_returns_singular_byte_for_input_1(self):
        self.assertEqual(
            humanize_filesize(1),
            '1 byte'
        )

    def test_returns_number_of_bytes_if_in_byte_range(self):
        self.assertEqual(
            humanize_filesize(500),
            '500 bytes'
        )

    def test_returns_number_of_kilobytes_if_in_kilobyte_range(self):
        self.assertEqual(
            humanize_filesize(512000),
            '500.0KB'
        )

    def test_returns_number_of_megabytes_if_in_megabyte_range(self):
        self.assertEqual(
            humanize_filesize(524288000),
            '500.0MB'
        )

    def test_returns_number_of_gigabytes_if_in_gigabyte_range(self):
        self.assertEqual(
            humanize_filesize(536870912000),
            '500.0GB'
        )

    def test_returns_number_of_terabytes_if_in_terabyte_range(self):
        self.assertEqual(
            humanize_filesize(549755813888000),
            '500.0TB'
        )


class S3MixinTests(TestCase):
    def setUp(self):
        self.s3_mixin = S3Mixin()

    def test_get_bucket_uses_cached_bucket_if_exists(self):
        self.s3_mixin.bucket = 'test test test'
        result = self.s3_mixin.get_bucket()
        self.assertEqual(result, 'test test test')

    @patch('remote_fixtures.utils.S3Connection')
    def test_get_bucket_initialises_s3connection_with_key_and_secret(self, mock_s3connection):
        self.s3_mixin.get_bucket()

        mock_s3connection.assert_called_once_with(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)

    @patch('remote_fixtures.utils.S3Connection')
    def test_bucket_returned_from_get_bucket_and_cached(self, mock_s3connection):
        mock_s3connection.return_value = Mock(**{
            'get_bucket.return_value': 'this is my mock bucket'
        })
        bucket = self.s3_mixin.get_bucket()
        self.assertEqual(self.s3_mixin.bucket, 'this is my mock bucket')
        self.assertEqual(bucket, 'this is my mock bucket')
