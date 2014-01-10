from django.test import TestCase

from .utils import humanize_filesize


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
