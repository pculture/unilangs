# -*- coding: utf-8 -*-

from unilangs.bcp47.registry import (
    LANGUAGE_SUBTAGS, EXTLANG_SUBTAGS, SCRIPT_SUBTAGS, REGION_SUBTAGS,
    VARIANT_SUBTAGS, GRANDFATHERED_SUBTAGS
)

from pprint import pprint


# Exceptions
class MalformedLanguageCodeException(Exception):
    pass


# Convenience Functions
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


# Parsing codes
def _next_chunk(code):
    """Split a chunk off of the given code, return (chunk, rest)."""
    return code.split('-', 1) if '-' in code else (code, '')


def _parse_extensions(code):
    """Parse all the extension tags from the given code.

    The code must *only* consist of extensions (it's assumed you've already
    parsed the beginning).

    A dict of lists will be returned, looking something like this:

        _parse_extensions('x-foo-bar-a-baz')

        {'x': ['foo', 'bar'],
         'a': ['baz']}

    """
    def _die():
        raise MalformedLanguageCodeException(
            "Garbage '%s' at the end of the language code!" % code)

    # Split on dashes, and make sure we don't end up with any empty elements.
    # Those would come from things like '-foo', 'foo-', or 'foo--bar', which
    # are all invalid.
    bits = code.split('-')
    if any(not bit for bit in bits):
        _die()

    # Split the words into runs of [singleton, data, data, ...].
    chunks = list(_split_at(lambda el: len(el) == 1, bits))

    # We may not have anything at all.  That's fine.
    if not chunks:
        return {}

    # Because of the way split_at works, it's possible we may not have
    # a singleton starting the first chunk, which is invalid (e.g. 'foo-x-bar').
    if len(chunks[0][0]) != 1:
        _die()

    results = {}
    for chunk in chunks:
        # We know we have a list of runs, each starting with a singleton tag.
        tag, data = chunk[0], chunk[1:]

        # Singletons without data are disallowed by the spec (e.g.'x-a-foo'
        # or 'x-foo-b').
        if not data:
            raise MalformedLanguageCodeException(
                "Encountered a singleton extension tag '%s' without data!"
                % chunk[0])

        if tag in results:
            raise MalformedLanguageCodeException(
                "Encountered a duplicate singleton extension tag '%s'!" % tag)

        results[tag] = data

    return results


def _parse_subtag(next, code, reg):
    if next in reg:
        st = reg[next]
        next, code = _next_chunk(code)
        return st, next, code
    else:
        return None, next, code

def _parse_variants(next, code):
    variants = []
    variant, next, code = _parse_subtag(next, code, VARIANT_SUBTAGS)

    while variant:
        variants.append(variant)
        variant, next, code = _parse_subtag(next, code, VARIANT_SUBTAGS)

    return variants, next, code

def _parse_code(code):
    """Parse a BCP47 language code into its constituent parts.

    A BCP47 language code looks like this:

        language-extlang-script-region-variant-extension-privateuse

    Every one of those except for language is optional.  Multiple variant tags
    can appear, as well as any number of extensions.

    A dictionary of parts will be returned, with keys of 'language', 'extlang',
    etc and values of the entries in the BCP47 registry.

    The variant portion will be returned with a key of 'variants' and value of
    a list of registry entries (possibly empty).

    The extension portion will be returned as a list of tuples of (code,
    [data...]).  For example, "en-x-foo-bar" would have an 'extensions' value
    of [('x', ['foo', 'bar'])].

    Note that this function only validates the structure of the language code.
    It doesn't look at the semantic values of each piece and check for things
    like nonsensical variants for languages.  Use _validate for that.

    """
    code = code.lower()
    result = {'language': None, 'extlang': None, 'script': None, 'region': None,
              'variants': [], 'grandfathered': None, 'extensions': {}}

    # Grandfathered tags take precedence over everything.
    if code in GRANDFATHERED_SUBTAGS:
        result['grandfathered'] = GRANDFATHERED_SUBTAGS[code]
        return result

    # "Private use" language codes.
    if code.startswith('x-'):
        result['extensions'] = _parse_extensions(code)
        return result

    # Ensure that there are no empty chunks, like 'en--us' or 'en-'.
    if any((not c) for c in code.split('-')):
        raise MalformedLanguageCodeException(
            "Invalid language code (malformed hyphen)!")

    # Language is required and always comes first, no matter what.
    language, code = _next_chunk(code)

    if language in LANGUAGE_SUBTAGS:
        result['language'] = LANGUAGE_SUBTAGS[language]
        next, code = _next_chunk(code)
    else:
        raise MalformedLanguageCodeException(
            "Invalid primary language '%s'!" % language)

    # Parse the rest of the subtags, in order.
    result['extlang'], next, code = _parse_subtag(next, code, EXTLANG_SUBTAGS)
    result['script'], next, code = _parse_subtag(next, code, SCRIPT_SUBTAGS)
    result['region'], next, code = _parse_subtag(next, code, REGION_SUBTAGS)
    result['variants'], next, code = _parse_variants(next, code)

    if next and not code:
        raise MalformedLanguageCodeException(
            "Garbage '%s' at the end of the language code!" % next)

    # Any remainder is a set of one or more extensions.
    if next:
        # Restore the full remainder of the code.
        code = next + '-' + code
        result['extensions'] = _parse_extensions(code)

    return result


# Validating parsed codes
def _validate(l):
    """Validated that the parsed language dict makes sense.

    Returns the language code if it's okay, or throws an exception if it's
    broken.

    """

    # Grandfathered languages are always valid.
    if l['grandfathered']:
        return l

    return l


# Public API
def parse_code(bcp47_language_code):
    return _validate(_parse_code(bcp47_language_code))

