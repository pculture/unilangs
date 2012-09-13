# -*- coding: utf-8 -*-

from __future__ import with_statement

from unilangs.bcp47.data import data

try:
    import json
    assert json # Shut up, Pyflakes.
except ImportError:
    import simplejson as json


# See also: http://github.com/pculture/bcp47-json
REGISTRY = json.loads(data)['subtags']

def _filter_subtags(typ):
    return [st for st in REGISTRY if st['type'] == typ]

def _map_by_subtag(typ):
    return dict((st['subtag'].lower(), st) for st in _filter_subtags(typ))

def _map_by_tag(typ):
    return dict((st['tag'].lower(), st) for st in _filter_subtags(typ))

LANGUAGE_SUBTAGS = _map_by_subtag('language')
SCRIPT_SUBTAGS = _map_by_subtag('script')
REGION_SUBTAGS = _map_by_subtag('region')
VARIANT_SUBTAGS = _map_by_subtag('variant')
EXTLANG_SUBTAGS = _map_by_subtag('extlang')
GRANDFATHERED_SUBTAGS = _map_by_tag('grandfathered')
REDUNDANT_SUBTAGS = _map_by_tag('redundant')
