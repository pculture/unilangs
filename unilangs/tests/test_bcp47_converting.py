# -*- coding: utf-8 -*-

from unittest import TestCase
from unilangs.bcp47.converter import BCP47ToUnilangConverter


c = BCP47ToUnilangConverter()

class BCP47ConverterTest(TestCase):
    def test_simple(self):
        """Test some basic tags."""

        self.assertEqual(c['en'], 'en')
        self.assertEqual(c['en-us'], 'en')
        self.assertEqual(c['en-gb'], 'en-gb')

        self.assertEqual(c['is'], 'is')

        self.assertEqual(c['ig'], 'ibo')
        self.assertEqual(c['aao'], 'arq')

    def test_extra(self):
        """Test BCP47 tags that have extra, unused stuff in them."""

        self.assertEqual(c['en-Latn-US'], 'en')
        self.assertEqual(c['de-DE'], 'de')
        self.assertEqual(c['en-x-cats-dogs-mice'], 'en')

    def test_tricky(self):
        """Test some BCP47 codes that need special parts to convert right."""

        self.assertEqual(c['sr'], 'sr')
        self.assertEqual(c['sr-SR'], 'sr')
        self.assertEqual(c['sr-Latn'], 'sr-latn')
        self.assertEqual(c['sr-Latn-SR'], 'sr-latn')

        self.assertEqual(c['yue'], 'zh')
        self.assertEqual(c['zh-Hans'], 'zh-cn')
        self.assertEqual(c['zh-Hant'], 'zh-tw')
        self.assertEqual(c['zh-Hant-HK'], 'zh-hk')
        self.assertEqual(c['zh-Hans-SG'], 'zh-sg')

