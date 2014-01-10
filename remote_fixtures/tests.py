from django.test import TestCase

from .utils import humanize_filesize


class HumanizeFilesizeTests(TestCase):
    def test_humanize_filesize_returns_0_for_input_0(self):
        self.assertEqual(humanize_filesize(0), '0 bytes')
