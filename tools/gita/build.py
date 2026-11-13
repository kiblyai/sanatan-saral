#!/usr/bin/env python3
"""Build the pages for one Gita chapter from tools/gita/chNN.json. Run from the site root.

    python3 tools/gita/build.py 7
    python3 tools/split_languages.py        # afterwards: sets each new page's canonical link and head script

Writes gita-N.html (every verse of the chapter) and gita-N-V.html (one page per verse), in English, and adds
them to the chapter before it, the Gita hub, the search index and the sitemap. Safe to run again.

Verses that already had a page of their own before the chapter was built (listed as "featured" in the
chapter's data) keep that page. Only its previous/next links and its "in context" link are changed.

The page furniture (head, menu, footer) is copied from chapter 6: gita-6-10.html for a verse page and
gita-6.html for a chapter page, so a change to the site's menu there carries into rebuilt pages.
"""
import datetime, html, json, os, re, sys, urllib.parse
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from translit import iast

SITE = 'https://sanatan.space/'
EN = 'en xg xt xm xa xb xk xl'
LANGS = ['hi', 'gu', 'te', 'mr', 'ta', 'bn', 'kn', 'ml']
HERE = os.path.dirname(os.path.abspath(__file__))
COUNTS = {1: 47, 2: 72, 3: 43, 4: 42, 5: 29, 6: 47, 7: 30, 8: 28, 9: 34, 10: 42, 11: 55, 12: 20,
          13: 34, 14: 27, 15: 20, 16: 24, 17: 28, 18: 78}


def e(t):
    return html.escape(t, quote=False)


def span(t):
    return '<span class="%s">%s</span>' % (EN, e(t))


def sub1(pattern, repl, s, what, flags=re.S):
    new, n = re.subn(pattern, lambda m: repl, s, count=1, flags=flags)
    if n != 1:
        raise SystemExit('template changed: could not find ' + what)
    return new


def skt_html(v):
    L = v['skt']
    if len(L) == 2:
        body = '%s ।<br/>%s ॥' % (L[0], L[1])
    elif len(L) == 4:
        body = '%s<br/>%s ।<br/>%s<br/>%s ॥' % tuple(L)
    else:
        body = '<br/>'.join(L[:-1]) + '<br/>' + L[-1] + ' ॥'
    return (v['opens'] + '<br/>' if v['opens'] else '') + body


def iast_lines(v):
    L = [iast(x) for x in v['skt']]
    if len(L) == 2:
        return [L[0] + ' |', L[1] + ' ||']
    if len(L) == 4:
        return [L[0], L[1] + ' |', L[2], L[3] + ' ||']
    return L[:-1] + [L[-1] + ' ||']


def article(c, v, own_page, featured):
    """One verse. own_page: on its own page (no link in the heading). featured: it has a longer page elsewhere."""
    n = v['v']
    ref = 'Gita %d.%d' % (c, n)
    head = '%d.%d · %s' % (c, n, v['speaker'])
    src = ('<span class="src">%s</span>' % span(ref)) if own_page else ('<a class="src" href="gita-%d-%d.html">%s</a>' % (c, n, span(ref)))
    words = ''.join('<dt>%s</dt><dd>%s</dd>' % (e(sk), span(en)) for sk, en in v['words'])
    more = ('<p class="%s"><a class="more" href="gita.html#v-gita-%d-%d">Read the full explanation →</a></p>' % (EN, c, n)) if featured else ''
    q = urllib.parse.quote_plus('Gita %d.%d %s chanting' % (c, n, head))
    return ('<article class="verse" id="v-gita-%d-%d">\n' % (c, n)
            + '<div class="v-head"><h3>%s</h3>%s</div>\n' % (span(head), src)
            + '<p class="skt">%s</p>\n' % skt_html(v)
            + '<p class="iast">%s</p>\n' % e('\n'.join(iast_lines(v)))
            + '<details class="words"><summary>%s</summary><dl>%s</dl></details>\n' % (span('Word by word'), words)
            + '<div><span class="label">%s</span><p class="%s">%s</p>%s</div>\n' % (span('Translation'), EN, e(v['tr']), more)
            + '<p class="listen"><a href="https://www.youtube.com/results?search_query=%s" rel="noopener" target="_blank">%s</a>' % (q, span('▶ Listen to recitations'))
            + '<a class="share-wa" href="https://wa.me/" rel="noopener" target="_blank">%s</a>' % span('Share on WhatsApp')
            + '<button class="share-copy" type="button">%s</button><button class="v-save" type="button">%s</button>' % (span('Copy'), span('☆ Save'))
            + '<button class="v-img" type="button">%s</button></p></article>' % span('🖼 Picture'))


def neighbours(c, n, folder=''):
    """The verse before and after, across chapter ends, but only where a page exists (in folder, e.g. 'hi/')."""
    prev = (c, n - 1) if n > 1 else ((c - 1, COUNTS[c - 1]) if c > 1 else None)
    nxt = (c, n + 1) if n < COUNTS[c] else ((c + 1, 1) if c < 18 else None)
    ok = lambda p: p and os.path.exists(folder + 'gita-%d-%d.html' % p)
    return (prev if ok(prev) else None), (nxt if ok(nxt) else None)


def vnav(c, n):
    prev, nxt = neighbours(c, n)
    a = ''
    if prev:
        a += '<a class="vnav-prev" href="gita-%d-%d.html">%s</a>' % (prev[0], prev[1], span('← Gita %d.%d' % prev))
    if nxt:
        a += '<a class="vnav-next" href="gita-%d-%d.html">%s</a>' % (nxt[0], nxt[1], span('Gita %d.%d →' % nxt))
    return '<nav class="vnav" aria-label="More verses">%s</nav>' % a


def vback(c, n):
    return '<p class="vback"><a class="more" href="gita-%d.html#v-gita-%d-%d">%s</a></p>' % (c, c, n, span('See it in context →'))


def hreflang_en(s, url, hi_url=None):
    """English (and, where there is one, Hindi) alternates; any others the template had are removed."""
    s = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n', '', s)
    block = '<link rel="alternate" hreflang="en" href="%s">\n' % url
    if hi_url:
        block += '<link rel="alternate" hreflang="hi" href="%s">\n' % hi_url
    block += '<link rel="alternate" hreflang="x-default" href="%s">\n' % url
    return s.replace('</head>', block + '</head>', 1)


def shorten(t, limit=150):
    if len(t) <= limit:
        return t
    return t[:limit].rsplit(' ', 1)[0].rstrip(',;:') + '…'


def verse_page(tpl, c, meta, v, hindi=False):
    n = v['v']
    url = '%sgita-%d-%d.html' % (SITE, c, n)
    il = iast_lines(v)
    first = il[0].rstrip(' |')
    words4 = ' '.join(first.split()[:4])
    title = 'Bhagavad Gita %d.%d: %s – Meaning | Sanatan Dharma Saral' % (c, n, words4)
    headline = 'Bhagavad Gita %d.%d: %s' % (c, n, first)
    desc = shorten(v['tr']) + ' Sanskrit, pronunciation, word meanings and a simple explanation.'
    chap = 'Gita chapter %d: %s' % (c, meta['name'])
    image = SITE + 'og/gita-%d.png?v=2' % c
    s = tpl
    s = sub1(r'<title>.*?</title>', '<title>%s</title>' % e(title), s, 'title')
    s = sub1(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % html.escape(desc), s, 'description')
    s = sub1(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url, s, 'canonical')
    s = sub1(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % url, s, 'og:url')
    s = sub1(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % html.escape(title), s, 'og:title')
    s = sub1(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % html.escape(desc), s, 'og:description')
    s = sub1(r'<meta property="og:image" content="[^"]*">', '<meta property="og:image" content="%s">' % image, s, 'og:image')
    s = sub1(r'<meta name="twitter:image" content="[^"]*">', '<meta name="twitter:image" content="%s">' % image, s, 'twitter:image')
    art = {"@context": "https://schema.org", "@type": "Article", "headline": headline, "description": desc, "url": url,
           "inLanguage": "en", "image": image,
           "isPartOf": {"@type": "WebSite", "name": "Sanatan Dharma Saral", "url": SITE}, "mainEntityOfPage": url}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": chap, "item": '%sgita-%d.html' % (SITE, c)},
        {"@type": "ListItem", "position": 3, "name": headline, "item": url}]}
    js = lambda d: json.dumps(d, ensure_ascii=False).replace('</', '<\\/')
    s = sub1(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "Article".*?</script>',
             '<script type="application/ld+json">%s</script>' % js(art), s, 'article data')
    s = sub1(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "BreadcrumbList".*?</script>',
             '<script type="application/ld+json">%s</script>' % js(crumbs), s, 'breadcrumb data')
    s = hreflang_en(s, url, (SITE + 'hi/gita-%d-%d.html' % (c, n)) if hindi else None)
    s = sub1(r'<p class="kicker">.*?</p>', '<p class="kicker"><a href="gita-%d.html#v-gita-%d-%d" style="color:inherit">%s</a></p>' % (c, c, n, span(chap)), s, 'kicker')
    s = sub1(r'<h1>.*?</h1>', '<h1>%s</h1>' % span(headline), s, 'h1')
    s = sub1(r'<p class="lede[^"]*">.*?</p>', '<p class="lede %s">%s</p>' % (EN, e(v['tr'])), s, 'lede')
    main = ('<main class="wrap vpage">\n<section class="stack">\n' + article(c, v, True, False) + '\n</section>\n'
            + vnav(c, n) + '\n' + vback(c, n) + '\n</main>')
    return sub1(r'<main class="wrap vpage">.*?</main>', main, s, 'main')


def chapter_page(tpl, c, meta, verses, featured, hindi=False):
    n = len(verses)
    url = '%sgita-%d.html' % (SITE, c)
    title = 'Bhagavad Gita Chapter %d in English: All %d Verses Explained' % (c, n)
    desc = ('All %d verses of Bhagavad Gita Chapter %d (%s) in Sanskrit with transliteration, English translation and a '
            'word-by-word meaning of each verse.' % (n, c, meta['roman_name']))
    s = tpl
    s = s.replace('Bhagavad Gita Chapter 6 in English: All 47 Verses Explained', title)
    s = s.replace('All 47 verses of Bhagavad Gita Chapter 6 (Dhyana Yoga) in Sanskrit with transliteration, English translation and a simple explanation of each verse.', desc)
    s = s.replace(SITE + 'gita-6.html', url).replace(SITE + 'og/gita-6.png?v=2', SITE + 'og/gita-%d.png?v=2' % c)
    s = sub1(r'"inLanguage":\[[^\]]*\]', '"inLanguage":["en", "hi"]' if hindi else '"inLanguage":["en"]', s, 'inLanguage')
    s = sub1(r'"dateModified":"[^"]*"', '"dateModified":"%s"' % datetime.date.today().isoformat(), s, 'dateModified')
    s = hreflang_en(s, url, (SITE + 'hi/gita-%d.html' % c) if hindi else None)
    s = sub1(r'<p class="kicker">.*?</p>', '<p class="kicker">श्रीमद्भगवद्गीता · अध्याय %d</p>' % c, s, 'kicker')
    s = sub1(r'<h1>.*?</h1>', '<h1>%s</h1>' % span('Gita chapter %d: %s' % (c, meta['name'])), s, 'h1')
    s = sub1(r'<p class="lede[^"]*">.*?</p>', '<p class="lede %s">%s</p>' % (EN, e('All %d verses of chapter %d, each with Sanskrit, pronunciation, word meanings and a translation.' % (n, c))), s, 'lede')
    s = sub1(r'<svg aria-label="Chapter 6"', '<svg aria-label="Chapter %d"' % c, s, 'hero number label')
    s = sub1(r'(text-anchor="middle" x="100" y="128">)6(</text>)', 'text-anchor="middle" x="100" y="128">%d</text>' % c, s, 'hero number')
    row = ('<div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;margin-top:1.4rem">'
           + '<a class="more" href="gita-%d.html">%s</a>' % (c - 1, span('← Chapter %d' % (c - 1)))
           + '<a class="more" href="gita.html#ch%d">%s</a>' % (c, span('Chapter summary'))
           + ('<a class="more" href="gita-%d.html">%s</a>' % (c + 1, span('Chapter %d →' % (c + 1))) if os.path.exists('gita-%d.html' % (c + 1))
              else '<span class="ix-hint">%s</span>' % span('More chapters are being added.' if c < 18 else 'This is the last chapter.'))
           + '</div>')
    intro = ('Every verse of chapter %d, <i>%s</i>, with the Sanskrit, its pronunciation, the meaning of each word and a translation in '
             'simple English.' % (c, e(meta['skt_name'])))
    if featured:
        intro += ' Verses marked with a link are explained in depth on the main Gita page.'
    main = ('<main class="wrap">\n<section id="verses">\n<div class="sec-head">\n'
            + '<p class="eyebrow">%s</p>\n' % span('Chapter %d · %d verses' % (c, n))
            + '<h2>%s</h2>\n' % span(meta['name'])
            + '<p class="%s">%s</p><p class="%s">%s</p>\n</div>\n' % (EN, intro, EN, e(meta['outline']))
            + '<div class="toc">%s</div>' % ''.join('<a href="#v-gita-%d-%d">%d</a>' % (c, v['v'], v['v']) for v in verses)
            + row + '<div class="stack" style="margin-top:1.2rem">\n'
            + '\n'.join(article(c, v, False, v['v'] in featured) for v in verses)
            + '</div>' + row
            + '<p class="note" style="margin-top:1.4rem">%s</p>\n</section>\n</main>' % span(
                'Sanskrit text checked against three public-domain copies; transliteration generated in IAST; word meanings and '
                'translation written for this site in simple language. Please report any errors.'))
    return sub1(r'<main class="wrap">.*?</main>', main, s, 'main')


def link_previous_chapter(c):
    """Chapter c-1's page said more chapters were coming; point it at this one instead."""
    path = 'gita-%d.html' % (c - 1)
    s = open(path, encoding='utf-8').read()
    link = '<a class="more" href="gita-%d.html">%s</a>' % (c, span('Chapter %d →' % c))
    new = re.sub(r'<span class="ix-hint"><span class="[^"]*">More chapters are being added\.</span></span>', lambda m: link, s)
    if new != s:
        open(path, 'w', encoding='utf-8').write(new)


def link_hub(c, n):
    """On the Gita hub (and its language copies), add "Read all N verses of chapter C" under the chapter."""
    for lang in [''] + LANGS:
        path = (lang + '/' if lang else '') + 'gita.html'
        if not os.path.exists(path):
            continue
        s = open(path, encoding='utf-8').read()
        if re.search(r'href="[^"]*gita-%d\.html"' % c, s):
            continue
        # Each language already has this sentence for chapter 6; reuse its wording with the new numbers.
        m = re.search(r'<p style="margin-top:1rem"><a class="more" href="[^"]*gita-6\.html">(.*?)</a></p>\n', s, re.S)
        btn = '<p style="margin-top:1rem"><button class="read-btn" data-read-id="gita-ch%d"' % c
        if not m or s.count(btn) != 1:
            print('  hub link not added in', path)
            continue
        text = m.group(1).replace('47', str(n)).replace('४७', str(n))
        text = re.sub(r'6(?!\d)', str(c), text).replace('६', str(c))
        s = s.replace(btn, '<p style="margin-top:1rem"><a class="more" href="gita-%d.html">%s</a></p>\n%s' % (c, text, btn))
        open(path, 'w', encoding='utf-8').write(s)


def update_search(c, verses, featured, trs=None):
    path = 'search-index.js'
    s = open(path, encoding='utf-8').read()
    i, j = s.index('{'), s.rindex('}') + 1
    d = json.loads(s[i:j])
    page = 'gita-%d.html' % c
    d['pages'][page] = ['Gita chapter %d' % c, 'गीता अध्याय %d' % c]
    d['verses'] = [x for x in d['verses'] if x.get('page') != page]
    for v in verses:
        if v['v'] in featured:
            continue
        il = iast_lines(v)
        d['verses'].append({
            'page': page, 'id': 'v-gita-%d-%d' % (c, v['v']),
            't_en': '%d.%d · %s' % (c, v['v'], v['speaker']), 't_hi': ('%d.%d · %s' % (c, v['v'], HI_WHO[v['speaker']])) if trs else '',
            'r_en': 'Gita %d.%d' % (c, v['v']), 'r_hi': 'गीता %d.%d' % (c, v['v']),
            'skt': skt_html(v).replace('<br/>', '\n').replace(' ', ' '), 'iast': ' '.join(il),
            'tr_en': v['tr'], 'tr_hi': trs[v['v']] if trs else '', 's_en': '', 's_hi': '', 'words': []})
    open(path, 'w', encoding='utf-8').write(s[:i] + json.dumps(d, ensure_ascii=False) + s[j:])


def update_sitemap(urls):
    path = 'sitemap.xml'
    s = open(path, encoding='utf-8').read()
    today = datetime.date.today().isoformat()
    add = ''
    for u in urls:
        if '<loc>%s</loc>' % u in s:
            s = re.sub(r'<url><loc>%s</loc>(<lastmod>[^<]*</lastmod>)?</url>' % re.escape(u), '<url><loc>%s</loc><lastmod>%s</lastmod></url>' % (u, today), s)
        else:
            add += '<url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (u, today)
    s = s.replace('</urlset>', add + '</urlset>')
    open(path, 'w', encoding='utf-8').write(s)


def update_llms(c, meta, n):
    """llms.txt lists every chapter page; add this one after the previous chapter's line."""
    path = 'llms.txt'
    s = open(path, encoding='utf-8').read()
    if 'gita-%d.html' % c in s:
        return
    line = ('- [Bhagavad Gita Chapter %d in English: All %d Verses Explained](%sgita-%d.html): All %d verses of Bhagavad Gita '
            'Chapter %d (%s) in Sanskrit with transliteration, English translation and a word-by-word meaning of each verse.'
            % (c, n, SITE, c, n, c, meta['roman_name']))
    out, done = [], False
    for l in s.split('\n'):
        out.append(l)
        if '(%sgita-%d.html)' % (SITE, c - 1) in l:
            out.append(line); done = True
    if not done:
        raise SystemExit('llms.txt: no line for chapter %d to follow' % (c - 1))
    open(path, 'w', encoding='utf-8').write('\n'.join(out))


# ---------- Hindi ----------
# A chapter gets Hindi pages when tools/gita/content/hNN.py exists: META (name, outline) and T, a Hindi translation
# for every verse that has no page of its own yet. Verses that already had a Hindi page keep it, and their Hindi
# translation is read from that page. Like chapters 1 to 6, the Hindi pages carry the Sanskrit, pronunciation and
# translation; the word-by-word list stays on the English page, which each Hindi chapter page links to.

HI_WHO = {'Krishna': 'श्रीकृष्ण', 'Arjuna': 'अर्जुन', 'Sanjaya': 'संजय', 'Dhritarashtra': 'धृतराष्ट्र'}


def hspan(t):
    return '<span class="hi">%s</span>' % e(t)


def load_hindi(c, verses, featured):
    path = os.path.join(HERE, 'content', 'h%02d.py' % c)
    if not os.path.exists(path):
        return None, None
    ns = {}
    exec(open(path, encoding='utf-8').read(), ns)
    tr = {}
    for v in verses:
        n = v['v']
        if n in featured:
            page = open('hi/gita-%d-%d.html' % (c, n), encoding='utf-8').read()
            m = re.search(r'<span class="label"><span class="hi">अनुवाद</span></span><p class="hi">(.*?)</p>', page, re.S)
            if not m:
                raise SystemExit('no Hindi translation found on hi/gita-%d-%d.html' % (c, n))
            tr[n] = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
            if n in ns['T']:
                raise SystemExit('h%02d.py: verse %d already has a Hindi page; leave it out of T' % (c, n))
        elif n not in ns['T']:
            raise SystemExit('h%02d.py: no Hindi translation for verse %d' % (c, n))
        else:
            tr[n] = ns['T'][n].strip()
    extra = set(ns['T']) - {v['v'] for v in verses}
    if extra:
        raise SystemExit('h%02d.py: verses that do not exist: %s' % (c, sorted(extra)))
    return ns['META'], tr


def article_hi(c, v, tr, own_page, featured):
    n = v['v']
    ref = 'गीता %d.%d' % (c, n)
    head = '%d.%d · %s' % (c, n, HI_WHO[v['speaker']])
    src = ('<span class="src">%s</span>' % hspan(ref)) if own_page else ('<a class="src" href="/hi/gita-%d-%d.html">%s</a>' % (c, n, hspan(ref)))
    more = ('<p class="hi"><a class="more" href="/hi/gita.html#v-gita-%d-%d">पूरी व्याख्या पढ़ें →</a></p>' % (c, n)) if featured else ''
    q = urllib.parse.quote_plus('Gita %d.%d %d.%d · %s chanting' % (c, n, c, n, v['speaker']))
    return ('<article class="verse" id="v-gita-%d-%d">\n' % (c, n)
            + '<div class="v-head"><h3>%s</h3>%s</div>\n' % (hspan(head), src)
            + '<p class="skt">%s</p>\n' % skt_html(v)
            + '<p class="iast">%s</p>\n' % e('\n'.join(iast_lines(v)))
            + '<div><span class="label">%s</span><p class="hi">%s</p>%s</div>\n' % (hspan('अनुवाद'), e(tr), more)
            + '<p class="listen"><a href="https://www.youtube.com/results?search_query=%s" rel="noopener" target="_blank">%s</a>' % (q, hspan('▶ पाठ सुनें'))
            + '<a class="share-wa" href="https://wa.me/" rel="noopener" target="_blank">%s</a>' % hspan('WhatsApp पर भेजें')
            + '<button class="share-copy" type="button">%s</button><button class="v-save" type="button">%s</button>' % (hspan('कॉपी करें'), hspan('☆ सहेजें'))
            + '<button class="v-img" type="button">%s</button></p></article>' % hspan('🖼 चित्र'))


def vnav_hi(c, n):
    prev, nxt = neighbours(c, n, 'hi/')
    a = ''
    if prev:
        a += '<a class="vnav-prev" href="/hi/gita-%d-%d.html">%s</a>' % (prev[0], prev[1], hspan('← गीता %d.%d' % prev))
    if nxt:
        a += '<a class="vnav-next" href="/hi/gita-%d-%d.html">%s</a>' % (nxt[0], nxt[1], hspan('गीता %d.%d →' % nxt))
    return '<nav class="vnav" aria-label="More verses">%s</nav>' % a


def vback_hi(c, n):
    return '<p class="vback"><a class="more" href="/hi/gita-%d.html#v-gita-%d-%d">%s</a></p>' % (c, c, n, hspan('पूरे प्रसंग में पढ़ें →'))


def head_tags(s, title, desc, url, image):
    s = sub1(r'<title>.*?</title>', '<title>%s</title>' % e(title), s, 'title')
    s = sub1(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % html.escape(desc), s, 'description')
    s = sub1(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url, s, 'canonical')
    s = sub1(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % url, s, 'og:url')
    s = sub1(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % html.escape(title), s, 'og:title')
    s = sub1(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % html.escape(desc), s, 'og:description')
    s = sub1(r'<meta (?:property="og:image" content="[^"]*"|content="[^"]*" property="og:image")/?>', '<meta property="og:image" content="%s">' % image, s, 'og:image')
    s = sub1(r'<meta (?:name="twitter:image" content="[^"]*"|content="[^"]*" name="twitter:image")/?>', '<meta name="twitter:image" content="%s">' % image, s, 'twitter:image')
    return s


def ld(s, kind, data):
    js = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    return sub1(r'<script type="application/ld\+json">\{"@context": ?"https://schema.org", ?"@type": ?"%s".*?</script>' % kind,
                '<script type="application/ld+json">%s</script>' % js, s, kind + ' data')


def verse_page_hi(tpl, c, meta, mhi, v, tr):
    n = v['v']
    url = '%shi/gita-%d-%d.html' % (SITE, c, n)
    first = v['skt'][0]
    title = 'गीता %d.%d: %s | सनातन धर्म सरल' % (c, n, first)
    headline = 'गीता %d.%d: %s' % (c, n, first)
    chap = 'गीता अध्याय %d: %s' % (c, mhi['name'])
    image = SITE + 'og/gita-%d.png?v=2' % c
    s = head_tags(tpl, title, shorten(tr, 160), url, image)
    s = ld(s, 'Article', {"@context": "https://schema.org", "@type": "Article", "headline": headline, "description": shorten(tr, 160),
                          "url": url, "inLanguage": "hi", "image": image,
                          "isPartOf": {"@type": "WebSite", "name": "Sanatan Dharma Saral", "url": SITE}, "mainEntityOfPage": url})
    s = ld(s, 'BreadcrumbList', {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "सनातन धर्म सरल", "item": SITE + 'hi/'},
        {"@type": "ListItem", "position": 2, "name": chap, "item": '%shi/gita-%d.html' % (SITE, c)},
        {"@type": "ListItem", "position": 3, "name": headline, "item": url}]})
    s = hreflang_en(s, '%sgita-%d-%d.html' % (SITE, c, n), url)
    s = sub1(r'<p class="kicker">.*?</p>', '<p class="kicker"><a href="/hi/gita-%d.html#v-gita-%d-%d" style="color:inherit">%s</a></p>' % (c, c, n, hspan(chap)), s, 'kicker')
    s = sub1(r'<h1>.*?</h1>', '<h1>%s</h1>' % hspan(headline), s, 'h1')
    s = sub1(r'<p class="lede[^"]*">.*?</p>', '<p class="lede hi">%s</p>' % e(tr), s, 'lede')
    main = ('<main class="wrap vpage">\n<section class="stack">\n' + article_hi(c, v, tr, True, False) + '\n</section>\n'
            + vnav_hi(c, n) + '\n' + vback_hi(c, n) + '\n</main>')
    return sub1(r'<main class="wrap vpage">.*?</main>', main, s, 'main')


def chapter_page_hi(tpl, c, meta, mhi, verses, trs, featured):
    n = len(verses)
    url = '%shi/gita-%d.html' % (SITE, c)
    name = 'गीता अध्याय %d: %s' % (c, mhi['name'])
    title = '%s | सनातन धर्म सरल' % name
    desc = 'अध्याय %d के सभी %d श्लोक, हर एक संस्कृत, उच्चारण और सरल हिन्दी अनुवाद के साथ।' % (c, n)
    image = SITE + 'og/gita-%d.png?v=2' % c
    s = head_tags(tpl, title, desc, url, image)
    s = sub1(r'<script type="application/ld\+json">\{"@context":"https://schema.org","@type":"BreadcrumbList".*?</script>',
             '<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "सनातन धर्म सरल", "item": SITE + 'hi/'},
                 {"@type": "ListItem", "position": 2, "name": "भगवद्गीता", "item": SITE + 'hi/gita.html'},
                 {"@type": "ListItem", "position": 3, "name": name, "item": url}]}, ensure_ascii=False), s, 'breadcrumb data')
    s = sub1(r'<script type="application/ld\+json">\{"@context":"https://schema.org","@type":"Article".*?</script>',
             '<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": name,
                 "description": desc, "image": image, "inLanguage": "hi", "url": url, "mainEntityOfPage": url,
                 "dateModified": datetime.date.today().isoformat(),
                 "isPartOf": {"@type": "WebSite", "name": "Sanatan Dharma Saral", "url": SITE}}, ensure_ascii=False), s, 'article data')
    s = hreflang_en(s, '%sgita-%d.html' % (SITE, c), url)
    s = sub1(r'<p class="kicker">.*?</p>', '<p class="kicker">श्रीमद्भगवद्गीता · अध्याय %d</p>' % c, s, 'kicker')
    s = sub1(r'<h1>.*?</h1>', '<h1>%s</h1>' % hspan(name), s, 'h1')
    s = sub1(r'<p class="lede[^"]*">.*?</p>', '<p class="lede hi">%s</p>' % e(desc), s, 'lede')
    s = sub1(r'<svg aria-label="Chapter 6"', '<svg aria-label="Chapter %d"' % c, s, 'hero number label')
    s = sub1(r'(text-anchor="middle" x="100" y="128">)6(</text>)', 'text-anchor="middle" x="100" y="128">%d</text>' % c, s, 'hero number')
    nxt = os.path.exists('hi/gita-%d.html' % (c + 1))
    row = ('<div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;margin-top:1.4rem">'
           + '<a class="more" href="/hi/gita-%d.html">%s</a>' % (c - 1, hspan('← अध्याय %d' % (c - 1)))
           + '<a class="more" href="/hi/gita.html#ch%d">%s</a>' % (c, hspan('अध्याय का सार'))
           + ('<a class="more" href="/hi/gita-%d.html">%s</a>' % (c + 1, hspan('अध्याय %d →' % (c + 1))) if nxt
              else '<span class="ix-hint">%s</span>' % hspan('और अध्याय जोड़े जा रहे हैं।' if c < 18 else 'यह अन्तिम अध्याय है।'))
           + '</div>')
    intro = ('अध्याय %d, <i>%s</i>, का हर श्लोक: संस्कृत, उच्चारण और सरल हिन्दी में अनुवाद। हर शब्द का अर्थ '
             '<a href="/gita-%d.html">अंग्रेज़ी पृष्ठ</a> पर है।' % (c, e(meta['skt_name']), c))
    if featured:
        intro += ' जिन श्लोकों के साथ लिंक है, उनकी विस्तृत व्याख्या मुख्य गीता पृष्ठ पर है।'
    main = ('<main class="wrap">\n<section id="verses">\n<div class="sec-head">\n'
            + '<p class="eyebrow">%s</p>\n' % hspan('अध्याय %d · %d श्लोक' % (c, n))
            + '<h2>%s</h2>\n' % hspan(mhi['name'])
            + '<p class="hi">%s</p><p class="hi">%s</p>\n</div>\n' % (intro, e(mhi['outline']))
            + '<div class="toc">%s</div>' % ''.join('<a href="/hi/gita-%d.html#v-gita-%d-%d">%d</a>' % (c, c, v['v'], v['v']) for v in verses)
            + row + '<div class="stack" style="margin-top:1.2rem">\n'
            + '\n'.join(article_hi(c, v, trs[v['v']], False, v['v'] in featured) for v in verses)
            + '</div>' + row
            + '<p class="note" style="margin-top:1.4rem">%s</p>\n</section>\n</main>' % hspan(
                'संस्कृत पाठ तीन सार्वजनिक संस्करणों से मिलाकर; उच्चारण IAST में; अनुवाद इस साइट के लिए सरल भाषा में लिखे गए। '
                'कोई त्रुटि दिखे तो बताएँ।'))
    return sub1(r'<main class="wrap">.*?</main>', main, s, 'main')



def build_hindi(c, meta, mhi, verses, trs, featured):
    vtpl = open('hi/gita-6-10.html', encoding='utf-8').read()
    ctpl = open('hi/gita-6.html', encoding='utf-8').read()
    for v in verses:
        path = 'hi/gita-%d-%d.html' % (c, v['v'])
        if v['v'] not in featured and not os.path.exists(path):
            open(path, 'w', encoding='utf-8').write('')
    made = 0
    for v in verses:
        n = v['v']
        path = 'hi/gita-%d-%d.html' % (c, n)
        if n in featured:
            s = open(path, encoding='utf-8').read()
            s = sub1(r'<nav class="vnav"[^>]*>.*?</nav>', vnav_hi(c, n), s, 'verse links in ' + path)
            s = sub1(r'<p class="vback">.*?</p>', vback_hi(c, n), s, 'context link in ' + path)
            open(path, 'w', encoding='utf-8').write(s)
        else:
            open(path, 'w', encoding='utf-8').write(verse_page_hi(vtpl, c, meta, mhi, v, trs[n]))
            made += 1
    open('hi/gita-%d.html' % c, 'w', encoding='utf-8').write(chapter_page_hi(ctpl, c, meta, mhi, verses, trs, featured))
    # the chapter before: its last verse and its chapter page now lead here
    last = 'hi/gita-%d-%d.html' % (c - 1, COUNTS[c - 1])
    if os.path.exists(last):
        s = open(last, encoding='utf-8').read()
        s = sub1(r'<nav class="vnav"[^>]*>.*?</nav>', vnav_hi(c - 1, COUNTS[c - 1]), s, 'verse links in ' + last)
        open(last, 'w', encoding='utf-8').write(s)
    prev = 'hi/gita-%d.html' % (c - 1)
    s = open(prev, encoding='utf-8').read()
    s2 = s.replace('<span class="ix-hint"><span class="hi">और अध्याय जोड़े जा रहे हैं।</span></span>',
                   '<a class="more" href="/hi/gita-%d.html">%s</a>' % (c, hspan('अध्याय %d →' % c)))
    if s2 != s:
        open(prev, 'w', encoding='utf-8').write(s2)
    # the Hindi Gita hub sent readers to the English chapter; send them to the Hindi one
    s = open('hi/gita.html', encoding='utf-8').read()
    s2 = re.sub(r'(<p style="margin-top:1rem"><a class="more" href=")gita-%d\.html(">)' % c, r'\g<1>/hi/gita-%d.html\2' % c, s)
    if s2 == s and 'href="/hi/gita-%d.html"' % c not in s:
        print('  Hindi hub link not changed')
    open('hi/gita.html', 'w', encoding='utf-8').write(s2)
    return made


def main():
    c = int(sys.argv[1])
    data = json.load(open(os.path.join(HERE, 'ch%02d.json' % c), encoding='utf-8'))
    meta, verses = data['meta'], data['verses']
    assert len(verses) == COUNTS[c], 'chapter %d should have %d verses' % (c, COUNTS[c])
    featured = set(meta.get('featured', []))
    mhi, trs = load_hindi(c, verses, featured)
    hindi = mhi is not None
    vtpl = open('gita-6-10.html', encoding='utf-8').read()
    ctpl = open('gita-6.html', encoding='utf-8').read()
    # First pass: every verse page must exist before previous/next links are worked out.
    for v in verses:
        path = 'gita-%d-%d.html' % (c, v['v'])
        if v['v'] not in featured and not os.path.exists(path):
            open(path, 'w', encoding='utf-8').write('')
    made = 0
    for v in verses:
        path = 'gita-%d-%d.html' % (c, v['v'])
        if v['v'] in featured:
            s = open(path, encoding='utf-8').read()
            s = sub1(r'<nav class="vnav"[^>]*>.*?</nav>', vnav(c, v['v']), s, 'verse links in ' + path)
            s = sub1(r'<p class="vback">.*?</p>', vback(c, v['v']), s, 'context link in ' + path)
            open(path, 'w', encoding='utf-8').write(s)
        else:
            open(path, 'w', encoding='utf-8').write(verse_page(vtpl, c, meta, v, hindi))
            made += 1
    open('gita-%d.html' % c, 'w', encoding='utf-8').write(chapter_page(ctpl, c, meta, verses, featured, hindi))
    # The last verse of the chapter before now has a next verse.
    last = 'gita-%d-%d.html' % (c - 1, COUNTS[c - 1])
    if c > 1 and os.path.exists(last):
        s = open(last, encoding='utf-8').read()
        s = sub1(r'<nav class="vnav"[^>]*>.*?</nav>', vnav(c - 1, COUNTS[c - 1]), s, 'verse links in ' + last)
        open(last, 'w', encoding='utf-8').write(s)
    link_previous_chapter(c)
    link_hub(c, len(verses))
    update_search(c, verses, featured, trs)
    update_llms(c, meta, len(verses))
    update_sitemap([SITE + 'gita-%d.html' % c] + ['%sgita-%d-%d.html' % (SITE, c, v['v']) for v in verses])
    if hindi:
        made_hi = build_hindi(c, meta, mhi, verses, trs, featured)
        update_sitemap([SITE + 'hi/gita-%d.html' % c] + ['%shi/gita-%d-%d.html' % (SITE, c, v['v']) for v in verses])
        print('chapter %d in Hindi: %d verse pages written, chapter page written' % (c, made_hi))
    print('chapter %d: %d verse pages written, %d featured pages relinked, chapter page written' % (c, made, len(featured)))


if __name__ == '__main__':
    main()
