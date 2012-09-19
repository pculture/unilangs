# -*- coding: utf-8 -*-

from os.path import dirname, join
from unittest import TestCase
from unilangs.unilangs import LanguageCode


class LanguageCodeTest(TestCase):
    def assertEncodesAs(self, bcp47_code, unilangs_code):
        lc = LanguageCode(bcp47_code, 'bcp47')
        self.assertEqual(unilangs_code, lc.encode('unisubs'),
                         "BCP47 code '%s' did not encode to unilangs code '%s'!"
                         % (bcp47_code, unilangs_code))

    def assertLossilyEncodesAs(self, bcp47_code, unilangs_code):
        lc = LanguageCode(bcp47_code, 'bcp47-lossy')
        self.assertEqual(unilangs_code, lc.encode('unisubs'),
                         "BCP47 code '%s' did not lossily encode to unilangs code '%s'!"
                         % (bcp47_code, unilangs_code))

    def test_encode_strict(self):
        self.assertEncodesAs('en', 'en')
        self.assertEncodesAs('en-u-foo', 'en')

        self.assertEncodesAs('en-GB-a-foo-x-mouse-dogs-cats', 'en-gb')

        self.assertEncodesAs('pt', 'pt')
        self.assertEncodesAs('pt-br', 'pt-br')

        self.assertEncodesAs('ig', 'ibo')

    def test_encode_lossy(self):
        self.assertLossilyEncodesAs('en-us-u-foo', 'en')
        self.assertLossilyEncodesAs('en-Latn-US', 'en')

        self.assertLossilyEncodesAs('en-latn-GB-a-foo-x-dogs-cats', 'en-gb')

        self.assertLossilyEncodesAs('es-es', 'es')

