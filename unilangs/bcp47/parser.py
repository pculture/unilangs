# -*- coding: utf-8 -*-

from unilangs.bcp47.registry import (
    LANGUAGE_SUBTAGS, EXTLANG_SUBTAGS, SCRIPT_SUBTAGS, REGION_SUBTAGS,
    VARIANT_SUBTAGS, GRANDFATHERED_SUBTAGS
)

from pprint import pprint


class InvalidLanguageException(Exception):
    pass

class MalformedLanguageCodeException(Exception):
    pass


def _split_at(pred, seq):
    """Split the given sequence into a number of sequences as a generator.

    The seq is split wherever pred(element) returns true.  The elements
    themselves ARE included in the resulting sequences.

    Example:

        _split_at(lambda el: len(el) == 1,
                  ['foo', 'bar', 'a', 'baz', 'b', 'c', 'spam'])

        [['foo', 'bar'],
         ['a', 'baz'],
         ['b'],
         ['c', 'spam']]

    """
    # We start with None as a sentinal to handle the case of splitter value at
    # index 0.
    next = None

    for el in seq:
        if pred(el):
            if next != None:
                yield next
            next = [el]
        else:
            if next == None:
                next = []
            next.append(el)

    if next:
        yield next


def _next_chunk(code):
    """Split a chunk off of the given code, return (chunk, rest)."""
    return code.split('-', 1) if '-' in code else (code, '')


def _parse_extensions(code):
    """Parse all the extension tags from the given code.

    The code must *only* consist of extensions (it's assumed you've already
    parsed the beginning).

    A list of tuples will be returned, looking something like this:

        _parse_extensions('x-foo-bar-a-baz')

        [('x', ['foo', 'bar']),
         ('a', ['baz'])]

    """
    chunks = list(_split_at(lambda el: len(el) == 1,
                            code.split('-')))

    if chunks and len(chunks[0]) != 1:
        raise MalformedLanguageCodeException(
            "Garbage '%s' at the end of the language code!" % code)

    results = []
    for chunk in chunks:
        tag, data = chunk[0], chunk[1:]

        if not data:
            raise MalformedLanguageCodeException(
                "Encountered a singleton extension tag '%s' without data!"
                % chunk[0])

        results.append((tag, data))

    return results


def _parse_code(code):
    """Parse a BCP47 language code into its constituent parts.

    A BCP47 language code looks like this:

        language-extlang-script-region-variant-extension-privateuse

    Every one of those except for language is optional.

    A dictionary of parts will be returned, with keys of 'language', 'extlang',
    etc and values of the entries in the BCP47 registry.

    Note that this function only validates the structure of the language code.
    It doesn't look at the semantic values of each piece and check for things
    like nonsensical variants for languages.  Use _validate for that.

    """
    code = code.lower()
    result = {'language': None, 'extlang': None, 'script': None, 'region': None,
              'variant': None, 'grandfathered': None, 'extensions': []}

    # Grandfathered tags take precedence over everything.
    if code in GRANDFATHERED_SUBTAGS:
        result['grandfathered'] = GRANDFATHERED_SUBTAGS[code]
        return result

    # "Private use" language codes.
    if code.startswith('x-'):
        result['extensions'] = _parse_extensions(code)
        return result

    # Language is required and always comes first, no matter what.
    language, code = _next_chunk(code)

    if language in LANGUAGE_SUBTAGS:
        result['language'] = LANGUAGE_SUBTAGS[language]
        next, code = _next_chunk(code)
    else:
        raise InvalidLanguageException(
            "Invalid primary language '%s'!" % language)

    # Parse the rest of the subtags, in order.
    def _parse_subtag(next, code, reg):
        if next in reg:
            st = reg[next]
            next, code = _next_chunk(code)
            return st, next, code
        else:
            return None, next, code

    result['extlang'], next, code = _parse_subtag(next, code, EXTLANG_SUBTAGS)
    result['script'],  next, code = _parse_subtag(next, code, SCRIPT_SUBTAGS)
    result['region'],  next, code = _parse_subtag(next, code, REGION_SUBTAGS)
    result['variant'], next, code = _parse_subtag(next, code, VARIANT_SUBTAGS)

    if next and not code:
        raise MalformedLanguageCodeException(
            "Garbage '%s' at the end of the language code!" % next)

    # Any remainder is a set of one or more extensions.
    if next:
        # Restore the full remainder of the code.
        code = next + '-' + code
        result['extensions'] = _parse_extensions(code)

    return result

def _validate(l):
    """Validated that the parsed language dict makes sense."""

    # Grandfathered languages are always valid.
    if l['grandfathered']:
        return l

    return l

def parse_code(bcp47_language_code):
    return _validate(_parse_code(bcp47_language_code))

def _t(lc):
    print '=' * 60
    pprint(parse_code(lc))
    print

# _t('en')
# _t('zh-yue')
# _t('zh-yue-Hans')
# _t('zh-Hans')
# _t('sl-nedis')
# _t('en-Latn-US-x-hurr-u-durr-a-spam-eggs')
_t('art-lojban')
_t('jbo')
_t('i-klingon')
