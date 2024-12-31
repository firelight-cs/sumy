import re

_PERFECTIVE_GROUND = r'(ив|ыв|ивши|ывши|ившись|ывшись)$'
_REFLEXIVE = r'(ся|сь)$'
_ADJECTIVE = r'(ый|ий|ой|ем|им|ым|ом|его|ого|ему|ому|ее|ое|ие|ые|их|ых|ую|юю|ая|яя|ою|ею)$'
_PARTICIPLE = r'(ивш|ывш|ующ)$'
_VERB = r'(ила|ыла|ена|ена|ить|ыть|ете|ите|или|ыли|йте|йте|ла|на|ете|ите|й)$'
_NOUN = r'(а|ев|ов|е|иями|ями|ами|еи|и|ей|ий|й|иям|ям|ием|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я)$'
_RVRE = r'[аеиоуюяёэы]'
_DERIVATIONAL = r'[^аеиоуюяёэы][аеиоуюяёэы]+[^аеиоуюяёэы]+[аеиоуюяёэы].*(?<=о)сть?$'

def stem_word(word):
    word = _preprocess(word)
    if not re.search(_RVRE, word):
        return word

    p = re.search(_RVRE, word)
    start = word[:p.span()[1]]
    suffix = word[p.span()[1]:]

    # Step 1
    updated, suffix = _update_suffix(suffix, _PERFECTIVE_GROUND, '')
    if not updated:
        _, suffix = _update_suffix(suffix, _REFLEXIVE, '')
        updated, suffix = _update_suffix(suffix, _ADJECTIVE, '')
        if updated:
            updated, suffix = _update_suffix(suffix, _PARTICIPLE, '')
        else:
            updated, suffix = _update_suffix(suffix, _VERB, '')
            if not updated:
                _, suffix = _update_suffix(suffix, _NOUN, '')

    # Step 2
    updated, suffix = _update_suffix(suffix, 'и$', '')

    # Step 3
    if re.search(_DERIVATIONAL, suffix):
        updated, suffix = _update_suffix(suffix, 'ость$', '')

    # Step 4
    updated, suffix = _update_suffix(suffix, 'ь$', '')
    if updated:
        _, suffix = _update_suffix(suffix, 'ейше?$', '')
        _, suffix = _update_suffix(suffix, 'нн$', 'н')

    return start + suffix

def _preprocess(word):
    return word.lower().replace('ё', 'е').strip()

def _update_suffix(suffix, pattern, replacement):
    result = re.sub(pattern, replacement, suffix)
    return suffix != result, result
