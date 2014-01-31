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


# INTERNAL_NAMES stores the English and native names for the various languages.
#
# Code -> (English name, Native name)
#
# { 'ar': (u'Arabic', u'العربية'),
#   'el': (u'Greek', u'Ελληνικά'),
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

def add_standard(standard, mapping, base=None, exclude=None):
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
        m = copy.copy(TO_INTERNAL[base])
        m.update(mapping)

        if exclude:
            for c in exclude:
                del m[c]
    else:
        m = mapping

    TO_INTERNAL[standard] = m
    FROM_INTERNAL[standard] = _reverse_dict(m)

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
        'aa': (gettext_noop(u'Afar'), u'Afar'),
        'ab': (gettext_noop(u'Abkhazian'), u'Abkhazian'),
        'ae': (gettext_noop(u'Avestan'), u'Avestan'),
        'af': (gettext_noop(u'Afrikaans'), u'Afrikaans'),
        'aka': (gettext_noop(u'Akan'), u'Akana'),
        'amh': (gettext_noop(u'Amharic'), u'Amharic'),
        'an': (gettext_noop(u'Aragonese'), u'Aragonés'),
        'ar': (gettext_noop(u'Arabic'), u'العربية'),
        'arc': (gettext_noop(u'Aramaic'), u'ܐܪܡܝܐ'),
        'arq': (gettext_noop(u'Algerian Arabic'), u'دزيري/جزائري'),
        'as': (gettext_noop(u'Assamese'), u'Assamese'),
        'ase': (gettext_noop(u'American Sign Language'), u'American Sign Language'),
        'ast': (gettext_noop(u'Asturian'), u'Asturianu'),
        'av': (gettext_noop(u'Avaric'), u'Авар'),
        'ay': (gettext_noop(u'Aymara'), u'Aymar'),
        'az': (gettext_noop(u'Azerbaijani'), u'Azərbaycan'),
        'ba': (gettext_noop(u'Bashkir'), u'Башҡорт'),
        'bam': (gettext_noop(u'Bambara'), u'Bamanankan'),
        'be': (gettext_noop(u'Belarusian'), u'Беларуская'),
        'ber': (gettext_noop(u'Berber'), u'Berber'),
        'bg': (gettext_noop(u'Bulgarian'), u'Български'),
        'bh': (gettext_noop(u'Bihari'), u'भोजपुर'),
        'bi': (gettext_noop(u'Bislama'), u'Bislama'),
        'bn': (gettext_noop(u'Bengali'), u'Bengali'),
        'bnt': (gettext_noop(u'Ibibio'), u'Ibibio'),
        'bo': (gettext_noop(u'Tibetan'), u'Bod skad'),
        'br': (gettext_noop(u'Breton'), u'Brezhoneg'),
        'bs': (gettext_noop(u'Bosnian'), u'Bosanski'),
        'bug': (gettext_noop(u'Buginese'), u'Basa Ugi'),
        'ca': (gettext_noop(u'Catalan'), u'Català'),
        'cak': (gettext_noop(u'Cakchiquel, Central'), u'Cakchiquel, Central'),
        'ce': (gettext_noop(u'Chechen'), u'Chechen'),
        'ceb': (gettext_noop(u'Cebuano'), u'Cebuano'),
        'ch': (gettext_noop(u'Chamorro'), u'Chamoru'),
        'cho': (gettext_noop(u'Choctaw'), u'Choctaw'),
        'co': (gettext_noop(u'Corsican'), u'Corsu'),
        'cr': (gettext_noop(u'Cree'), u'Nehiyaw'),
        'cs': (gettext_noop(u'Czech'), u'Čeština'),
        'ctu': (gettext_noop(u'Chol, Tumbalá'), u'Chol, Tumbalá'),
        'ctd': (gettext_noop(u'Chin, Tedim'), u'Chin, Tedim'),
        'cu': (gettext_noop(u'Church Slavic'), u'Church Slavic'),
        'cv': (gettext_noop(u'Chuvash'), u'Chuvash'),
        'cy': (gettext_noop(u'Welsh'), u'Cymraeg'),
        'da': (gettext_noop(u'Danish'), u'Dansk'),
        'de': (gettext_noop(u'German'), u'Deutsch'),
        'dv': (gettext_noop(u'Divehi'), u'Divehi'),
        'dz': (gettext_noop(u'Dzongkha'), u'Dzongkha'),
        'ee': (gettext_noop(u'Ewe'), u'Ewe'),
        'efi': (gettext_noop(u'Efik'), u'Efik'),
        'el': (gettext_noop(u'Greek'), u'Ελληνικά'),
        'en': (gettext_noop(u'English'), u'English'),
        'en-gb': (gettext_noop(u'English, British'), u'English, British'),
        'eo': (gettext_noop(u'Esperanto'), u'Esperanto'),
        'es': (gettext_noop(u'Spanish'), u'Español'),
        'es-ar': (gettext_noop(u'Spanish, Argentinian'), u'Spanish, Argentinian'),
        'es-mx': (gettext_noop(u'Spanish, Mexican'), u'Spanish, Mexican'),
        'es-ni': (gettext_noop(u'Spanish, Nicaraguan'), u'Spanish, Nicaraguan, '),
        'et': (gettext_noop(u'Estonian'), u'Eesti'),
        'eu': (gettext_noop(u'Basque'), u'Euskara'),
        'fa': (gettext_noop(u'Persian'), u'فارسی'),
        'ff': (gettext_noop(u'Fulah'), u'Fulah'),
        'fi': (gettext_noop(u'Finnish'), u'Suomi'),
        'fil': (gettext_noop(u'Filipino'), u'Filipino'),
        'fj': (gettext_noop(u'Fijian'), u'Na Vosa Vakaviti'),
        'fo': (gettext_noop(u'Faroese'), u'Føroyskt'),
        'fr': (gettext_noop(u'French'), u'Français'),
        'fr-ca': (gettext_noop(u'French, Canadian'), u'French, Canadian'),
        'ful': (gettext_noop(u'Fula'), u'Fula'),
        'fy-nl': (gettext_noop(u'Frisian'), u'Frysk'),
        'ga': (gettext_noop(u'Irish'), u'Gaeilge'),
        'gd': (gettext_noop(u'Scottish Gaelic'), u'Gàidhlig'),
        'gl': (gettext_noop(u'Galician'), u'Galego'),
        'gn': (gettext_noop(u'Guaran'), u'Avañe\'ẽ'),
        'gu': (gettext_noop(u'Gujarati'), u'ગુજરાતી'),
        'gv': (gettext_noop(u'Manx'), u'Gaelg'),
        'hai': (gettext_noop(u'Haida'), u'Haida'),
        'hau': (gettext_noop(u'Hausa'), u'هَوُسَ'),
        'haz': (gettext_noop(u'Hazaragi'), u'هزارگی'),
        'hch': (gettext_noop(u'Huichol'), u'Huichol'),
        'he': (gettext_noop(u'Hebrew'), u'עברית'),
        'hi': (gettext_noop(u'Hindi'), u'हिन्दी'),
        'ho': (gettext_noop(u'Hiri Motu'), u'Hiri Motu'),
        'hr': (gettext_noop(u'Croatian'), u'Hrvatski'),
        'ht': (gettext_noop(u'Creole, Haitian'), u'Creole, Haitian'),
        'hu': (gettext_noop(u'Hungarian'), u'Magyar'),
        'hup': (gettext_noop(u'Hupa'), u'Hupa'),
        'hus': (gettext_noop(u'Huastec, Veracruz'), u'Huastec, Veracruz'),
        'hy': (gettext_noop(u'Armenian'), u'Հայերեն'),
        'hz': (gettext_noop(u'Herero'), u'Herero'),
        'ia': (gettext_noop(u'Interlingua'), u'Interlingua'),
        'ibo': (gettext_noop(u'Igbo'), u'Igbo'),
        'id': (gettext_noop(u'Indonesian'), u'Bahasa Indonesia'),
        'ie': (gettext_noop(u'Interlingue'), u'Interlingue'),
        'ii': (gettext_noop(u'Sichuan Yi'), u'Sichuan Yi'),
        'ik': (gettext_noop(u'Inupia'), u'Iñupiak'),
        'ilo': (gettext_noop(u'Ilocano'), u'Ilocano'),
        'inh': (gettext_noop(u'Ingush'), u'Ingush'),
        'io': (gettext_noop(u'Ido'), u'Ido'),
        'iro': (gettext_noop(u'Iroquoian languages'), u'Iroquoian languages'),
        'is': (gettext_noop(u'Icelandic'), u'Íslenska'),
        'it': (gettext_noop(u'Italian'), u'Italiano'),
        'iu': (gettext_noop(u'Inuktitut'), u'Inuktitut'),
        'ja': (gettext_noop(u'Japanese'), u'日本語'),
        'jv': (gettext_noop(u'Javanese'), u'Basa Jawa'),
        'ka': (gettext_noop(u'Georgian'), u'ქართული'),
        'kar': (gettext_noop(u'Karen'), u'Karen'),
        'kau': (gettext_noop(u'Kanuri'), u'Kanuri'),
        'kik': (gettext_noop(u'Gikuyu'), u'Gikuyu'),
        'kin': (gettext_noop(u'Rwandi'), u'Kinyarwanda'),
        'kj': (gettext_noop(u'Kuanyama, Kwanyama'), u'Kuanyama, Kwanyama'),
        'kk': (gettext_noop(u'Kazakh'), u'қазақша'),
        'kl': (gettext_noop(u'Greenlandic'), u'Kalaallisut'),
        'km': (gettext_noop(u'Khmer'), u'Khmer'),
        'kn': (gettext_noop(u'Kannada'), u'ಕನ್ನಡ'),
        'ko': (gettext_noop(u'Korean'), u'한국어'),
        'kon': (gettext_noop(u'Kongo'), u'Kongo'),
        'ks': (gettext_noop(u'Kashmiri'), u'कश्मीरी - (كشميري'),
        'ksh': (gettext_noop(u'Colognian'), u'Kölsch'),
        'ku': (gettext_noop(u'Kurdish'), u'Kurdî / كوردی'),
        'kv': (gettext_noop(u'Komi'), u'Komi'),
        'kw': (gettext_noop(u'Cornish'), u'Kernewek/Karnuack'),
        'ky': (gettext_noop(u'Kyrgyz'), u'Kırgızca'),
        'la': (gettext_noop(u'Latin'), u'Latina'),
        'ltg': (gettext_noop(u'Latgalian'), u'Latgalian'),
        'lld': (gettext_noop(u'Ladin'), u'Ladino'),
        'lb': (gettext_noop(u'Luxembourgish'), u'Lëtzebuergesch'),
        'lg': (gettext_noop(u'Ganda'), u'Ganda'),
        'li': (gettext_noop(u'Limburgish'), u'Limburgs'),
        'lin': (gettext_noop(u'Lingala'), u'Lingala'),
        'lkt': (gettext_noop(u'Lakota'), u'Lakota'),
        'lo': (gettext_noop(u'Lao'), u'Lao'),
        'lt': (gettext_noop(u'Lithuanian'), u'Lietuvių'),
        'lu': (gettext_noop(u'Luba-Katagana'), u'Luba-Katagana'),
        'lua': (gettext_noop(u'Luba-Kasai'), u'Luba-Kasai'),
        'luo': (gettext_noop(u'Luo'), u'Luo'),
        'luy': (gettext_noop(u'Luhya'), u'Luhya'),
        'lv': (gettext_noop(u'Latvian'), u'Latviešu'),
        'meta-audio': (gettext_noop(u'Metadata: Audio Description'), u'Metadata: Audio Description'),
        'meta-geo': (gettext_noop(u'Metadata: Geo'), u'Metadata: Geo'),
        'meta-tw': (gettext_noop(u'Metadata: Twitter'), u'Metadata: Twitter'),
        'meta-wiki': (gettext_noop(u'Metadata: Wikipedia'), u'Metadata: Wikipedia'),
        'mad': (gettext_noop(u'Madurese'), u'Madurese'),
        'mh': (gettext_noop(u'Marshallese'), u'Ebon'),
        'mi': (gettext_noop(u'Maori'), u'Māori'),
        'mk': (gettext_noop(u'Macedonian'), u'Македонски'),
        'ml': (gettext_noop(u'Malayalam'), u'Malayalam'),
        'mlg': (gettext_noop(u'Malagasy'), u'Malagasy'),
        'mn': (gettext_noop(u'Mongolian'), u'Монгол'),
        'mnk': (gettext_noop(u'Mandinka'), u'Mandinka'),
        'mo': (gettext_noop(u'Moldavian, Moldovan'), u'Moldoveana'),
        'moh': (gettext_noop(u'Mohawk'), u'Mohawk'),
        'mni': (gettext_noop(u'Manipuri'), u'মৈইতৈইলোন'),
        'mos': (gettext_noop(u'Mossi'), u'Mossi'),
        'mr': (gettext_noop(u'Marathi'), u'मराठी'),
        'ms': (gettext_noop(u'Malay'), u'Bahasa Melayu'),
        'mt': (gettext_noop(u'Maltese'), u'bil-Malti'),
        'mus': (gettext_noop(u'Muscogee'), u'Muscogee'),
        'my': (gettext_noop(u'Burmese'), u'Myanmasa'),
        'nan': (gettext_noop(u'Hokkien'), u'Hokkien'),
        'na': (gettext_noop(u'Naurunan'), u'dorerin Naoero'),
        'nb': (gettext_noop(u'Norwegian Bokmal'), u'Norsk Bokmål'),
        'nci': (gettext_noop(u'Nahuatl, Classical'), u'Nahuatl, Classical'),
        'ncj': (gettext_noop(u'Nahuatl, Northern Puebla'), u'Nahuatl, Northern Puebla'),
        'nd': (gettext_noop(u'North Ndebele'), u'North Ndebele'),
        'ne': (gettext_noop(u'Nepali'), u'नेपाली'),
        'ng': (gettext_noop(u'Ndonga'), u'Ndonga'),
        'nl': (gettext_noop(u'Dutch'), u'Nederlands'),
        'nn': (gettext_noop(u'Norwegian Nynorsk'), u'Nynorsk'),
        'no': (gettext_noop(u'Norwegian'), u'Norwegian'),
        'nr': (gettext_noop(u'Southern Ndebele'), u'Southern Ndebele'),
        'nso': (gettext_noop(u'Northern Sotho'), u'Northern Sotho'),
        'nv': (gettext_noop(u'Navajo'), u'Navajo'),
        'nya': (gettext_noop(u'Chewa'), u'Chewa'),
        'oc': (gettext_noop(u'Occitan'), u'Occitan'),
        'oji': (gettext_noop(u'Ojibwe'), u'Ojibwe'),
        'or': (gettext_noop(u'Oriya'), u'Oriya'),
        'orm': (gettext_noop(u'Oromo'), u'Oromoo'),
        'os': (gettext_noop(u'Ossetian, Ossetic'), u'Ossetian, Ossetic'),
        'pam': (gettext_noop(u'Kapampangan'), u'Pampango'),
        'pap': (gettext_noop(u'Papiamento'), u'Papiamentu'),
        'pan': (gettext_noop(u'Eastern Punjabi'), u'ਪੰਜਾਬੀ'),
        'pi': (gettext_noop(u'Pali'), u'पािऴ'),
        'pl': (gettext_noop(u'Polish'), u'Polski'),
        'pnb': (gettext_noop(u'Western Punjabi'), u'پنجابی'),
        'prs': (gettext_noop(u'Dari'), u'دری'),
        'ps': (gettext_noop(u'Pashto'), u'پښتو'),
        'pt': (gettext_noop(u'Portuguese'), u'Português'),
        'pt-br': (gettext_noop(u'Portuguese, Brazilian'), u'Portuguese, Brazilian'),
        'que': (gettext_noop(u'Quechua'), u'Runa Simi'),
        'qvi': (gettext_noop(u'Quichua, Imbabura Highland'), u'Quichua, Imbabura Highland'),
        'raj': (gettext_noop(u'Rajasthani'), u'राजस्थानी'),
        'rm': (gettext_noop(u'Romansh'), u'Rumantsch'),
        'ro': (gettext_noop(u'Romanian'), u'Română'),
        'ru': (gettext_noop(u'Russian'), u'Русский'),
        'run': (gettext_noop(u'Rundi'), u'Kirundi'),
        'rup': (gettext_noop(u'Macedo'), u'Macedo'),
        'ry': (gettext_noop(u'Rusyn'), u'Rusyn'),
        'sa': (gettext_noop(u'Sanskrit'), u'संस्कृतम्'),
        'sc': (gettext_noop(u'Sardinian'), u'Sardu'),
        'sco': (gettext_noop(u'Scots'), u'Scots'),
        'sd': (gettext_noop(u'Sindhi'), u'سنڌي'),
        'se': (gettext_noop(u'Northern Sami'), u'Northern Sami'),
        'sg': (gettext_noop(u'Sango'), u'Sängö'),
        'sgn': (gettext_noop(u'Sign Languages'), u'Sign Languages'),
        'sh': (gettext_noop(u'Serbo-Croatian'), u'Srpskohrvatski'),
        'si': (gettext_noop(u'Sinhala'), u'Sinhalese'),
        'sk': (gettext_noop(u'Slovak'), u'Slovenčina'),
        'skx': (gettext_noop(u'Seko Padang'), u'Sua Tu Padang'),
        'sl': (gettext_noop(u'Slovenian'), u'Slovenščina'),
        'sm': (gettext_noop(u'Samoan'), u'Gagana Samoa'),
        'sna': (gettext_noop(u'Shona'), u'chiShona'),
        'som': (gettext_noop(u'Somali'), u'Soomaaliga'),
        'sot': (gettext_noop(u'Sotho'), u'seSotho'),
        'sq': (gettext_noop(u'Albanian'), u'Shqip'),
        'sr': (gettext_noop(u'Serbian'), u'Српски / Srpski'),
        'sr-latn': (gettext_noop(u'Serbian, Latin'), u'Serbian, Latin'),
        'srp': (gettext_noop(u'Montenegrin'), u'Crnogorski jezik, Црногорски језик'),
        'ss': (gettext_noop(u'Swati'), u'SiSwati'),
        'su': (gettext_noop(u'Sundanese'), u'Basa Sunda'),
        'sv': (gettext_noop(u'Swedish'), u'Svenska'),
        'swa': (gettext_noop(u'Swahili'), u'Kiswahili'),
        'szl': (gettext_noop(u'Silesian'), u'ślōnskŏ gŏdka'),
        'ta': (gettext_noop(u'Tamil'), u'தமிழ்'),
        'tar': (gettext_noop(u'Tarahumara, Central'), u'Ralámul'),
        'tet': (gettext_noop(u'Tetum'), u'Tetum'),
        'te': (gettext_noop(u'Telugu'), u'తెలుగు'),
        'tg': (gettext_noop(u'Tajik'), u'Тоҷикӣ'),
        'th': (gettext_noop(u'Thai'), u'ไทย'),
        'tir': (gettext_noop(u'Tigrinya'), u'Tigrinya'),
        'tk': (gettext_noop(u'Turkmen'), u'تركمن / Туркмен'),
        'tl': (gettext_noop(u'Tagalog'), u'Tagalog'),
        'tlh': (gettext_noop(u'Klingon'), u'tlhIngan-Hol'),
        'to': (gettext_noop(u'Tonga'), u'faka Tonga'),
        'toj': (gettext_noop(u'Tojolabal'), u'Tojolabal'),
        'tr': (gettext_noop(u'Turkish'), u'Türkçe'),
        'ts': (gettext_noop(u'Tsonga'), u'Xitsonga'),
        'tsn': (gettext_noop(u'Tswana'), u'Setswana'),
        'tsz': (gettext_noop(u'Purepecha'), u'Purepecha'),
        'tt': (gettext_noop(u'Tartar'), u'Tatarça / Татарча'),
        'tw': (gettext_noop(u'Twi'), u'Twi'),
        'ty': (gettext_noop(u'Tahitian'), u'Tahitian'),
        'tzh': (gettext_noop(u'Tzeltal, Oxchuc'), u'Tzeltal, Oxchuc'),
        'tzo': (gettext_noop(u'Tzotzil, Venustiano Carranza'), 
                             u'Tzotzil, Venustiano Carranza'),
        'uk': (gettext_noop(u'Ukrainian'), u'Українська'),
        'umb': (gettext_noop(u'Umbundu'), u'Umbundu'),
        'ug': (gettext_noop(u'Uyghur'), u'ئۇيغۇر'),
        'ur': (gettext_noop(u'Urdu'), u'اڙدو'),
        'uz': (gettext_noop(u'Uzbek'), u'O‘zbek'),
        've': (gettext_noop(u'Venda'), u'Venda'),
        'vi': (gettext_noop(u'Vietnamese'), u'Tiếng Việt'),
        'vls': (gettext_noop(u'Flemish'), u'Vlaams'),
        'vo': (gettext_noop(u'Volapuk'), u'Volapük'),
        'wa': (gettext_noop(u'Walloon'), u'Walon'),
        'wbl': (gettext_noop(u'Wakhi'), u'Wakhi'),
        'wol': (gettext_noop(u'Wolof'), u'Wollof'),
        'xho': (gettext_noop(u'Xhosa'), u'isiXhosa'),
        'yaq': (gettext_noop(u'Yaqui'), u'Yaqui'),
        'yi': (gettext_noop(u'Yiddish'), u'ייִדיש'),
        'yor': (gettext_noop(u'Yoruba'), u'Yorùbá'),
        'yua': (gettext_noop(u'Maya, Yucatán'), u'Maya, Yucatán'),
        'za': (gettext_noop(u'Zhuang, Chuang'), u'Cuengh'),
        'zam': (gettext_noop(u'Zapotec, Miahuatlán'), u'Zapotec, Miahuatlán'),
        'zh': (gettext_noop(u'Chinese, Yue'), u'中文'),
        'zh-cn': (gettext_noop(u'Chinese, Simplified'), u'简体中文'),
        'zh-tw': (gettext_noop(u'Chinese, Traditional'), u'繁體中文'),
        'zh-sg': (gettext_noop(u'Chinese, Simplified (Singaporean)'), u''),
        'zh-hk': (gettext_noop(u'Chinese, Traditional (Hong Kong)'), u''),
        'zul': (gettext_noop(u'Zulu'), u'isiZulu'),
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
        'af': 'af',
        'aka': 'aka',
        'amh': 'amh',
        'an': 'an',
        'arc': 'arc',
        'arq': 'arq',
        'as': 'as',
        'ase': 'ase',
        'ast': 'ast',
        'av': 'av',
        'ay': 'ay',
        'ba': 'ba',
        'bam': 'bam',
        'be': 'be',
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
        'co': 'co',
        'cr': 'cr',
        'ctu': 'ctu',
        'ctd': 'ctd',
        'cu': 'cu',
        'cv': 'cv',
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
        'gu': 'gu',
        'gv': 'gv',
        'hai': 'hai',
        'hau': 'hau',
        'haz': 'haz',
        'hch': 'hch',
        'ho': 'ho',
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
        'luy': 'luy',
        'meta-audio':'meta-audio',
        'meta-geo': 'meta-geo',
        'meta-tw': 'meta-tw',
        'meta-wiki': 'meta-wiki',
        'mad': 'mad',
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
        'pi': 'pi',
        'pnb': 'pnb',
        'prs': 'prs',
        'ps': 'ps',
        'pt-br': 'pt-br',
        'que': 'que',
        'qvi': 'qvi',
        'raj': 'raj',
        'rm': 'rm',
        'run': 'run',
        'rup': 'rup',
        'ry': 'ry',
        'sa': 'sa',
        'sc': 'sc',
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
        'tar': 'tar',
        'tet': 'tet',
        'tg': 'tg',
        'tir': 'tir',
        'tk': 'tk',
        'tl': 'tl',
        'tlh': 'tlh',
        'to': 'to',
        'toj': 'toj',
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

def _add_youtube():
    add_standard('youtube', {
        'aa': 'aa',
        'ab': 'ab',
        'ae': 'ae',
        'af': 'af',
        'ak': 'aka',
        'am': 'amh',
        'an': 'an',
        'ar': 'ar',
        'as': 'as',
        'ast': 'ast',
        'av': 'av',
        'ay': 'ay',
        'az': 'az',
        'ba': 'ba',
        'bm': 'bam',
        'ber': 'ber',
        'be': 'be',
        'bg': 'bg',
        'bh': 'bh',
        'bi': 'bi',
        'bn': 'bn',
        'bnt': 'bnt',
        'bo': 'bo',
        'br': 'br',
        'bs': 'bs',
        'ce': 'ce',
        'ceb': 'ceb',
        'ca': 'ca',
        'ch': 'ch',
        'cho': 'cho',
        'co': 'co',
        'cr': 'cr',
        'cs': 'cs',
        'cu': 'cu',
        'cv': 'cv',
        'cy': 'cy',
        'da': 'da',
        'de': 'de',
        'dv': 'dv',
        'dz': 'dz',
        'ee': 'ee',
        'efi': 'efi',
        'el': 'el',
        'en': 'en',
        'en-GB': 'en-gb',
        'en-US': 'en',
        'eo': 'eo',
        'es-AR': 'es-ar',
        'es-ES': 'es',
        'es-NI': 'es-ni',
        'es-MX': 'es-mx',
        'et': 'et',
        'eu': 'eu',
        'fa': 'fa',
        'fa-AF': 'fa',
        'fi': 'fi',
        'fil': 'fil',
        'ff': 'ff',
        'fj': 'fj',
        'fo': 'fo',
        'fr': 'fr',
        'fr-CA': 'fr-ca',
        'fy': 'fy-nl',
        'ga': 'ga',
        'gd': 'gd',
        'gl': 'gl',
        'gn': 'gn',
        'gu': 'gu',
        'gv': 'gv',
        'ha': 'hau',
        'hai': 'hai',
        'hi': 'hi',
        'ho': 'ho',
        'hr': 'hr',
        'hu': 'hu',
        'ht': 'ht',
        'hup': 'hup',
        'hy': 'hy',
        'hz': 'hz',
        'ia': 'ia',
        'id': 'id',
        'ie': 'ie',
        'ig': 'ibo',
        'ii': 'ii',
        'ik': 'ik',
        'ilo': 'ilo',
        'inh': 'inh',
        'io': 'io',
        'iu': 'iu',
        'iro': 'iro',
        'is': 'is',
        'it': 'it',
        'iw': 'he',
        'ja': 'ja',
        'jv': 'jv',
        'ka': 'ka',
        'kar': 'kar',
        'kg': 'kon',
        'ki': 'kik',
        'kk': 'kk',
        'kj': 'kj',
        'kl': 'kl',
        'km': 'km',
        'kn': 'kn',
        'ko': 'ko',
        'ks': 'ks',
        'ksh': 'ksh',
        'kr': 'kau',
        'ku': 'ku',
        'ky': 'ky',
        'kv': 'kv',
        'kw': 'kw',
        'la': 'la',
        'lb': 'lb',
        'lg': 'lg',
        'li': 'li',
        'lld': 'lld',
        'ln': 'lin',
        'lo': 'lo',
        'lt': 'lt',
        'lu': 'lu',
        'lua': 'lua',
        'luo': 'luo',
        'luy': 'luy',
        'lv': 'lv',
        'mad': 'mad',
        'mg': 'mlg',
        'mh': 'mh',
        'mi': 'mi',
        'mk': 'mk',
        'ml': 'ml',
        'mn': 'mn',
        'mni': 'mni',
        'mo': 'mo',
        'moh': 'moh',
        'mos': 'mos',
        'mr': 'mr',
        'ms': 'ms',
        'mt': 'mt',
        'my': 'my',
        'na': 'na',
        'nd': 'nd',
        'ne': 'ne',
        'ng': 'ng',
        'nl': 'nl',
        'nl-BE': 'nl',
        'nn': 'nn',
        'no': 'nb',
        'nb': 'nb',
        'nr': 'nr',
        'nso': 'nso',
        'nv': 'nv',
        'ny': 'nya',
        'oc': 'oc',
        'oj': 'oji',
        'om': 'orm',
        'or': 'or',
        'os': 'os',
        'pa': 'pa',
        'pap': 'pap',
        'pi': 'pi',
        'pl': 'pl',
        'ps': 'ps',
        'pt-BR': 'pt-br',
        'pt-PT': 'pt',
        'qu': 'que',
        'rm': 'rm',
        'rn': 'run',
        'ro': 'ro',
        'ru': 'ru',
        'rup': 'rup',
        'rw': 'kin',
        'rue-UA': 'ry',
        'sa': 'sa',
        'sc': 'sc',
        'sd': 'sd',
        'se': 'se',
        'sg': 'sg',
        'sh': 'sh',
        'si': 'si',
        'sk': 'sk',
        'sl': 'sl',
        'sm': 'sm',
        'sn': 'sna',
        'so': 'som',
        'sq': 'sq',
        'sr': 'sr',
        'sr-Latn': 'sr-latn',
        'ss': 'ss',
        'st': 'sot',
        'su': 'su',
        'sv': 'sv',
        'sw': 'swa',
        'ta': 'ta',
        'te': 'te',
        'tet': 'tet',
        'tg': 'tg',
        'th': 'th',
        'ti': 'tir',
        'tk': 'tk',
        'tl': 'tl',
        'tlh': 'tlh',
        'tn': 'tsn',
        'to': 'to',
        'tr': 'tr',
        'ts': 'ts',
        'tt': 'tt',
        'ty': 'ty',
        'tw': 'tw',
        'uk': 'uk',
        'ug': 'ug',
        'ur': 'ur',
        'umb': 'umb',
        'uz': 'uz',
        've': 've',
        'vi': 'vi',
        'vo': 'vo',
        'wa': 'wa',
        'wo': 'wol',
        'xh': 'xho',
        'yi': 'yi',
        'yo': 'yor',
        'zh': 'zh-hk',
        'zh-CN': 'zh-cn',
        'zh-HK': 'zh-hk',
        'zh-Hans': 'zh-cn',
        'zh-Hant': 'zh-tw',
        'zh_Hant-HK': 'nan',
# we need to fix unilangs what to do when
# two dialects point to the same main language
        'zh-SG': 'zh-sg',
        'zh-TW': 'zh-tw',
        'za': 'za',
        'zu': 'zul'})

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
_add_bcp47()

class LanguageCode(object):
    def __init__(self, language_code, standard):
        try:
            standard_dict = TO_INTERNAL[standard.lower()]
        except KeyError:
            raise Exception("Standard '%s' is not registred" % standard)
        self._code = standard_dict[language_code]

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
        return INTERNAL_NAMES[self._code][0]

    def native_name(self):
        """Return the native name for this language as a unicode string."""
        return INTERNAL_NAMES[self._code][1]

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
    return dict((code, LanguageCode(code, standard).name())
                for code in TO_INTERNAL.get(standard))

def get_language_native_mapping(standard):
    """Return a dict of code -> native name for all languages in the standard."""
    return dict((code, LanguageCode(code, standard).native_name())
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

