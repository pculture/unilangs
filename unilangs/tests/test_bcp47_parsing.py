# -*- coding: utf-8 -*-

from unittest import TestCase
from unilangs.bcp47.parser import (
    parse_code, MalformedLanguageCodeException, InvalidLanguageException
)
from pprint import pprint as pp


class BCP47ParserTest(TestCase):
    def assertMalformed(self, code):
        return self.assertRaises(MalformedLanguageCodeException,
                                 lambda: parse_code(code))

    def assertInvalid(self, code):
        return self.assertRaises(InvalidLanguageException,
                                 lambda: parse_code(code))


    def test_grandfathered(self):
        p = parse_code('i-klingon')
        self.assertEqual(p['grandfathered']['tag'], 'i-klingon')
        self.assertEqual(p['grandfathered']['preferred-value'], 'tlh')
        self.assertEqual(p['grandfathered']['description'][0], 'Klingon')
        self.assertIsNone(p['language'])
        self.assertIsNone(p['extlang'])
        self.assertIsNone(p['script'])
        self.assertIsNone(p['region'])
        self.assertIsNone(p['variant'])
        self.assertEqual(p['extensions'], [])

        p = parse_code('art-lojban')
        self.assertEqual(p['grandfathered']['tag'], 'art-lojban')
        self.assertEqual(p['grandfathered']['preferred-value'], 'jbo')
        self.assertEqual(p['grandfathered']['description'][0], 'Lojban')
        self.assertIsNone(p['language'])
        self.assertIsNone(p['extlang'])
        self.assertIsNone(p['script'])
        self.assertIsNone(p['region'])
        self.assertIsNone(p['variant'])
        self.assertEqual(p['extensions'], [])

    def test_bare_language(self):
        # Bare, simple language codes should parse fine.
        p = parse_code('en')
        self.assertEqual(p['language']['subtag'], 'en')
        self.assertEqual(p['language']['description'][0], 'English')
        self.assertIsNone(p['extlang'])
        self.assertIsNone(p['script'])
        self.assertIsNone(p['region'])
        self.assertIsNone(p['variant'])
        self.assertEqual(p['extensions'], [])
        self.assertIsNone(p['grandfathered'])

        p = parse_code('de')
        self.assertEqual(p['language']['subtag'], 'de')
        self.assertEqual(p['language']['description'][0], 'German')
        self.assertIsNone(p['extlang'])
        self.assertIsNone(p['script'])
        self.assertIsNone(p['region'])
        self.assertIsNone(p['variant'])
        self.assertEqual(p['extensions'], [])
        self.assertIsNone(p['grandfathered'])

        # Language codes are case-insensitive.
        self.assertEqual(parse_code('en'), parse_code('EN'))
        self.assertEqual(parse_code('en'), parse_code('eN'))

        # Invalid languages should throw errors.
        self.assertInvalid('cheese')
        self.assertInvalid('dogs')

    def test_language_script(self):
        # Languages with scripts should parse fine.
        p = parse_code('zh-Hans')
        self.assertEqual(p['language']['subtag'], 'zh')
        self.assertEqual(p['language']['description'][0], 'Chinese')
        self.assertEqual(p['script']['subtag'].lower(), 'hans')
        self.assertEqual(p['script']['description'][0], 'Han (Simplified variant)')
        self.assertIsNone(p['extlang'])
        self.assertIsNone(p['region'])
        self.assertIsNone(p['variant'])
        self.assertEqual(p['extensions'], [])
        self.assertIsNone(p['grandfathered'])

        p = parse_code('zh-HANT')
        self.assertEqual(p['language']['subtag'], 'zh')
        self.assertEqual(p['language']['description'][0], 'Chinese')
        self.assertEqual(p['script']['subtag'].lower(), 'hant')
        self.assertEqual(p['script']['description'][0], 'Han (Traditional variant)')
        self.assertIsNone(p['extlang'])
        self.assertIsNone(p['region'])
        self.assertIsNone(p['variant'])
        self.assertEqual(p['extensions'], [])
        self.assertIsNone(p['grandfathered'])

        # Scripts cannot stand without a language.
        self.assertInvalid('Cyrl')
        self.assertInvalid('Hant')

        # Invalid languages are still invalid, even with a script.
        self.assertInvalid('kitties-Hant')

        # Invalid scripts are invalid.
        self.assertMalformed('zh-Hannt')

    def test_language_region(self):
        # Language with region codes should be fine.
        p = parse_code('en-us')
        self.assertEqual(p['language']['subtag'], 'en')
        self.assertEqual(p['language']['description'][0], 'English')
        self.assertEqual(p['region']['subtag'].lower(), 'us')
        self.assertEqual(p['region']['description'][0], 'United States')
        self.assertIsNone(p['extlang'])
        self.assertIsNone(p['script'])
        self.assertIsNone(p['variant'])
        self.assertEqual(p['extensions'], [])
        self.assertIsNone(p['grandfathered'])

        p = parse_code('en-gb')
        self.assertEqual(p['language']['subtag'], 'en')
        self.assertEqual(p['language']['description'][0], 'English')
        self.assertEqual(p['region']['subtag'].lower(), 'gb')
        self.assertEqual(p['region']['description'][0], 'United Kingdom')
        self.assertIsNone(p['extlang'])
        self.assertIsNone(p['script'])
        self.assertIsNone(p['variant'])
        self.assertEqual(p['extensions'], [])
        self.assertIsNone(p['grandfathered'])

        p = parse_code('es-419')
        self.assertEqual(p['language']['subtag'], 'es')
        self.assertEqual(p['language']['description'][0], 'Spanish')
        self.assertEqual(p['region']['subtag'].lower(), '419')
        self.assertEqual(p['region']['description'][0], 'Latin America and the Caribbean')
        self.assertIsNone(p['extlang'])
        self.assertIsNone(p['script'])
        self.assertIsNone(p['variant'])
        self.assertEqual(p['extensions'], [])
        self.assertIsNone(p['grandfathered'])

        # Regions cannot be given without a language.
        self.assertInvalid('419')
        self.assertInvalid('gb')

        # Invalid languages are still invalid, even with a region.
        self.assertInvalid('cheese-gb')

        # Invalid regions are invalid.
        self.assertMalformed('en-murica')

    def test_language_script_region(self):
        p = parse_code('en-Latn-us')
        self.assertEqual(p['language']['subtag'], 'en')
        self.assertEqual(p['language']['description'][0], 'English')
        self.assertEqual(p['region']['subtag'].lower(), 'us')
        self.assertEqual(p['region']['description'][0], 'United States')
        self.assertEqual(p['script']['subtag'].lower(), 'latn')
        self.assertEqual(p['script']['description'][0], 'Latin')
        self.assertIsNone(p['extlang'])
        self.assertIsNone(p['variant'])
        self.assertEqual(p['extensions'], [])
        self.assertIsNone(p['grandfathered'])

        p = parse_code('sr-Cyrl-RS')
        self.assertEqual(p['language']['subtag'], 'sr')
        self.assertEqual(p['language']['description'][0], 'Serbian')
        self.assertEqual(p['region']['subtag'].lower(), 'rs')
        self.assertEqual(p['region']['description'][0], 'Serbia')
        self.assertEqual(p['script']['subtag'].lower(), 'cyrl')
        self.assertEqual(p['script']['description'][0], 'Cyrillic')
        self.assertIsNone(p['extlang'])
        self.assertIsNone(p['variant'])
        self.assertEqual(p['extensions'], [])
        self.assertIsNone(p['grandfathered'])

        # Scripts and regions still require a language.
        self.assertInvalid('Latn-us')

        # Invalid language codes, scripts, and regions don't work.
        self.assertInvalid('minecraft-Latn-us')
        self.assertMalformed('en-cursive-us')
        self.assertMalformed('en-Latn-murica')
