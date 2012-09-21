# -*- coding: utf-8 -*-
from os.path import dirname, join

import unilangs.bcp47.parser as parser
from unittest import TestCase
from unilangs.bcp47.parser import (
    parse_code, MalformedLanguageCodeException
)


class BCP47ParserTest(TestCase):
    def assertMalformed(self, code):
        return self.assertRaises(MalformedLanguageCodeException,
                                 lambda: parse_code(code))


    def assertTagDesc(self, subtag_dict, tag, desc):
        self.assertEqual(subtag_dict['subtag'].lower(), tag)
        self.assertEqual(subtag_dict['description'][0], desc)

    def assertNil(self, language_dict, fields):
        for f in fields:
            val = language_dict[f]

            if f == 'variants':
                self.assertEqual(val, [])
            elif f == 'extensions':
                self.assertEqual(val, {})
            else:
                self.assertIsNone(val)


    def test_grandfathered(self):
        p = parser._parse_code('i-klingon')
        self.assertEqual(p['grandfathered']['tag'], 'i-klingon')
        self.assertEqual(p['grandfathered']['description'][0], 'Klingon')
        self.assertNil(p, ['language', 'extlang', 'script', 'region',
                           'variants', 'extensions'])

        p = parser._parse_code('i-navajo')
        self.assertEqual(p['grandfathered']['tag'], 'i-navajo')
        self.assertEqual(p['grandfathered']['description'][0], 'Navajo')
        self.assertNil(p, ['language', 'extlang', 'script', 'region',
                           'variants', 'extensions'])

        p = parser._parse_code('art-lojban')
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
        self.assertMalformed('cheese')
        self.assertMalformed('dogs')

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
        self.assertMalformed('Cyrl')
        self.assertMalformed('Hant')

        # Invalid languages are still invalid, even with a script.
        self.assertMalformed('kitties-Hant')

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
        self.assertMalformed('419')
        self.assertMalformed('gb')

        # Invalid languages are still invalid, even with a region.
        self.assertMalformed('cheese-gb')

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
        self.assertMalformed('Latn-us')

        # Invalid language codes, scripts, and regions don't work.
        self.assertMalformed('minecraft-Latn-us')
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
        self.assertMalformed('rozaj')
        self.assertMalformed('rozaj-biske')

        # Invalid variants don't work.
        self.assertMalformed('sl-rozajbad')

    def test_language_region_variants(self):
        p = parse_code('de-CH-1901')
        self.assertTagDesc(p['language'], 'de', 'German')
        self.assertTagDesc(p['region'], 'ch', 'Switzerland')
        self.assertTagDesc(p['variants'][0], '1901', 'Traditional German orthography')
        self.assertNil(p, ['extlang', 'script', 'extensions', 'grandfathered'])

        p = parse_code('sl-it-nedis')
        self.assertTagDesc(p['language'], 'sl', 'Slovenian')
        self.assertTagDesc(p['region'], 'it', 'Italy')
        self.assertTagDesc(p['variants'][0], 'nedis', 'Natisone dialect')
        self.assertNil(p, ['extlang', 'script', 'extensions', 'grandfathered'])

        p = parse_code('fr-419-1694acad-hepburn')
        self.assertTagDesc(p['language'], 'fr', 'French')
        self.assertTagDesc(p['region'], '419', 'Latin America and the Caribbean')
        self.assertTagDesc(p['variants'][0], '1694acad', 'Early Modern French')
        self.assertTagDesc(p['variants'][1], 'hepburn', 'Hepburn romanization')
        self.assertNil(p, ['extlang', 'script', 'extensions', 'grandfathered'])

        self.assertMalformed('419-1694acad')
        self.assertMalformed('fr-2345-nedis')
        self.assertMalformed('fr-ca-01010101')

    def test_language_script_region_variants(self):
        p = parse_code('hy-Latn-IT-arevela')
        self.assertTagDesc(p['language'], 'hy', 'Armenian')
        self.assertTagDesc(p['script'], 'latn', 'Latin')
        self.assertTagDesc(p['region'], 'it', 'Italy')
        self.assertTagDesc(p['variants'][0], 'arevela', 'Eastern Armenian')
        self.assertNil(p, ['extlang', 'extensions', 'grandfathered'])

        self.assertMalformed('Latn-IT-arevela')
        self.assertMalformed('hy-invalid-IT-arevela')
        self.assertMalformed('hy-Latn-invalid-arevela')
        self.assertMalformed('hy-Latn-IT-invalid')

    def test_language_extlang(self):
        p = parser._parse_code('zh-cmn-Hans-CN')
        self.assertTagDesc(p['language'], 'zh', 'Chinese')
        self.assertTagDesc(p['extlang'], 'cmn', 'Mandarin Chinese')
        self.assertTagDesc(p['script'], 'hans', 'Han (Simplified variant)')
        self.assertTagDesc(p['region'], 'cn', 'China')
        self.assertNil(p, ['variants', 'extensions', 'grandfathered'])

        p = parser._parse_code('zh-yue-HK')
        self.assertTagDesc(p['language'], 'zh', 'Chinese')
        self.assertTagDesc(p['extlang'], 'yue', 'Yue Chinese')
        self.assertTagDesc(p['region'], 'hk', 'Hong Kong')
        self.assertNil(p, ['script', 'variants', 'extensions', 'grandfathered'])

        p = parser._parse_code('sgn-ase')
        self.assertTagDesc(p['language'], 'sgn', 'Sign languages')
        self.assertTagDesc(p['extlang'], 'ase', 'American Sign Language')
        self.assertNil(p, ['script', 'region', 'variants', 'extensions',
                           'grandfathered'])

        self.assertMalformed('zh-invalid-Hans-CN')
        self.assertMalformed('zh-cmn-invalid-CN')
        self.assertMalformed('zh-cmn-Hans-invalid')

    def test_extensions(self):
        p = parse_code('x-cheese')
        self.assertEqual(p['extensions'], {'x': ['cheese']})
        self.assertNil(p, ['language', 'extlang', 'script', 'region',
                           'variants', 'grandfathered'])

        p = parse_code('x-cheese-and-crackers')
        self.assertEqual(p['extensions'], {'x': ['cheese', 'and', 'crackers']})
        self.assertNil(p, ['language', 'extlang', 'script', 'region',
                           'variants', 'grandfathered'])

        p = parse_code('fr-u-ham-and-swiss')
        self.assertTagDesc(p['language'], 'fr', 'French')
        self.assertEqual(p['extensions'], {'u': ['ham', 'and', 'swiss']})
        self.assertNil(p, ['extlang', 'script', 'region', 'variants',
                           'grandfathered'])

        p = parse_code('hy-Latn-IT-arevela-x-phonebook-a-foo-b-bar-baz')
        self.assertTagDesc(p['language'], 'hy', 'Armenian')
        self.assertTagDesc(p['script'], 'latn', 'Latin')
        self.assertTagDesc(p['region'], 'it', 'Italy')
        self.assertTagDesc(p['variants'][0], 'arevela', 'Eastern Armenian')
        self.assertEqual(p['extensions'], {'x': ['phonebook'],
                                           'a': ['foo'],
                                           'b': ['bar', 'baz']})
        self.assertNil(p, ['extlang', 'grandfathered'])

        # Extensions have to contain data.
        self.assertMalformed('x-')
        self.assertMalformed('x-x-foo')
        self.assertMalformed('x-a-foo')
        self.assertMalformed('x-foo-a')
        self.assertMalformed('x--eggs')
        self.assertMalformed('x-egg--dog')
        self.assertMalformed('x-egg-dog-')

        # Private use extensions can stand alone, but others cannot.
        self.assertMalformed('a-foo')
        self.assertMalformed('u-bar')
        self.assertMalformed('u-bar-x-baz')

        # According to the spec, I *think* this should be invalid, but I'm not
        # 100% sure so we'll accept it for now.
        # self.assertMalformed('x-foo-a-bar')


    def test_invalid(self):
        """Test some malformed tags to make sure they don't parse."""

        # Two regions.
        self.assertMalformed('de-419-DE')

        # Starting with a non-x singleton.
        self.assertMalformed('a-DE')

        # Bad dashes.
        self.assertMalformed('en--us')
        self.assertMalformed('en-us-')

        # Garbage.
        self.assertMalformed('en-us,')
        self.assertMalformed('en us')

        # Duplicate extension singleton tags.
        self.assertMalformed('ar-a-aaa-b-bbb-a-ccc')
        self.assertMalformed('en-us-a-123-b-bbb-a-ccc')


    def test_youtube(self):
        """Test a bunch of language codes YouTube uses.

        This should give us a nice variety of test cases.

        """
        with open(join(dirname(__file__), 'youtube_languages.txt')) as f:
            for code in f:
                # For some reason youtube uses underscores in some of its codes.
                # We'll just strip them out here -- users of the library can do
                # sanitation stuff like this themselves.
                code = code.strip()
                code = code.replace('_', '-')

                self.assertIsNotNone(parse_code(code))


    def test_normalization_grandfathered(self):
        p = parse_code('i-navajo')
        self.assertTagDesc(p['language'], 'nv', 'Navajo')
        self.assertNil(p, ['extlang', 'script', 'region', 'variants',
                           'extensions', 'grandfathered'])

        p = parse_code('art-lojban')
        self.assertTagDesc(p['language'], 'jbo', 'Lojban')
        self.assertNil(p, ['extlang', 'script', 'region', 'variants',
                           'extensions', 'grandfathered'])

    def test_normalization_extlangs(self):
        p = parse_code('sgn-ase')
        self.assertTagDesc(p['language'], 'ase', 'American Sign Language')
        self.assertNil(p, ['extlang', 'script', 'region', 'variants',
                           'extensions', 'grandfathered'])

        p = parse_code('ar-abh')
        self.assertTagDesc(p['language'], 'abh', 'Tajiki Arabic')
        self.assertNil(p, ['extlang', 'script', 'region', 'variants',
                           'extensions', 'grandfathered'])
    def test_normalization_languages(self):
        p = parse_code('ji-Latn')
        self.assertTagDesc(p['language'], 'yi', 'Yiddish')
        self.assertTagDesc(p['script'], 'latn', 'Latin')
        self.assertNil(p, ['extlang', 'region', 'variants', 'extensions',
                           'grandfathered'])

        p = parse_code('iw-u-foo-bar')
        self.assertTagDesc(p['language'], 'he', 'Hebrew')
        self.assertEqual(p['extensions'], {'u': ['foo', 'bar']})
        self.assertNil(p, ['extlang', 'script', 'region', 'variants',
                           'grandfathered'])
    def test_normalization_redundant(self):
        # These aren't special cases -- they're just provided in the subtag
        # registry as examples for god knows why.

        p = parse_code('zh-gan')
        self.assertTagDesc(p['language'], 'gan', 'Gan Chinese')
        self.assertNil(p, ['extlang', 'script', 'region', 'variants',
                           'extensions', 'grandfathered'])

        p = parse_code('zh-cmn-Hans')
        self.assertTagDesc(p['language'], 'cmn', 'Mandarin Chinese')
        self.assertTagDesc(p['script'], 'hans', 'Han (Simplified variant)')
        self.assertNil(p, ['extlang', 'region', 'variants', 'extensions',
                           'grandfathered'])
