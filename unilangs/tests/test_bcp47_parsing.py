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

    def assertTagDesc(self, subtag_dict, tag, desc):
        self.assertEqual(subtag_dict['subtag'].lower(), tag)
        self.assertEqual(subtag_dict['description'][0], desc)

    def assertNil(self, language_dict, fields):
        for f in fields:
            val = language_dict[f]

            if f in ['variants', 'extensions']:
                self.assertEqual(val, [])
            else:
                self.assertIsNone(val)


    def test_grandfathered(self):
        p = parse_code('i-klingon')
        self.assertEqual(p['grandfathered']['tag'], 'i-klingon')
        self.assertEqual(p['grandfathered']['description'][0], 'Klingon')
        self.assertNil(p, ['language', 'extlang', 'script', 'region',
                           'variants', 'extensions'])

        p = parse_code('art-lojban')
        self.assertEqual(p['grandfathered']['tag'], 'art-lojban')
        self.assertEqual(p['grandfathered']['description'][0], 'Lojban')
        self.assertNil(p, ['language', 'extlang', 'script', 'region',
                           'variants', 'extensions'])

    def test_bare_language(self):
        # Bare, simple language codes should parse fine.
        p = parse_code('en')
        self.assertTagDesc(p['language'], 'en', 'English')
        self.assertNil(p, ['extlang', 'script', 'region', 'variants',
                           'extensions', 'grandfathered'])

        p = parse_code('de')
        self.assertTagDesc(p['language'], 'de', 'German')
        self.assertNil(p, ['extlang', 'script', 'region', 'variants',
                           'extensions', 'grandfathered'])

        # Language codes are case-insensitive.
        self.assertEqual(parse_code('en'), parse_code('EN'))
        self.assertEqual(parse_code('en'), parse_code('eN'))

        # Invalid languages should throw errors.
        self.assertInvalid('cheese')
        self.assertInvalid('dogs')

    def test_language_script(self):
        # Languages with scripts should parse fine.
        p = parse_code('zh-Hans')
        self.assertTagDesc(p['language'], 'zh', 'Chinese')
        self.assertTagDesc(p['script'], 'hans', 'Han (Simplified variant)')
        self.assertNil(p, ['extlang', 'region', 'variants', 'extensions',
                           'grandfathered'])

        p = parse_code('zh-HANT')
        self.assertTagDesc(p['language'], 'zh', 'Chinese')
        self.assertTagDesc(p['script'], 'hant', 'Han (Traditional variant)')
        self.assertNil(p, ['extlang', 'region', 'variants', 'extensions',
                           'grandfathered'])

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
        self.assertTagDesc(p['language'], 'en', 'English')
        self.assertTagDesc(p['region'], 'us', 'United States')
        self.assertNil(p, ['extlang', 'script', 'variants', 'extensions',
                           'grandfathered'])

        p = parse_code('en-gb')
        self.assertTagDesc(p['language'], 'en', 'English')
        self.assertTagDesc(p['region'], 'gb', 'United Kingdom')
        self.assertNil(p, ['extlang', 'script', 'variants', 'extensions',
                           'grandfathered'])

        p = parse_code('es-419')
        self.assertTagDesc(p['language'], 'es', 'Spanish')
        self.assertTagDesc(p['region'], '419', 'Latin America and the Caribbean')
        self.assertNil(p, ['extlang', 'script', 'variants', 'extensions',
                           'grandfathered'])

        # Regions cannot be given without a language.
        self.assertInvalid('419')
        self.assertInvalid('gb')

        # Invalid languages are still invalid, even with a region.
        self.assertInvalid('cheese-gb')

        # Invalid regions are invalid.
        self.assertMalformed('en-murica')

    def test_language_script_region(self):
        p = parse_code('en-Latn-us')
        self.assertTagDesc(p['language'], 'en', 'English')
        self.assertTagDesc(p['script'], 'latn', 'Latin')
        self.assertTagDesc(p['region'], 'us', 'United States')
        self.assertNil(p, ['extlang', 'variants', 'extensions', 'grandfathered'])

        p = parse_code('sr-Cyrl-RS')
        self.assertTagDesc(p['language'], 'sr', 'Serbian')
        self.assertTagDesc(p['script'], 'cyrl', 'Cyrillic')
        self.assertTagDesc(p['region'], 'rs', 'Serbia')
        self.assertNil(p, ['extlang', 'variants', 'extensions', 'grandfathered'])

        # Scripts and regions still require a language.
        self.assertInvalid('Latn-us')

        # Invalid language codes, scripts, and regions don't work.
        self.assertInvalid('minecraft-Latn-us')
        self.assertMalformed('en-cursive-us')
        self.assertMalformed('en-Latn-murica')

    def test_language_variants(self):
        p = parse_code('sl-rozaj')
        self.assertTagDesc(p['language'], 'sl', 'Slovenian')
        self.assertTagDesc(p['variants'][0], 'rozaj', 'Resian')
        self.assertNil(p, ['extlang', 'script', 'region', 'extensions',
                           'grandfathered'])

        p = parse_code('sl-rozaj-biske')
        self.assertTagDesc(p['language'], 'sl', 'Slovenian')
        self.assertTagDesc(p['variants'][0], 'rozaj', 'Resian')
        self.assertTagDesc(p['variants'][1], 'biske', 'The San Giorgio dialect of Resian')
        self.assertNil(p, ['extlang', 'script', 'region', 'extensions',
                           'grandfathered'])

        # Variants still require a language.
        self.assertInvalid('rozaj')
        self.assertInvalid('rozaj-biske')

        # Invalid variants don't work.
        self.assertMalformed('sl-rozajbad')

    def test_language_region_variants(self):
        p = parse_code('de-CH-1901')
        self.assertTagDesc(p['language'], 'de', 'German')
        self.assertTagDesc(p['region'], 'ch', 'Switzerland')
        self.assertTagDesc(p['variants'][0], '1901', 'Traditional German orthography')
        self.assertNil(p, ['extlang', 'script', 'extensions', 'grandfathered'])
