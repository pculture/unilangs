# -*- coding: utf-8 -*-
"""Universal Language Codes

This library aims to provide an [en/de]coding utility for language codes.

To get a "universal" language code you create a LanguageCode object, giving it
the code and the standard it should use to look up that code.

    >>> lc = LanguageCode('en', 'iso-639-1')

Internally the code is stored in a custom standard designed specifically for
this purpose.  It doesn't have any use in the real world, so to get a useful
representation out you "encode" the code:

    >>> lc.encode('iso-639-2')
    'eng'

This is similar to Python's handling of Unicode and byte strings:

    >>> s = 'Hello, world'.decode('ascii')

    >>> s
    u'Hello, world'

    >>> s.encode('utf-8')
    'Hello, world'

"""

import copy

from .bcp47.converter import (
    StrictBCP47ToUnilangConverter, LossyBCP47ToUnilangConverter,
    UNILANGS_TO_BCP47
)


def _reverse_dict(d):
    return dict([(v, k) for k, v in d.items()])


# INTERNAL_NAMES stores the English names for the various languages.
#
# Code -> English name
#
# { 'ar': u'Arabic',
#   'el': u'Greek',
#   ... }
INTERNAL_NAMES = {}

# TO_INTERNAL is a dict of dicts.
#
# The first level is a mapping of standard names to their dicts.
#
# The second level (one per standard) is a mapping of that standard's language
# codes to the internal language codes.
#
# { 'iso-639-1': {
#      'ak': 'aka',
#      ...
#    },
#    ... }
TO_INTERNAL = {}

# FROM_INTERNAL is a dict of dicts.
#
# The first level is a mapping of standard names to their dicts.
#
# The second level (one per standard) is a mapping of internal language codes
# to that standard's language codes.
#
# { 'iso-639-1': {
#      'ak': 'aka',
#      ...
#    },
#    ... }
FROM_INTERNAL = {}


gettext_noop = lambda s: s

def convert_bcp47_case(language_code):
    """
    en -> en
    fr -> fr
    fr-ca -> fr-CA
    es-mx -> es-MX
    zh-cn -> zh-CN
    zh-hant -> zh-Hant
    zh-hans -> zh-Hans
    """
    language_country = language_code.split('-')
    if len(language_country) > 1:
        if len(language_country[1]) > 2:
            language_code = language_country[0] + '-' + language_country[1].capitalize()
        else:
            language_code = language_country[0] + '-' + language_country[1].upper()
    return language_code

def add_standard(standard, mapping, base=None, exclude=None, bcp47_case=False):
    """Add a new standard to the list of supported standards.

    `mapping` should be a dictionary mapping your custom standard's codes to the
    internal "universal" code used by this library.

    `base` is optional.  If given it will use the given standard as a base and
    copy all of its mappings before updating it with the ones you pass in
    through `mappings`.

    This can be useful for creating your own custom standard that's mostly like
    an existing one except for a few changes:

        >>> add_standard('my-standard', {'american': 'en'}, base='iso-639-1')

    This example creates a new custom standard, which is pretty much like
    ISO-639-1 but adds a code called 'american' that represents the English
    language.  Now you can do:

        >>> lc = LanguageCode('american', 'my-standard')
        >>> lc.encode('iso-639-2')
        'en'

    You can pass a list of codes to exclude from the base through the `exclude`
    parameter:

        >>> add_standard('my-standard', {'american': 'en'},
                         base='iso-639-1', exclude=('no', 'en'))

    """
    if base:
        if bcp47_case:
            forward_map = {}
            reverse_map = {}
            for key, val in TO_INTERNAL[base].iteritems():
                forward_map[convert_bcp47_case(key)] = val
            for key, val in FROM_INTERNAL[base].iteritems():
                reverse_map[key] = convert_bcp47_case(val)
        else:
            forward_map = TO_INTERNAL[base].copy()
            reverse_map = FROM_INTERNAL[base].copy()
        forward_map.update(mapping)

        if exclude:
            for c in exclude:
                del forward_map[c]

        reverse_map.update(_reverse_dict(mapping))
    else:
        forward_map = mapping
        reverse_map = _reverse_dict(mapping)

    TO_INTERNAL[standard] = forward_map
    FROM_INTERNAL[standard] = reverse_map

def add_standard_custom(standard, to_internal, from_internal):
    """Add a new standard to the list of supported standards with custom dicts.

    `to_internal` should be a dictionary mapping your custom standard's codes to
    the internal "universal" code used by this library.

    `from_internal` should be a dictionary mapping the internal "universal"
    codes to your custom standard's codes.

    """
    TO_INTERNAL[standard] = to_internal
    FROM_INTERNAL[standard] = from_internal

def _generate_initial_data():
    INTERNAL_NAMES.update({
        'aa': gettext_noop(u'Afar'),
        'ab': gettext_noop(u'Abkhazian'),
        'ae': gettext_noop(u'Avestan'),
        'aeb': gettext_noop(u'Tunisian Arabic'),
        'af': gettext_noop(u'Afrikaans'),
        'aka': gettext_noop(u'Akan'),
        'am': gettext_noop(u'Amharic'),
        'amh': gettext_noop(u'Amharic'),
        'ami': gettext_noop(u'Amis'),
        'an': gettext_noop(u'Aragonese'),
        'ar': gettext_noop(u'Arabic'),
        'arc': gettext_noop(u'Aramaic'),
        'arq': gettext_noop(u'Algerian Arabic'),
        'arz': gettext_noop(u'Egyptian Arabic'),
        'as': gettext_noop(u'Assamese'),
        'ase': gettext_noop(u'American Sign Language'),
        'ast': gettext_noop(u'Asturian'),
        'av': gettext_noop(u'Avaric'),
        'ay': gettext_noop(u'Aymara'),
        'az': gettext_noop(u'Azerbaijani'),
        'ba': gettext_noop(u'Bashkir'),
        'bam': gettext_noop(u'Bambara'),
        'be': gettext_noop(u'Belarusian'),
        'bem': gettext_noop(u'Bemba (Zambia)'),
        'ber': gettext_noop(u'Berber'),
        'bg': gettext_noop(u'Bulgarian'),
        'bh': gettext_noop(u'Bihari'),
        'bi': gettext_noop(u'Bislama'),
        'bn': gettext_noop(u'Bengali'),
        'bnt': gettext_noop(u'Ibibio'),
        'bo': gettext_noop(u'Tibetan'),
        'br': gettext_noop(u'Breton'),
        'bs': gettext_noop(u'Bosnian'),
        'bug': gettext_noop(u'Buginese'),
        'ca': gettext_noop(u'Catalan'),
        'cak': gettext_noop(u'Cakchiquel, Central'),
        'ce': gettext_noop(u'Chechen'),
        'ceb': gettext_noop(u'Cebuano'),
        'ch': gettext_noop(u'Chamorro'),
        'cho': gettext_noop(u'Choctaw'),
        'chr': gettext_noop(u'Cherokee'),
        'ckb': gettext_noop(u'Kurdish (Central)'),
        'cku': gettext_noop(u'Koasati'),
        'cly': gettext_noop(u'Eastern Chatino'),
        'cnh': gettext_noop(u'Hakha Chin'),
        'co': gettext_noop(u'Corsican'),
        'cr': gettext_noop(u'Cree'),
        'crs': gettext_noop(u'Seselwa Creole French'),
        'cs': gettext_noop(u'Czech'),
        'cta': gettext_noop(u'Tataltepec Chatino'),
        'ctd': gettext_noop(u'Chin, Tedim'),
        'ctu': gettext_noop(u'Chol, Tumbal\xe1'),
        'cu': gettext_noop(u'Church Slavic'),
        'cv': gettext_noop(u'Chuvash'),
        'cy': gettext_noop(u'Welsh'),
        'czn': gettext_noop(u'Zenzontepec Chatino'),
        'da': gettext_noop(u'Danish'),
        'de': gettext_noop(u'German'),
        'de-at': gettext_noop(u'German (Austria)'),
        'de-ch': gettext_noop(u'German (Switzerland)'),
        'din': gettext_noop(u'Dinka'),
        'dsb': gettext_noop('Lower Sorbian'),
        'dv': gettext_noop(u'Divehi'),
        'dz': gettext_noop(u'Dzongkha'),
        'ee': gettext_noop(u'Ewe'),
        'efi': gettext_noop(u'Efik'),
        'el': gettext_noop(u'Greek'),
        'en': gettext_noop(u'English'),
        'en-ca': gettext_noop(u'English (Canada)'),
        'en-gb': gettext_noop(u'English, British'),
        'en-ie': gettext_noop(u'English (Ireland)'),
        'en-us': gettext_noop(u'English (United States)'),
        'eo': gettext_noop(u'Esperanto'),
        'es': gettext_noop(u'Spanish'),
        'es-419': gettext_noop(u'Spanish (Latin America)'),
        'es-ar': gettext_noop(u'Spanish, Argentinian'),
        'es-ec': gettext_noop(u'Spanish (Ecuador)'),
        'es-es': gettext_noop('Spanish (Spain)'),
        'es-mx': gettext_noop(u'Spanish, Mexican'),
        'es-ni': gettext_noop(u'Spanish, Nicaraguan'),
        'et': gettext_noop(u'Estonian'),
        'eu': gettext_noop(u'Basque'),
        'fa': gettext_noop(u'Persian'),
        'fa-af': gettext_noop(u'Persian (Afghanistan)'),
        'ff': gettext_noop(u'Fulah'),
        'fi': gettext_noop(u'Finnish'),
        'fil': gettext_noop(u'Filipino'),
        'fj': gettext_noop(u'Fijian'),
        'fo': gettext_noop(u'Faroese'),
        'fr': gettext_noop(u'French'),
        'fr-be': gettext_noop(u'French (Belgium)'),
        'fr-ca': gettext_noop(u'French (Canada)'),
        'fr-ch': gettext_noop(u'French (Switzerland)'),
        'ful': gettext_noop(u'Fula'),
        'fy': gettext_noop('Western Frisian'),
        'fy-nl': gettext_noop(u'Frisian'),
        'ga': gettext_noop(u'Irish'),
        'gd': gettext_noop(u'Scottish Gaelic'),
        'gl': gettext_noop(u'Galician'),
        'gn': gettext_noop(u'Guaran'),
        'got': gettext_noop(u'Gothic'),
        'gsw': gettext_noop(u'Swiss German'),
        'gu': gettext_noop(u'Gujarati'),
        'gv': gettext_noop(u'Manx'),
        'ha': gettext_noop('Hausa'),
        'hai': gettext_noop(u'Haida'),
        'hau': gettext_noop(u'Hausa'),
        'haw': gettext_noop(u'Hawaiian'),
        'haz': gettext_noop(u'Hazaragi'),
        'hb': gettext_noop(u'HamariBoli (Roman Hindi-Urdu)'),
        'hch': gettext_noop(u'Huichol'),
        'he': gettext_noop(u'Hebrew'),
        'hi': gettext_noop(u'Hindi'),
        'hmm': gettext_noop(u'Hmong'),
        'ho': gettext_noop(u'Hiri Motu'),
        'hr': gettext_noop(u'Croatian'),
        'hsb': gettext_noop('Upper Sorbian'),
        'ht': gettext_noop(u'Creole, Haitian'),
        'hu': gettext_noop(u'Hungarian'),
        'hup': gettext_noop(u'Hupa'),
        'hus': gettext_noop(u'Huastec, Veracruz'),
        'hy': gettext_noop(u'Armenian'),
        'hz': gettext_noop(u'Herero'),
        'ia': gettext_noop(u'Interlingua'),
        'ibo': gettext_noop(u'Igbo'),
        'id': gettext_noop(u'Indonesian'),
        'ie': gettext_noop(u'Interlingue'),
        'ii': gettext_noop(u'Sichuan Yi'),
        'ik': gettext_noop(u'Inupia'),
        'ilo': gettext_noop(u'Ilocano'),
        'inh': gettext_noop(u'Ingush'),
        'io': gettext_noop(u'Ido'),
        'iro': gettext_noop(u'Iroquoian languages'),
        'is': gettext_noop(u'Icelandic'),
        'it': gettext_noop(u'Italian'),
        'iu': gettext_noop(u'Inuktitut'),
        'iw': gettext_noop('Hebrew'),
        'ja': gettext_noop(u'Japanese'),
        'jv': gettext_noop(u'Javanese'),
        'ka': gettext_noop(u'Georgian'),
        'kaa': gettext_noop(u'Karakalpak'),
        'kar': gettext_noop(u'Karen'),
        'kau': gettext_noop(u'Kanuri'),
        'kik': gettext_noop(u'Gikuyu'),
        'kin': gettext_noop(u'Rwandi'),
        'kj': gettext_noop(u'Kuanyama, Kwanyama'),
        'kk': gettext_noop(u'Kazakh'),
        'kl': gettext_noop(u'Greenlandic'),
        'km': gettext_noop(u'Khmer'),
        'kn': gettext_noop(u'Kannada'),
        'ko': gettext_noop(u'Korean'),
        'kon': gettext_noop(u'Kongo'),
        'ks': gettext_noop(u'Kashmiri'),
        'ksh': gettext_noop(u'Colognian'),
        'ku': gettext_noop(u'Kurdish'),
        'kv': gettext_noop(u'Komi'),
        'kw': gettext_noop(u'Cornish'),
        'ky': gettext_noop(u'Kyrgyz'),
        'la': gettext_noop(u'Latin'),
        'lb': gettext_noop(u'Luxembourgish'),
        'lg': gettext_noop(u'Ganda'),
        'li': gettext_noop(u'Limburgish'),
        'lin': gettext_noop(u'Lingala'),
        'lkt': gettext_noop(u'Lakota'),
        'lld': gettext_noop(u'Ladin'),
        'ln': gettext_noop('Lingala'),
        'lo': gettext_noop(u'Lao'),
        'lt': gettext_noop(u'Lithuanian'),
        'ltg': gettext_noop(u'Latgalian'),
        'lu': gettext_noop(u'Luba-Katagana'),
        'lua': gettext_noop(u'Luba-Kasai'),
        'luo': gettext_noop(u'Luo'),
        'lus': gettext_noop(u'Mizo'),
        'lut': gettext_noop(u'Lushootseed'),
        'luy': gettext_noop(u'Luhya'),
        'lv': gettext_noop(u'Latvian'),
        'mad': gettext_noop(u'Madurese'),
        'meta-audio': gettext_noop(u'Metadata: Audio Description'),
        'meta-geo': gettext_noop(u'Metadata: Geo'),
        'meta-tw': gettext_noop(u'Metadata: Twitter'),
        'meta-video': gettext_noop(u'Metadata: Video Description'),
        'meta-wiki': gettext_noop(u'Metadata: Wikipedia'),
        'mfe': gettext_noop('Mauritian Creole'),
        'mg': gettext_noop('Malagasy'),
        'mh': gettext_noop(u'Marshallese'),
        'mi': gettext_noop(u'Maori'),
        'mk': gettext_noop(u'Macedonian'),
        'ml': gettext_noop(u'Malayalam'),
        'mlg': gettext_noop(u'Malagasy'),
        'mn': gettext_noop(u'Mongolian'),
        'mni': gettext_noop(u'Manipuri'),
        'mnk': gettext_noop(u'Mandinka'),
        'mo': gettext_noop(u'Moldavian, Moldovan'),
        'moh': gettext_noop(u'Mohawk'),
        'mos': gettext_noop(u'Mossi'),
        'mr': gettext_noop(u'Marathi'),
        'ms': gettext_noop(u'Malay'),
        'mt': gettext_noop(u'Maltese'),
        'mus': gettext_noop(u'Muscogee'),
        'my': gettext_noop(u'Burmese'),
        'na': gettext_noop(u'Naurunan'),
        'nan': gettext_noop(u'Hokkien'),
        'nb': gettext_noop(u'Norwegian Bokmal'),
        'nci': gettext_noop(u'Nahuatl, Classical'),
        'ncj': gettext_noop(u'Nahuatl, Northern Puebla'),
        'nd': gettext_noop(u'North Ndebele'),
        'ne': gettext_noop(u'Nepali'),
        'ng': gettext_noop(u'Ndonga'),
        'nl': gettext_noop(u'Dutch'),
        'nl-be': gettext_noop(u'Dutch (Belgium)'),
        'nn': gettext_noop(u'Norwegian Nynorsk'),
        'no': gettext_noop(u'Norwegian'),
        'nr': gettext_noop(u'Southern Ndebele'),
        'nso': gettext_noop(u'Northern Sotho'),
        'nv': gettext_noop(u'Navajo'),
        'nya': gettext_noop(u'Chewa'),
        'oc': gettext_noop(u'Occitan'),
        'oji': gettext_noop(u'Ojibwe'),
        'om': gettext_noop('Oromo'),
        'or': gettext_noop(u'Oriya'),
        'orm': gettext_noop(u'Oromo'),
        'os': gettext_noop(u'Ossetian, Ossetic'),
        'pa': gettext_noop('Punjabi'),
        'pam': gettext_noop(u'Kapampangan'),
        'pan': gettext_noop(u'Punjabi'),
        'pap': gettext_noop(u'Papiamento'),
        'pcm': gettext_noop(u'Nigerian Pidgin'),
        'pi': gettext_noop(u'Pali'),
        'pl': gettext_noop(u'Polish'),
        'pnb': gettext_noop(u'Western Punjabi'),
        'prs': gettext_noop(u'Dari'),
        'ps': gettext_noop(u'Pashto'),
        'pt': gettext_noop(u'Portuguese'),
        'pt-br': gettext_noop(u'Portuguese, Brazilian'),
        'pt-pt': gettext_noop('Portuguese (Portugal)'),
        'qu': gettext_noop('Quechua'),
        'que': gettext_noop(u'Quechua'),
        'qvi': gettext_noop(u'Quichua, Imbabura Highland'),
        'raj': gettext_noop(u'Rajasthani'),
        'rar': gettext_noop(u'Cook Islands M\u0101ori'),
        'rm': gettext_noop(u'Romansh'),
        'rn': gettext_noop('Rundi'),
        'ro': gettext_noop(u'Romanian'),
        'ru': gettext_noop(u'Russian'),
        'run': gettext_noop(u'Rundi'),
        'rup': gettext_noop(u'Macedo'),
        'rw': gettext_noop('Kinyarwanda'),
        'ry': gettext_noop(u'Rusyn'),
        'sa': gettext_noop(u'Sanskrit'),
        'sc': gettext_noop(u'Sardinian'),
        'scn': gettext_noop(u'Sicilian'),
        'sco': gettext_noop(u'Scots'),
        'sd': gettext_noop(u'Sindhi'),
        'se': gettext_noop(u'Northern Sami'),
        'sg': gettext_noop(u'Sango'),
        'sgn': gettext_noop(u'Sign Languages'),
        'sh': gettext_noop(u'Serbo-Croatian'),
        'si': gettext_noop(u'Sinhala'),
        'sk': gettext_noop(u'Slovak'),
        'skx': gettext_noop(u'Seko Padang'),
        'sl': gettext_noop(u'Slovenian'),
        'sm': gettext_noop(u'Samoan'),
        'sn': gettext_noop('Shona'),
        'sna': gettext_noop(u'Shona'),
        'so': gettext_noop('Somali'),
        'som': gettext_noop(u'Somali'),
        'sot': gettext_noop(u'Sotho'),
        'sq': gettext_noop(u'Albanian'),
        'sr': gettext_noop(u'Serbian'),
        'sr-latn': gettext_noop(u'Serbian, Latin'),
        'srp': gettext_noop(u'Montenegrin'),
        'ss': gettext_noop(u'Swati'),
        'st': gettext_noop(u'Southern Sotho'),
        'su': gettext_noop(u'Sundanese'),
        'sv': gettext_noop(u'Swedish'),
        'sw': gettext_noop('Swahili'),
        'swa': gettext_noop(u'Swahili'),
        'szl': gettext_noop(u'Silesian'),
        'ta': gettext_noop(u'Tamil'),
        'tao': gettext_noop(u'Yami (Tao)'),
        'tar': gettext_noop(u'Tarahumara, Central'),
        'te': gettext_noop(u'Telugu'),
        'tet': gettext_noop(u'Tetum'),
        'tg': gettext_noop(u'Tajik'),
        'th': gettext_noop(u'Thai'),
        'ti': gettext_noop('Tigrinya'),
        'tir': gettext_noop(u'Tigrinya'),
        'tk': gettext_noop(u'Turkmen'),
        'tl': gettext_noop(u'Tagalog'),
        'tlh': gettext_noop(u'Klingon'),
        'tn': gettext_noop('Tswana'),
        'to': gettext_noop(u'Tonga'),
        'toj': gettext_noop(u'Tojolabal'),
        'tr': gettext_noop(u'Turkish'),
        'trv': gettext_noop(u'Seediq'),
        'ts': gettext_noop(u'Tsonga'),
        'tsn': gettext_noop(u'Tswana'),
        'tsz': gettext_noop(u'Purepecha'),
        'tt': gettext_noop(u'Tatar'),
        'tw': gettext_noop(u'Twi'),
        'ty': gettext_noop(u'Tahitian'),
        'tzh': gettext_noop(u'Tzeltal, Oxchuc'),
        'tzo': gettext_noop(u'Tzotzil, Venustiano Carranza'),
        'ug': gettext_noop(u'Uyghur'),
        'uk': gettext_noop(u'Ukrainian'),
        'umb': gettext_noop(u'Umbundu'),
        'ur': gettext_noop(u'Urdu'),
        'uz': gettext_noop(u'Uzbek'),
        've': gettext_noop(u'Venda'),
        'vi': gettext_noop(u'Vietnamese'),
        'vls': gettext_noop(u'Flemish'),
        'vo': gettext_noop(u'Volapuk'),
        'wa': gettext_noop(u'Walloon'),
        'wau': gettext_noop(u'Wauja'),
        'wbl': gettext_noop(u'Wakhi'),
        'wo': gettext_noop('Wolof'),
        'wol': gettext_noop(u'Wolof'),
        'xh': gettext_noop('Xhosa'),
        'xho': gettext_noop(u'Xhosa'),
        'yaq': gettext_noop(u'Yaqui'),
        'yi': gettext_noop(u'Yiddish'),
        'yo': gettext_noop('Yoruba'),
        'yor': gettext_noop(u'Yoruba'),
        'yua': gettext_noop(u'Maya, Yucat\xe1n'),
        'za': gettext_noop(u'Zhuang, Chuang'),
        'zam': gettext_noop(u'Zapotec, Miahuatl\xe1n'),
        'zh': gettext_noop(u'Chinese, Yue'),
        'zh-cn': gettext_noop(u'Chinese, Simplified'),
        'zh-hans': gettext_noop('Chinese (Simplified Han)'),
        'zh-hant': gettext_noop('Chinese (Traditional Han)'),
        'zh-hk': gettext_noop(u'Chinese, Traditional (Hong Kong)'),
        'zh-sg': gettext_noop(u'Chinese, Simplified (Singaporean)'),
        'zh-tw': gettext_noop(u'Chinese, Traditional'),
        'zu': gettext_noop('Zulu'),
        'zul': gettext_noop(u'Zulu'),
    })

def _add_iso_639_1():
    add_standard('iso-639-1', {
        'ab': 'ab',
        'aa': 'aa',
        'af': 'af',
        'ak': 'aka',
        'sq': 'sq',
        'am': 'amh',
        'ar': 'ar',
        'an': 'an',
        'hy': 'hy',
        'as': 'as',
        'av': 'av',
        'ae': 'ae',
        'ay': 'ay',
        'az': 'az',
        'bm': 'bam',
        'ba': 'ba',
        'eu': 'eu',
        'be': 'be',
        'bn': 'bn',
        'bh': 'bh',
        'bi': 'bi',
        'bs': 'bs',
        'br': 'br',
        'bg': 'bg',
        'my': 'my',
        'ca': 'ca',
        'km': 'km',
        'ch': 'ch',
        'ce': 'ce',
        'ny': 'nya',
        'zh': 'zh',
        'cu': 'cu',
        'cv': 'cv',
        'kw': 'kw',
        'co': 'co',
        'cr': 'cr',
        'hr': 'hr',
        'cs': 'cs',
        'da': 'da',
        'dv': 'dv',
        'nl': 'nl',
        'dz': 'dz',
        'en': 'en',
        'eo': 'eo',
        'et': 'et',
        'ee': 'ee',
        'fo': 'fo',
        'fj': 'fj',
        'fi': 'fi',
        'fr': 'fr',
        'ff': 'ff',
        'gl': 'gl',
        'lg': 'lg',
        'ka': 'ka',
        'de': 'de',
        'el': 'el',
        'gn': 'gn',
        'gu': 'gu',
        'ht': 'ht',
        'ha': 'hau',
        'he': 'he',
        'hz': 'hz',
        'hi': 'hi',
        'ho': 'ho',
        'hu': 'hu',
        'is': 'is',
        'io': 'io',
        'ig': 'ibo',
        'id': 'id',
        'ia': 'ia',
        'ie': 'ie',
        'iu': 'iu',
        'ik': 'ik',
        'ga': 'ga',
        'it': 'it',
        'ja': 'ja',
        'jv': 'jv',
        'kl': 'kl',
        'kn': 'kn',
        'kr': 'kau',
        'ks': 'ks',
        'kk': 'kk',
        'ki': 'kik',
        'rw': 'kin',
        'ky': 'ky',
        'kv': 'kv',
        'kg': 'kon',
        'ko': 'ko',
        'kj': 'kj',
        'ku': 'ku',
        'lo': 'lo',
        'la': 'la',
        'lv': 'lv',
        'li': 'li',
        'ln': 'lin',
        'lt': 'lt',
        'lu': 'lu',
        'lb': 'lb',
        'mk': 'mk',
        'mg': 'mlg',
        'ms': 'ms',
        'ml': 'ml',
        'mt': 'mt',
        'gv': 'gv',
        'mi': 'mi',
        'mr': 'mr',
        'mh': 'mh',
        'mo': 'mo',
        'mn': 'mn',
        'na': 'na',
        'nv': 'nv',
        'ng': 'ng',
        'ne': 'ne',
        'nd': 'nd',
        'se': 'se',
        'no': 'nb',
        'nb': 'nb',
        'nn': 'nn',
        'oc': 'oc',
        'oj': 'oji',
        'or': 'or',
        'om': 'orm',
        'os': 'os',
        'pi': 'pi',
        'pa': 'pa',
        'fa': 'fa',
        'pl': 'pl',
        'pt': 'pt',
        'ps': 'ps',
        'qu': 'que',
        'ro': 'ro',
        'rm': 'rm',
        'rn': 'run',
        'ru': 'ru',
        'ry': 'ry',
        'sm': 'sm',
        'sg': 'sg',
        'sa': 'sa',
        'sc': 'sc',
        'gd': 'gd',
        'sr': 'sr',
        'sh': 'sh',
        'sn': 'sna',
        'ii': 'ii',
        'sd': 'sd',
        'si': 'si',
        'sk': 'sk',
        'sl': 'sl',
        'so': 'som',
        'st': 'sot',
        'nr': 'nr',
        'es': 'es',
        'su': 'su',
        'sw': 'swa',
        'ss': 'ss',
        'sv': 'sv',
        'tl': 'tl',
        'ty': 'ty',
        'tg': 'tg',
        'ta': 'ta',
        'tt': 'tt',
        'te': 'te',
        'th': 'th',
        'bo': 'bo',
        'ti': 'tir',
        'to': 'to',
        'ts': 'ts',
        'tn': 'tsn',
        'tr': 'tr',
        'tk': 'tk',
        'tw': 'tw',
        'ug': 'ug',
        'uk': 'uk',
        'ur': 'ur',
        'uz': 'uz',
        've': 've',
        'vi': 'vi',
        'vo': 'vo',
        'wa': 'wa',
        'cy': 'cy',
        'fy': 'fy-nl',
        'wo': 'wol',
        'xh': 'xho',
        'yi': 'yi',
        'yo': 'yor',
        'za': 'za',
        'zu': 'zul',
    })

def _add_django():
    add_standard('django', {
        'ar': 'ar',
        'az': 'az',
        'bg': 'bg',
        'bn': 'bn',
        'bs': 'bs',
        'ca': 'ca',
        'cs': 'cs',
        'cy': 'cy',
        'da': 'da',
        'de': 'de',
        'el': 'el',
        'en': 'en',
        'en-gb': 'en-gb',
        'es': 'es',
        'es-ar': 'es-ar',
        'es-mx': 'es-mx',
        'es-ni': 'es-ni',
        'et': 'et',
        'eu': 'eu',
        'fa': 'fa',
        'fi': 'fi',
        'fr': 'fr',
        'fr-ca': 'fr-ca',
        'fy-nl': 'fy-nl',
        'ga': 'ga',
        'gl': 'gl',
        'he': 'he',
        'hi': 'hi',
        'hr': 'hr',
        'hu': 'hu',
        'id': 'id',
        'is': 'is',
        'it': 'it',
        'ja': 'ja',
        'ka': 'ka',
        'km': 'km',
        'kn': 'kn',
        'ko': 'ko',
        'lt': 'lt',
        'lv': 'lv',
        'mk': 'mk',
        'ml': 'ml',
        'mn': 'mn',
        'nl': 'nl',
        'nb': 'nb',
        'nn': 'nn',
        'pl': 'pl',
        'pt': 'pt',
        'pt-br': 'pt-br',
        'ro': 'ro',
        'ru': 'ru',
        'sk': 'sk',
        'sl': 'sl',
        'sq': 'sq',
        'sr': 'sr',
        'sr-latn': 'sr-latn',
        'sv': 'sv',
        'ta': 'ta',
        'te': 'te',
        'th': 'th',
        'tr': 'tr',
        'uk': 'uk',
        'ur': 'ur',
        'vi': 'vi',
        'zh-cn': 'zh-cn',
        'zh-tw': 'zh-tw',
    })

def _add_unisubs():
    add_standard('unisubs', {
        'aa': 'aa',
        'ab': 'ab',
        'ae': 'ae',
        'aeb': 'aeb',
        'af': 'af',
        'aka': 'aka',
        'amh': 'amh',
        'ami': 'ami',
        'an': 'an',
        'arc': 'arc',
        'arq': 'arq',
        'arz': 'arz',
        'as': 'as',
        'ase': 'ase',
        'ast': 'ast',
        'av': 'av',
        'ay': 'ay',
        'ba': 'ba',
        'bam': 'bam',
        'be': 'be',
        'bem': 'bem',
        'ber': 'ber',
        'bh': 'bh',
        'bi': 'bi',
        'bnt': 'bnt',
        'bo': 'bo',
        'br': 'br',
        'bug': 'bug',
        'cak': 'cak',
        'ce': 'ce',
        'ceb': 'ceb',
        'ch': 'ch',
        'cho': 'cho',
        'chr': 'chr',
        'ckb': 'ckb',
        'cku': 'cku',
        'cly': 'cly',
        'cnh': 'cnh',
        'co': 'co',
        'cr': 'cr',
        'crs': 'crs',
        'cta': 'cta',
        'ctu': 'ctu',
        'ctd': 'ctd',
        'cu': 'cu',
        'cv': 'cv',
        'czn': 'czn',
        'de-ch': 'de-ch',
        'dsb': 'dsb',
        'dv': 'dv',
        'dz': 'dz',
        'ee': 'ee',
        'efi': 'efi',
        'en-gb': 'en-gb',
        'eo': 'eo',
        'es-ar': 'es-ar',
        'ff': 'ff',
        'fil': 'fil',
        'fj': 'fj',
        'fo': 'fo',
        'fr-ca': 'fr-ca',
        'ful': 'ful',
        'ga': 'ga',
        'gd': 'gd',
        'gn': 'gn',
        'got': 'got',
        'gsw': 'gsw',
        'gu': 'gu',
        'gv': 'gv',
        'hai': 'hai',
        'hau': 'hau',
        'haw': 'haw',
        'haz': 'haz',
        'hb': 'hb',
        'hch': 'hch',
        'hmm': 'hmm',
        'ho': 'ho',
        'hsb': 'hsb',
        'ht': 'ht',
        'hup': 'hup',
        'hus': 'hus',
        'hy': 'hy',
        'hz': 'hz',
        'ia': 'ia',
        'ibo': 'ibo',
        'ie': 'ie',
        'ii': 'ii',
        'ik': 'ik',
        'ilo': 'ilo',
        'iro': 'iro',
        'inh': 'inh',
        'inh': 'inh',
        'io': 'io',
        'iro': 'iro',
        'iu': 'iu',
        'jv': 'jv',
        'kaa': 'kaa',
        'kar': 'kar',
        'kau': 'kau',
        'kik': 'kik',
        'kin': 'kin',
        'kj': 'kj',
        'kk': 'kk',
        'kl': 'kl',
        'kon': 'kon',
        'ks': 'ks',
        'ksh' : 'ksh',
        'ku': 'ku',
        'kv': 'kv',
        'kw': 'kw',
        'ky': 'ky',
        'la': 'la',
        'lld': 'lld',
        'lb': 'lb',
        'lg': 'lg',
        'li': 'li',
        'lin': 'lin',
        'lkt': 'lkt',
        'lo': 'lo',
        'ltg': 'ltg',
        'lu': 'lu',
        'lua': 'lua',
        'luo': 'luo',
        'lus': 'lus',
        'lut': 'lut',
        'luy': 'luy',
        'meta-audio':'meta-audio',
        'meta-geo': 'meta-geo',
        'meta-tw': 'meta-tw',
        'meta-video':'meta-video',
        'meta-wiki': 'meta-wiki',
        'mad': 'mad',
        'mfe': 'mfe',
        'mh': 'mh',
        'mi': 'mi',
        'ml': 'ml',
        'mlg': 'mlg',
        'mni': 'mni',
        'mnk': 'mnk',
        'mo': 'mo',
        'moh': 'moh',
        'mos': 'mos',
        'mr': 'mr',
        'ms': 'ms',
        'mt': 'mt',
        'mus': 'mus',
        'my': 'my',
        'na': 'na',
        'nan': 'nan',
        'nci': 'nci',
        'nd': 'nd',
        'ne': 'ne',
        'ng': 'ng',
        'nr': 'nr',
        'nso': 'nso',
        'nv': 'nv',
        'nya': 'nya',
        'oc': 'oc',
        'oji': 'oji',
        'or': 'or',
        'orm': 'orm',
        'os': 'os',
        'pam': 'pam',
        'pan': 'pan',
        'pap': 'pap',
        'pcm': 'pcm',
        'pi': 'pi',
        'pnb': 'pnb',
        'prs': 'prs',
        'ps': 'ps',
        'pt-br': 'pt-br',
        'que': 'que',
        'qvi': 'qvi',
        'raj': 'raj',
        'rar': 'rar',
        'rm': 'rm',
        'run': 'run',
        'rup': 'rup',
        'ry': 'ry',
        'sa': 'sa',
        'sc': 'sc',
        'scn': 'scn',
        'sco': 'sco',
        'sd': 'sd',
        'se': 'se',
        'sg': 'sg',
        'sgn': 'sgn',
        'skx': 'skx',
        'sh': 'sh',
        'si': 'si',
        'sm': 'sm',
        'sna': 'sna',
        'som': 'som',
        'sot': 'sot',
        'sr-latn': 'sr-latn',
        'srp': 'srp',
        'ss': 'ss',
        'su': 'su',
        'swa': 'swa',
        'szl': 'szl',
        'tao': 'tao',
        'tar': 'tar',
        'tet': 'tet',
        'tg': 'tg',
        'tir': 'tir',
        'tk': 'tk',
        'tl': 'tl',
        'tlh': 'tlh',
        'to': 'to',
        'toj': 'toj',
        'trv': 'trv',
        'ts': 'ts',
        'tsz': 'tsz',
        'tsn': 'tsn',
        'tzh': 'tzh',
        'tzo': 'tzo',
        'tt': 'tt',
        'tw': 'tw',
        'ty': 'ty',
        'ug': 'ug',
        'umb': 'umb',
        'uz': 'uz',
        've': 've',
        'vls': 'vls',
        'vo': 'vo',
        'wa': 'wa',
        'wau': 'wau',
        'wbl': 'wbl',
        'wol': 'wol',
        'xho': 'xho',
        'yaq': 'yaq',
        'yi': 'yi',
        'yor': 'yor',
        'yua': 'yua',
        'za': 'za',
        'zam': 'zam',
        'zh': 'zh',
        'zh-cn': 'zh-cn',
        'zh-tw': 'zh-tw',
        'zh-sg': 'zh-sg',
        'zh-hk': 'zh-hk',
        'zul': 'zul',
    }, base='django')

def _add_youtube_with_mapping():
    add_standard('youtube_with_mapping', {
        'ak': 'aka',
        'am': 'amh',
        'fy': 'fy-nl',
        'ha': 'hau',
        'ig': 'ibo',
        'iw': 'he',
        'mg': 'mlg',
        'no': 'nb',
        'ny': 'nya',
        'pa': 'pan',
        'pt-PT': 'pt',
        'rw': 'kin',
        'sn': 'sna',
        'so': 'som',
        'st': 'sot',
        'sw': 'swa',
        'ti': 'tir',
        'tn': 'tsn',
        'xh': 'xho',
        'yo': 'yor',
        'yue-HK': 'zh',
        'zh-Hans': 'zh-cn',
        'zh-Hant': 'zh-tw',
        'zu': 'zul',
    }, base='unisubs', bcp47_case=True)
    
def _add_youtube():
    add_standard('youtube', {},
                 base='unisubs', bcp47_case=True)

def _add_gettext():
    # translate locale names from our gettext directories to internal language
    # codes
    add_standard('gettext', {
        'az-az': 'az',
    }, base='unisubs')

def _add_bcp47():
    add_standard_custom('bcp47', StrictBCP47ToUnilangConverter(),
                        UNILANGS_TO_BCP47)
    add_standard_custom('bcp47-lossy', LossyBCP47ToUnilangConverter(),
                        UNILANGS_TO_BCP47)


_generate_initial_data()
_add_iso_639_1()
_add_django()
_add_unisubs()
_add_youtube()
_add_youtube_with_mapping()
_add_bcp47()
_add_gettext()

class LanguageCode(object):
    def __init__(self, language_code, standard):
        if standard == 'internal':
            self._code = language_code
            return
        try:
            standard_dict = TO_INTERNAL[standard.lower()]
        except KeyError:
            raise Exception("Standard '%s' is not registred" % standard)
        self._code = standard_dict[language_code]

    def to_internal(self):
        return self._code

    def encode(self, standard, fuzzy=False):
        """Return the code for this language in the given standard."""
        if fuzzy:
            return self._fuzzy_encode(standard)
        else:
            return FROM_INTERNAL[standard.lower()][self._code]

    def _fuzzy_encode(self, standard):
        """Return the code or closest approximate for this language in the given standard.

        This will try harder than the `encode()` function, but may result in
        data loss.  For example:

            >>> lc = LanguageCode('en-gb', 'django')

            >>> lc.name()
            'British English'

            >>> lc.encode('iso-639-1')
            KeyError...

            >>> lc.fuzzy_encode('iso-639-1')
            'en'

        Here's an example of how you can lose data:

            >>> original = 'en-gb'                           # Start with 'en-gb'
            >>> lc = LanguageCode(original, 'django')        # Decode as Django
            >>> new_lang = lc.fuzzy_encode('iso-639-1')      # Fuzzy encode to ISO-639-1
            >>> new_lc = LanguageCode(new_lang, 'iso-639-1') # Decode as ISO-639-1
            >>> result = new_lc.encode('django')             # Encode back to Django
            >>> assert original != result

        """
        # TODO: This.
        return

    def name(self):
        """Return the English name for this language as a unicode string.

        Note: The strings returned from this function have already been marked
        with gettext_noop, so they should be safe to use with gettext to
        translate into another language.

        """
        return INTERNAL_NAMES[self._code]

    def aliases(self):
        """Return the "aliases" for this language code.

        This is easiest to describe with an example:

            >>> LanguageCode('en', 'iso-639-1').aliases()
            { 'iso-639-1': 'en',
              'iso-639-2': 'eng',
              'django': 'en',
              # ...
            }
        """
        standards = FROM_INTERNAL.keys()
        return dict([(standard, FROM_INTERNAL[standard][self._code])
                     for standard in standards
                     if FROM_INTERNAL[standard].get(self._code)])


def get_language_name_mapping(standard):
    """Return a dict of code -> english name for all languages in the standard."""
    if standard == 'internal':
        return dict((code, name) for code, name in INTERNAL_NAMES.items())
    else:
        return dict((code, LanguageCode(code, standard).name())
                for code in TO_INTERNAL.get(standard))

def get_language_code_mapping(standard):
    """Return a dict of code -> LanguageCode for all languages in the standard."""
    return dict((code, LanguageCode(code, standard))
                for code in TO_INTERNAL.get(standard))


def _debug_missing_languages(standard):
    """Return a list of all the languages missing from the given standard."""
    return [(internal_code, name)
            for internal_code, name in INTERNAL_NAMES.items()
            if internal_code not in FROM_INTERNAL]

def _debug_missing_language_codes(standard, reference_standard='unisubs'):
    """
    Return a list of all the languages codes missing from the given standard
    """
    unisubs_langs  = set(get_language_code_mapping(reference_standard).keys())
    standard_langs = set()
    [standard_langs.add(LanguageCode(lc, standard).encode(reference_standard)) \
     for lc in get_language_code_mapping(standard).keys()]
    return list(unisubs_langs.difference(standard_langs))

