#!/usr/bin/env python3
"""Write tools/gita/ch01.json to ch06.json from the published English chapter pages.

    python3 -I tools/gita/make_early.py

Chapters 1 to 6 were made before make_data.py existed, so their checked Sanskrit lives in the English pages
(gita-1.html to gita-6.html). This reads it back, with the speaker and the English translation, so that build.py
can make pages for a language that does not have these chapters yet. It never changes the English pages, and
build.py does not rewrite them either (it skips the English part for chapters 1 to 6).

Each verse is checked: the Sanskrit that build.py would print must be exactly what the English page shows, so the
new pages carry the same text. The pronunciation is made from the Sanskrit; where the English page shows something
else, that is printed so the English page can be looked at.

"featured" lists the verses that already have a hand-made page in Kannada and Malayalam; those keep their pages.
"""
import html, json, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
os.chdir(ROOT)
import build as B

OPENS = {'श्री भगवानुवाच': 'Krishna', 'अर्जुन उवाच': 'Arjuna', 'सञ्जय उवाच': 'Sanjaya', 'संजय उवाच': 'Sanjaya',
         'धृतराष्ट्र उवाच': 'Dhritarashtra'}
ROMAN = {1: 'Arjuna Vishada Yoga', 2: 'Sankhya Yoga', 3: 'Karma Yoga', 4: 'Jnana Karma Sannyasa Yoga',
         5: 'Karma Sannyasa Yoga', 6: 'Dhyana Yoga'}


def text(x):
    return html.unescape(re.sub(r'<[^>]+>', '', x)).strip()


def chapter(c):
    s = open('gita-%d.html' % c, encoding='utf-8').read()
    name = text(re.search(r'<h1>(.*?)</h1>', s, re.S).group(1)).split(': ', 1)[1]
    skt_name = re.search(r'<i>([^<]*)</i>', s).group(1)
    verses = []
    for n in range(1, B.COUNTS[c] + 1):
        a = re.search(r'<article class="verse" id="v-gita-%d-%d">(.*?)</article>' % (c, n), s, re.S)
        if not a:
            raise SystemExit('gita-%d.html: verse %d not found' % (c, n))
        a = a.group(1)
        speaker = text(re.search(r'<h3>(.*?)</h3>', a, re.S).group(1)).split(' · ', 1)[1]
        skt = re.search(r'<p class="skt">(.*?)</p>', a, re.S).group(1)
        lines = [x.strip() for x in skt.split('<br/>')]
        opens = ''
        if lines[0] in OPENS:
            opens = lines.pop(0)
            if OPENS[opens] != speaker:
                raise SystemExit('%d.%d: %s opens but the heading says %s' % (c, n, opens, speaker))
        lines = [re.sub(r'\s*[।॥]\s*$', '', x) for x in lines]
        tr = text(re.search(r'<span class="label">.*?</span></span>\s*<p[^>]*>(.*?)</p>', a, re.S).group(1))
        v = {'v': n, 'speaker': speaker, 'opens': opens, 'skt': lines, 'tr': tr}
        if B.skt_html(v) != skt.strip():
            raise SystemExit('%d.%d: Sanskrit would print differently:\n  %s\n  %s' % (c, n, B.skt_html(v), skt.strip()))
        iast = html.unescape(re.search(r'<p class="iast">(.*?)</p>', a, re.S).group(1)).strip()
        if '\n'.join(B.iast_lines(v)) != iast:
            print('  %d.%d: the English page\'s pronunciation differs from the Sanskrit; the new pages follow the Sanskrit:\n    page: %r\n    new:  %r' % (c, n, iast, '\n'.join(B.iast_lines(v))))
        verses.append(v)
    featured = sorted(n for n in range(1, B.COUNTS[c] + 1)
                      if all(os.path.exists('%s/gita-%d-%d.html' % (l, c, n)) for l in ('kn', 'ml')))
    meta = {'n': c, 'featured': featured, 'name': name, 'skt_name': skt_name, 'roman_name': ROMAN[c]}
    json.dump({'meta': meta, 'verses': verses}, open(os.path.join(HERE, 'ch%02d.json' % c), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('ch%02d.json: %d verses, featured %s' % (c, len(verses), featured))


if __name__ == '__main__':
    for c in range(1, 7):
        chapter(c)
