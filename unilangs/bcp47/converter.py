# -*- coding: utf-8 -*-

from unilangs.bcp47.parser import parse_code



class BCP47ToUnilangConverter(object):
    """A conversion utility masquerading as a dict to fit into unilangs."""


    def __getitem__(self, k):
        return parse_code(k)

    def get(self, k, notfound=None):
        return self[k]


c = BCP47ToUnilangConverter()
print c.get('en')

