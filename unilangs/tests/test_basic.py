# -*- coding: utf-8 -*-

from unittest import TestCase
from unilangs.unilangs import LanguageCode


class LanguageCodeTest(TestCase):
    def test_encode(self):
        lc = LanguageCode('en', 'iso-639-1')

        self.assertEqual('en', lc.encode('iso-639-1'),
                         "Incorrect encoded value.")

        lc = LanguageCode('bm', 'iso-639-1')

        self.assertEqual('bm', lc.encode('iso-639-1'),
                         "Incorrect encoded value.")

        self.assertEqual('bam', lc.encode('unisubs'),
                         "Incorrect encoded value.")


    def test_aliases(self):
        lc = LanguageCode('bm', 'iso-639-1')
        aliases = lc.aliases()

        self.assertIn('iso-639-1', aliases,
                      "Alias not found.")
        self.assertIn('unisubs', aliases,
                      "Alias not found.")

        self.assertEqual('bm', aliases['iso-639-1'],
                         'Incorrect alias.')
        self.assertEqual('bam', aliases['unisubs'],
                         'Incorrect alias.')

