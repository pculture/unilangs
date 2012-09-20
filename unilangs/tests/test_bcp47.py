# -*- coding: utf-8 -*-

from os.path import dirname, join
from unittest import TestCase
from unilangs.unilangs import LanguageCode


class BCP47Test(TestCase):
    def assertEncodesAs(self, unisubs_code, bcp47_code):
        lc = LanguageCode(unisubs_code, 'unisubs')
        self.assertEqual(bcp47_code, lc.encode('bcp47'),
                        "Unisubs code '%s' did not encode to BCP47 code '%s' (it encoded to '%s' instead)!"
                         % (unisubs_code, bcp47_code, lc.encode('bcp47')))

    def assertDecodesAs(self, bcp47_code, unilangs_code):
        lc = LanguageCode(bcp47_code, 'bcp47')
        self.assertEqual(unilangs_code, lc.encode('unisubs'),
                         "BCP47 code '%s' did not decode to unilangs code '%s'!"
                         % (bcp47_code, unilangs_code))

    def assertLossilyDecodesAs(self, bcp47_code, unilangs_code):
        lc = LanguageCode(bcp47_code, 'bcp47-lossy')
        self.assertEqual(unilangs_code, lc.encode('unisubs'),
                         "BCP47 code '%s' did not lossily decode to unilangs code '%s'!"
                         % (bcp47_code, unilangs_code))

    def assertRoundtrips(self, bcp47_code):
        lc = LanguageCode(bcp47_code, 'bcp47')
        self.assertEqual(bcp47_code, lc.encode('bcp47'),
                        "BCP47 code '%s' did not round trip properly (it encoded to '%s' instead)!"
                         % (bcp47_code, lc.encode('bcp47')))


    def test_decode_strict(self):
        self.assertDecodesAs('en', 'en')
        self.assertDecodesAs('en-u-foo', 'en')

        self.assertDecodesAs('en-GB-a-foo-x-mouse-dogs-cats', 'en-gb')

        self.assertDecodesAs('pt', 'pt')
        self.assertDecodesAs('pt-br', 'pt-br')

        self.assertDecodesAs('ig', 'ibo')
        self.assertDecodesAs('fy', 'fy-nl')

        self.assertDecodesAs('es', 'es')
        self.assertDecodesAs('es-ar', 'es-ar')
        self.assertDecodesAs('es-mx', 'es-mx')
        self.assertDecodesAs('es-ni', 'es-ni')

    def test_decode_lossy(self):
        self.assertLossilyDecodesAs('en-us-u-foo', 'en')
        self.assertLossilyDecodesAs('en-Latn-US', 'en')

        self.assertLossilyDecodesAs('en-latn-GB-a-foo-x-dogs-cats', 'en-gb')

        self.assertLossilyDecodesAs('es-es', 'es')


    def test_encode(self):
        """Test that some basic languages encode to bcp47 properly."""

        #                    Unilangs   BCP47
        self.assertEncodesAs('en',      'en')
        self.assertEncodesAs('ibo',     'ig')
        self.assertEncodesAs('en-gb',   'en-gb')
        self.assertEncodesAs('fy-nl',   'fy')
        self.assertEncodesAs('sr-latn', 'sr-latn')
        self.assertEncodesAs('zh-cn',   'zh-hans')
        self.assertEncodesAs('zh-hk',   'zh-hant-hk')
        self.assertEncodesAs('swa',     'sw')

    def test_roundtrip(self):
        self.assertRoundtrips('en')
        self.assertRoundtrips('es-ar')
        self.assertRoundtrips('fy')
        self.assertRoundtrips('ff')
        self.assertRoundtrips('sr-latn')
        self.assertRoundtrips('zh-hans-sg')
