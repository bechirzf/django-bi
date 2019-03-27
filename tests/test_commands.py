from io import StringIO

from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase


class WarmupcacheTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command('warmupcache', stdout=out)
        self.assertIn('Cache was successfully warmed up', out.getvalue())

    def test_command_cache_was_cleared(self):
        cache.set('test_key', 'test value')
        out = StringIO()
        call_command('warmupcache', stdout=out)
        self.assertFalse(cache.get('test_key'))
