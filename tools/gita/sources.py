#!/usr/bin/env python3
"""Compare three open copies of the Gita's Sanskrit, verse by verse, and print where they differ.

    python3 -I tools/gita/sources.py <folder with the downloaded copies> <chapter> [<chapter> ...]

The folder holds: verse.json (github.com/gita/gita, data/verse.json), B/<ch>-<verse>.json
(github.com/vedicscriptures/bhagavad-gita, slok/) and C/<ch>.json (github.com/bhavykhatri/DharmicData,
SrimadBhagvadGita/). A and C descend from the same typing; B is independent of them.

All three number chapter 13 with 35 verses. The site follows the 700-verse numbering, in which the
first of those (Arjuna's question) is left out, so site verse 13.n is their 13.(n+1).
"""
import json, re, sys, unicodedata

SPEAKER = re.compile(r'^\s*(श्री\s*भगवानुवाच|श्रीभगवानुवाच|अर्जुन\s*उवाच|सञ्जय\s*उवाच|संजय\s*उवाच|धृतराष्ट्र\s*उवाच)\s*[।|]*\s*', re.M)


def load(folder):
    a = {(x['chapter_number'], x['verse_number']): x['text'] for x in json.load(open(folder + '/verse.json', encoding='utf-8'))}
    return a


def copy_b(folder, c, v):
    return json.load(open('%s/B/%d-%d.json' % (folder, c, v), encoding='utf-8'))['slok']


def copy_c(folder, c):
    d = json.load(open('%s/C/%d.json' % (folder, c), encoding='utf-8'))['BhagavadGitaChapter']
    return {x['verse']: x['text'] for x in d}


def repair(t):
    """Known faults that are not differences of reading.

    Copies A and C: a short-i sign typed before or after the virama (श्िच for श्चि, त्ति्र for त्त्रि); ṝ typed as ṛ plus a nukta (पितृ़न्);
    शृणु spelled श्रृणु. Copy B: hyphens marking where a line was broken, and editors' notes in brackets.
    """
    t = re.sub(r'्ि([क-ह])', r'्\1ि', t)
    t = re.sub(r'ि्([क-ह])', r'्\1ि', t)
    t = t.replace('ृ़', 'ॄ').replace('़', '').replace('श्रृ', 'शृ')
    t = re.sub(r'\([^)]*\)', '', t)
    t = re.sub(r'(?<=[\u0901-\u0963])-\s*(?=[\u0901-\u0963])', '', t)
    return t


def speaker(t):
    m = SPEAKER.search(t)
    return re.sub(r'\s+', '', m.group(1)) if m else ''


def lines(t):
    """The verse as clean lines: no speaker line, no verse number, one space between words."""
    t = unicodedata.normalize('NFC', t).replace('‌', '').replace('‍', '')
    t = SPEAKER.sub('', t)
    t = re.sub(r'[।|॥]+\s*[0-9०-९]+\s*[-.]\s*[0-9०-९]+\s*[।|॥]+', '', t)
    out = [re.sub(r'\s+', ' ', x).strip() for x in re.split(r'[।|॥\n]+', t)]
    return [x for x in out if x]


def key(t, loose=True):
    """For comparing: letters only; optionally treat a class nasal + virama like an anusvara."""
    k = re.sub(r'[\s।॥|-]', '', ' '.join(lines(t)))
    if loose:
        k = re.sub('[ङञणनम]्(?=[क-ह])', 'ं', k)
        k = k.replace('ऽ', '')
    return k


def diff(a, b):
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    return a[max(0, i - 10):i + 16], b[max(0, i - 10):i + 16]


if __name__ == '__main__':
    folder = sys.argv[1]
    A = load(folder)
    for c in map(int, [x for x in sys.argv[2:] if x.isdigit()]):
        C = copy_c(folder, c)
        n = max(v for (cc, v) in A if cc == c)
        same = 0
        for v in range(1, n + 1):
            ka, kb, kc = key(repair(A[(c, v)])), key(repair(copy_b(folder, c, v))), key(repair(C[v]))
            if ka == kb == kc:
                same += 1
                continue
            odd = 'B' if ka == kc else ('A' if kb == kc else ('C' if ka == kb else 'all three'))
            x, y = diff(ka, kb) if ka != kb else diff(ka, kc)
            print('%d.%d  differs: %s   %s | %s' % (c, v, odd, x, y))
            if '--full' in sys.argv:
                print('   A: ' + ' / '.join(lines(repair(A[(c, v)]))))
                print('   B: ' + ' / '.join(lines(repair(copy_b(folder, c, v)))))
        print('chapter %d: %d of %d verses agree in all three copies' % (c, same, n))
