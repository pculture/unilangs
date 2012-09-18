# -*- coding: utf-8 -*-

from unilangs.bcp47.parser import parse_code


class BestFitDict(dict):
    def add(self, value, language, region=None, script=None):
        self[(language, region, script)] = value

    def lookup(self, language, region, script):
        """Look up a value, returning the best-fitting entry."""

        result = (self.get((language, region, script)) or
                  self.get((language, None, script)) or
                  self.get((language, region, None)) or
                  self.get((language, None, None)) or
                  None)

        if result:
            return result
        else:
            raise KeyError(
                "Could not find Unilangs language for BCP47 "+
                "language '%s', region '%s', script '%s'"
                % (language, region, script))

    def add_all(self, langs):
        for lang in langs:
            self.add(*lang)


def _make_bcp47_to_unilangs():
    btu = BestFitDict()

    btu.add_all((
        # Unilangs code
        # |     BCP47 language[, region]
        # |     |
        # v     v
        ('aa', 'aa'),
        ('ab', 'ab'),
        ('ae', 'ae'),
        ('af', 'af'),
        ('aka', 'ak'),
        ('amh', 'am'),
        ('an', 'an'),
        ('ar', 'ar'),
        ('arq', 'aao'),
        ('as', 'as'),
        ('ase', 'ase'),
        ('ast', 'ast'),
        ('av', 'av'),
        ('ay', 'ay'),
        ('az', 'az'),
        ('ba', 'ba'),
        ('bam', 'bm'),
        ('be', 'be'),
        ('ber', 'ber'),
        ('bg', 'bg'),
        ('bh', 'bh'),
        ('bi', 'bi'),
        ('bn', 'bn'),
        ('bnt', 'bnt'),
        ('bo', 'bo'),
        ('br', 'br'),
        ('bs', 'bs'),
        ('bug', 'bug'),
        ('ca', 'ca'),
        ('ce', 'ce'),
        ('ceb', 'ceb'),
        ('ch', 'ch'),
        ('cho', 'cho'),
        ('co', 'co'),
        ('cr', 'cr'),
        ('cs', 'cs'),
        ('cu', 'cu'),
        ('cv', 'cv'),
        ('cy', 'cy'),
        ('da', 'da'),
        ('de', 'de'),
        ('dv', 'dv'),
        ('dz', 'dz'),
        ('ee', 'ee'),
        ('efi', 'efi'),
        ('el', 'el'),
        ('en', 'en'),
        ('en-gb', 'en', 'gb'),
        ('eo', 'eo'),
        ('es', 'es'),
        ('es-ar', 'es', 'ar'),
        ('es-mx', 'es', 'mx'),
        ('es-ni', 'es', 'ni'),
        ('et', 'et'),
        ('eu', 'eu'),
        ('fa', 'fa'),
        ('ff', 'ff'),
        ('fi', 'fi'),
        ('fil', 'fil'),
        ('fj', 'fj'),
        ('fo', 'fo'),
        ('fr', 'fr'),
        ('fr-ca', 'fr', 'ca'),
        ('ful', 'ff'),
        ('fy-nl', 'fy'),
        ('ga', 'ga'),
        ('gd', 'gd'),
        ('gl', 'gl'),
        ('gn', 'gn'),
        ('gu', 'gu'),
        ('gv', 'gv'),
        ('hai', 'hai'),
        ('hau', 'ha'),
        ('haz', 'haz'),
        ('he', 'he'),
        ('hi', 'hi'),
        ('ho', 'ho'),
        ('hr', 'hr'),
        ('ht', 'ht'),
        ('hu', 'hu'),
        ('hup', 'hup'),
        ('hy', 'hy'),
        ('hz', 'hz'),
        ('ia', 'ia'),
        ('ibo', 'ig'),
        ('id', 'id'),
        ('ie', 'ie'),
        ('ii', 'ii'),
        ('ik', 'ik'),
        ('ilo', 'ilo'),
        ('inh', 'inh'),
        ('io', 'io'),
        ('iro', 'iro'),
        ('is', 'is'),
        ('it', 'it'),
        ('iu', 'iu'),
        ('ja', 'ja'),
        ('jv', 'jv'),
        ('ka', 'ka'),
        ('kar', 'kar'),
        ('kau', 'kr'),
        ('kik', 'ki'),
        ('kin', 'rw'),
        ('kj', 'kj'),
        ('kk', 'kk'),
        ('kl', 'kl'),
        ('km', 'km'),
        ('kn', 'kn'),
        ('ko', 'ko'),
        ('kon', 'kg'),
        ('ks', 'ks'),
        ('ku', 'ku'),
        ('kv', 'kv'),
        ('kw', 'kw'),
        ('ky', 'ky'),
        ('la', 'la'),
        ('lb', 'lb'),
        ('lg', 'lg'),
        ('li', 'li'),
        ('lin', 'ln'),
        ('lkt', 'lkt'),
        ('lo', 'lo'),
        ('lt', 'lt'),
        ('lu', 'lu'),
        ('lua', 'lua'),
        ('luo', 'luo'),
        ('luy', 'luy'),
        ('lv', 'lv'),
        ('mad', 'mad'),
        ('mh', 'mh'),
        ('mi', 'mi'),
        ('mk', 'mk'),
        ('ml', 'ml'),
        ('mlg', 'mg'),
        ('mn', 'mn'),
        ('mnk', 'mnk'),
        ('mo', 'mo'),
        ('moh', 'moh'),
        ('mni', 'mni'),
        ('mos', 'mos'),
        ('mr', 'mr'),
        ('ms', 'ms'),
        ('mt', 'mt'),
        ('my', 'my'),
        ('nan', 'nan'),
        ('na', 'na'),
        ('nb', 'nb'),
        ('nd', 'nd'),
        ('ne', 'ne'),
        ('ng', 'ng'),
        ('nl', 'nl'),
        ('nn', 'nn'),
        ('no', 'no'),
        ('nr', 'nr'),
        ('nso', 'nso'),
        ('nv', 'nv'),
        ('nya', 'ny'),
        ('oc', 'oc'),
        ('oji', 'oj'),
        ('or', 'or'),
        ('orm', 'om'),
        ('os', 'os'),
        ('pam', 'pam'),
        ('pap', 'pap'),
        ('pan', 'pa'),
        ('pi', 'pi'),
        ('pl', 'pl'),
        ('pnb', 'pnb'),
        ('prs', 'prs'),
        ('ps', 'ps'),
        ('pt', 'pt'),
        ('pt-br', 'pt', 'br'),
        ('que', 'qu'),
        ('rm', 'rm'),
        ('ro', 'ro'),
        ('ru', 'ru'),
        ('run', 'rn'),
        ('rup', 'rup'),
        ('ry', 'rue'),
        ('sa', 'sa'),
        ('sc', 'sc'),
        ('sd', 'sd'),
        ('se', 'se'),
        ('sg', 'sg'),
        ('sh', 'sh'),
        ('si', 'si'),
        ('sk', 'sk'),
        ('skx', 'skx'),
        ('sl', 'sl'),
        ('sm', 'sm'),
        ('sna', 'sn'),
        ('som', 'so'),
        ('sot', 'st'),
        ('sq', 'sq'),
        ('sr', 'sr'),
        ('sr-latn', 'sr', None, 'latn'),
        ('ss', 'ss'),
        ('su', 'su'),
        ('sv', 'sv'),
        ('swa', 'sw'),
        ('ta', 'ta'),
        ('tet', 'tet'),
        ('te', 'te'),
        ('tg', 'tg'),
        ('th', 'th'),
        ('tir', 'ti'),
        ('tk', 'tk'),
        ('tl', 'tl'),
        ('tlh', 'tlh'),
        ('to', 'to'),
        ('tr', 'tr'),
        ('ts', 'ts'),
        ('tsn', 'tn'),
        ('tt', 'tt'),
        ('tw', 'tw'),
        ('ty', 'ty'),
        ('ug', 'ug'),
        ('uk', 'uk'),
        ('umb', 'umb'),
        ('ug', 'ug'),
        ('ur', 'ur'),
        ('uz', 'uz'),
        ('ve', 've'),
        ('vi', 'vi'),
        ('vo', 'vo'),
        ('wa', 'wa'),
        ('wol', 'wo'),
        ('xho', 'xh'),
        ('yi', 'yi'),
        ('yor', 'yo'),
        ('za', 'za'),
        ('zh', 'yue'),
        ('zh-cn', 'zh', None, 'hans'),
        ('zh-tw', 'zh', None, 'hant'),
        ('zh-sg', 'zh', 'sg', 'hans'),
        ('zh-hk', 'zh', 'hk', 'hant'),
        ('zul', 'zu'),
    ))

    return btu

BCP47_TO_UNILANGS = _make_bcp47_to_unilangs()


class BCP47ToUnilangConverter(object):
    """A conversion utility masquerading as a dict to fit into unilangs."""

    def __getitem__(self, k):
        parts = parse_code(k)

        def _get_part(part):
            return parts[part]['subtag'].lower() if parts[part] else None

        language = _get_part('language')
        region = _get_part('region')
        script = _get_part('script')

        return BCP47_TO_UNILANGS.lookup(language, region, script)

    def get(self, k, notfound=None):
        try:
            return self[k]
        except KeyError:
            return notfound

