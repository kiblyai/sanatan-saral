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


def hreflang_en(s, url, alts=None):
    """English plus the other languages the page exists in; any alternates the template had are removed."""
    if isinstance(alts, str):
        alts = {'hi': alts}
    s = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n', '', s)
    block = '<link rel="alternate" hreflang="en" href="%s">\n' % url
    for l, u in (alts or {}).items():
        block += '<link rel="alternate" hreflang="%s" href="%s">\n' % (l, u)
    block += '<link rel="alternate" hreflang="x-default" href="%s">\n' % url
    return s.replace('</head>', block + '</head>', 1)


def shorten(t, limit=150):
    if len(t) <= limit:
        return t
    return t[:limit].rsplit(' ', 1)[0].rstrip(',;:') + '…'


def verse_page(tpl, c, meta, v, present=()):
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
    s = hreflang_en(s, url, alternates(c, n, present)[1])
    s = sub1(r'<p class="kicker">.*?</p>', '<p class="kicker"><a href="gita-%d.html#v-gita-%d-%d" style="color:inherit">%s</a></p>' % (c, c, n, span(chap)), s, 'kicker')
    s = sub1(r'<h1>.*?</h1>', '<h1>%s</h1>' % span(headline), s, 'h1')
    s = sub1(r'<p class="lede[^"]*">.*?</p>', '<p class="lede %s">%s</p>' % (EN, e(v['tr'])), s, 'lede')
    main = ('<main class="wrap vpage">\n<section class="stack">\n' + article(c, v, True, False) + '\n</section>\n'
            + vnav(c, n) + '\n' + vback(c, n) + '\n</main>')
    return sub1(r'<main class="wrap vpage">.*?</main>', main, s, 'main')


def chapter_page(tpl, c, meta, verses, featured, present=()):
    n = len(verses)
    url = '%sgita-%d.html' % (SITE, c)
    title = 'Bhagavad Gita Chapter %d in English: All %d Verses Explained' % (c, n)
    desc = ('All %d verses of Bhagavad Gita Chapter %d (%s) in Sanskrit with transliteration, English translation and a '
            'word-by-word meaning of each verse.' % (n, c, meta['roman_name']))
    s = tpl
    s = s.replace('Bhagavad Gita Chapter 6 in English: All 47 Verses Explained', title)
    s = s.replace('All 47 verses of Bhagavad Gita Chapter 6 (Dhyana Yoga) in Sanskrit with transliteration, English translation and a simple explanation of each verse.', desc)
    s = s.replace(SITE + 'gita-6.html', url).replace(SITE + 'og/gita-6.png?v=2', SITE + 'og/gita-%d.png?v=2' % c)
    s = sub1(r'"inLanguage":\[[^\]]*\]', '"inLanguage":%s' % json.dumps(['en'] + list(present)), s, 'inLanguage')
    s = sub1(r'"dateModified":"[^"]*"', '"dateModified":"%s"' % datetime.date.today().isoformat(), s, 'dateModified')
    s = hreflang_en(s, url, alternates(c, None, present)[1])
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
            't_en': '%d.%d · %s' % (c, v['v'], v['speaker']), 't_hi': ('%d.%d · %s' % (c, v['v'], LG.L['hi']['who'][v['speaker']])) if trs else '',
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


# ---------- Other languages ----------
# A chapter gets pages in a language when its content file exists (see langs.py): META (outline, and for Hindi the
# chapter name) and T, a translation for every verse that has no page of its own in that language yet. Verses that
# already had a page keep it, and their translation is read from that page. Like chapters 1 to 6 in these languages,
# the pages carry the Sanskrit, pronunciation and translation; the word-by-word list stays on the English page, which
# each chapter page links to. The chapter name comes from the language's own Gita hub.

import langs as LG


def num(lang, x):
    d = LG.L[lang].get('digits')
    x = str(x)
    return ''.join(d[int(ch)] if d and ch.isdigit() else ch for ch in x)


def fmt(lang, key, **kw):
    return LG.L[lang][key].format(**{k: (num(lang, v) if isinstance(v, int) else v) for k, v in kw.items()})


def lspan(lang, t):
    return '<span class="%s">%s</span>' % (lang, e(t))


def langs_for(c):
    """The languages that have a content file for chapter c."""
    return [l for l in LG.ORDER if l in LG.L and os.path.exists(os.path.join(HERE, 'content', LG.L[l]['file'] % c))]


def hub_name(lang, c):
    s = open('%s/gita.html' % lang, encoding='utf-8').read()
    i = s.find('id="ch%d"' % c)
    m = re.search(r'<h2[^>]*><span class="%s">(.*?)</span>' % lang, s[i:i + 3000], re.S)
    if i < 0 or not m:
        raise SystemExit('%s/gita.html: no name for chapter %d' % (lang, c))
    return html.unescape(m.group(1)).strip()


def load_lang(lang, c, verses, featured):
    path = os.path.join(HERE, 'content', LG.L[lang]['file'] % c)
    ns = {}
    exec(open(path, encoding='utf-8').read(), ns)
    meta = dict(ns['META'])
    meta.setdefault('name', hub_name(lang, c))
    tr = {}
    prev = None
    for v in verses:
        n = v['v']
        if n in featured:
            page = open('%s/gita-%d-%d.html' % (lang, c, n), encoding='utf-8').read()
            m = re.search(r'<span class="label"><span class="%s">[^<]*</span></span><p class="%s">(.*?)</p>' % (lang, lang), page, re.S)
            if not m:
                raise SystemExit('no translation found on %s/gita-%d-%d.html' % (lang, c, n))
            tr[n] = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
            if n in ns['T']:
                raise SystemExit('%s: verse %d already has its own page; leave it out of T' % (path, n))
        elif n not in ns['T']:
            raise SystemExit('%s: no translation for verse %d' % (path, n))
        else:
            tr[n] = ns['T'][n].strip()
            said = LG.L[lang]['said'][v['speaker']]
            if prev != v['speaker'] and not tr[n].startswith(said):
                print('  %s %d.%d: the speaker changes, so the translation should start with "%s"' % (lang, c, n, said))
            if prev == v['speaker'] and any(tr[n].startswith(x) for x in LG.L[lang]['said'].values()):
                print('  %s %d.%d: starts with "... said:" but the speaker has not changed' % (lang, c, n))
        prev = v['speaker']
    extra = set(ns['T']) - {v['v'] for v in verses}
    if extra:
        raise SystemExit('%s: verses that do not exist: %s' % (path, sorted(extra)))
    return meta, tr


def article_l(lang, c, v, tr, own_page, featured):
    W = LG.L[lang]
    n = v['v']
    ref = '%s %s' % (W['gita'], num(lang, '%d.%d' % (c, n)))
    head = '%s · %s' % (num(lang, '%d.%d' % (c, n)), W['who'][v['speaker']])
    src = ('<span class="src">%s</span>' % lspan(lang, ref)) if own_page else ('<a class="src" href="/%s/gita-%d-%d.html">%s</a>' % (lang, c, n, lspan(lang, ref)))
    more = ('<p class="%s"><a class="more" href="/%s/gita.html#v-gita-%d-%d">%s</a></p>' % (lang, lang, c, n, W['more'])) if featured else ''
    q = urllib.parse.quote_plus('Gita %d.%d %d.%d · %s chanting' % (c, n, c, n, v['speaker']))
    return ('<article class="verse" id="v-gita-%d-%d">\n' % (c, n)
            + '<div class="v-head"><h3>%s</h3>%s</div>\n' % (lspan(lang, head), src)
            + '<p class="skt">%s</p>\n' % skt_html(v)
            + '<p class="iast">%s</p>\n' % e('\n'.join(iast_lines(v)))
            + '<div><span class="label">%s</span><p class="%s">%s</p>%s</div>\n' % (lspan(lang, W['tr']), lang, e(tr), more)
            + '<p class="listen"><a href="https://www.youtube.com/results?search_query=%s" rel="noopener" target="_blank">%s</a>' % (q, lspan(lang, W['listen']))
            + '<a class="share-wa" href="https://wa.me/" rel="noopener" target="_blank">%s</a>' % lspan(lang, W['wa'])
            + '<button class="share-copy" type="button">%s</button><button class="v-save" type="button">%s</button>' % (lspan(lang, W['copy']), lspan(lang, W['save']))
            + '<button class="v-img" type="button">%s</button></p></article>' % lspan(lang, W['img']))


def vnav_l(lang, c, n):
    W = LG.L[lang]
    prev, nxt = neighbours(c, n, lang + '/')
    a = ''
    if prev:
        a += '<a class="vnav-prev" href="/%s/gita-%d-%d.html">%s</a>' % (lang, prev[0], prev[1], lspan(lang, '← %s %s' % (W['gita'], num(lang, '%d.%d' % prev))))
    if nxt:
        a += '<a class="vnav-next" href="/%s/gita-%d-%d.html">%s</a>' % (lang, nxt[0], nxt[1], lspan(lang, '%s %s →' % (W['gita'], num(lang, '%d.%d' % nxt))))
    return '<nav class="vnav" aria-label="More verses">%s</nav>' % a


def vback_l(lang, c, n):
    return '<p class="vback"><a class="more" href="/%s/gita-%d.html#v-gita-%d-%d">%s</a></p>' % (lang, c, c, n, lspan(lang, LG.L[lang]['vback']))


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


def alternates(c, n, present):
    """hreflang links for a chapter page (n None) or verse page, in every language it has."""
    path = ('gita-%d.html' % c) if n is None else ('gita-%d-%d.html' % (c, n))
    return SITE + path, {l: '%s%s/%s' % (SITE, l, path) for l in present}


def verse_page_l(lang, tpl, c, meta, mloc, v, tr, present):
    W = LG.L[lang]
    n = v['v']
    url = '%s%s/gita-%d-%d.html' % (SITE, lang, c, n)
    first = v['skt'][0]
    headline = '%s %s: %s' % (W['gita'], num(lang, '%d.%d' % (c, n)), first)
    title = '%s | %s' % (headline, W['site'])
    chap = '%s: %s' % (fmt(lang, 'chapter', c=c), mloc['name'])
    image = SITE + 'og/gita-%d.png?v=2' % c
    s = head_tags(tpl, title, shorten(tr, 160), url, image)
    s = ld(s, 'Article', {"@context": "https://schema.org", "@type": "Article", "headline": headline, "description": shorten(tr, 160),
                          "url": url, "inLanguage": lang, "image": image,
                          "isPartOf": {"@type": "WebSite", "name": "Sanatan Dharma Saral", "url": SITE}, "mainEntityOfPage": url})
    s = ld(s, 'BreadcrumbList', {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": W['site'], "item": SITE + lang + '/'},
        {"@type": "ListItem", "position": 2, "name": chap, "item": '%s%s/gita-%d.html' % (SITE, lang, c)},
        {"@type": "ListItem", "position": 3, "name": headline, "item": url}]})
    en, alts = alternates(c, n, present)
    s = hreflang_en(s, en, alts)
    s = sub1(r'<p class="kicker">.*?</p>', '<p class="kicker"><a href="/%s/gita-%d.html#v-gita-%d-%d" style="color:inherit">%s</a></p>' % (lang, c, c, n, lspan(lang, chap)), s, 'kicker')
    s = sub1(r'<h1>.*?</h1>', '<h1>%s</h1>' % lspan(lang, headline), s, 'h1')
    s = sub1(r'<p class="lede[^"]*">.*?</p>', '<p class="lede %s">%s</p>' % (lang, e(tr)), s, 'lede')
    main = ('<main class="wrap vpage">\n<section class="stack">\n' + article_l(lang, c, v, tr, True, False) + '\n</section>\n'
            + vnav_l(lang, c, n) + '\n' + vback_l(lang, c, n) + '\n</main>')
    return sub1(r'<main class="wrap vpage">.*?</main>', main, s, 'main')


def chapter_page_l(lang, tpl, c, meta, mloc, verses, trs, featured, present):
    W = LG.L[lang]
    n = len(verses)
    url = '%s%s/gita-%d.html' % (SITE, lang, c)
    name = '%s: %s' % (fmt(lang, 'chapter', c=c), mloc['name'])
    title = '%s | %s' % (name, W['site'])
    desc = fmt(lang, 'desc', c=c, n=n)
    image = SITE + 'og/gita-%d.png?v=2' % c
    s = head_tags(tpl, title, desc, url, image)
    s = sub1(r'<script type="application/ld\+json">\{"@context":"https://schema.org","@type":"BreadcrumbList".*?</script>',
             '<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": W['site'], "item": SITE + lang + '/'},
                 {"@type": "ListItem", "position": 2, "name": W['hub'], "item": SITE + lang + '/gita.html'},
                 {"@type": "ListItem", "position": 3, "name": name, "item": url}]}, ensure_ascii=False), s, 'breadcrumb data')
    s = sub1(r'<script type="application/ld\+json">\{"@context":"https://schema.org","@type":"Article".*?</script>',
             '<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": name,
                 "description": desc, "image": image, "inLanguage": lang, "url": url, "mainEntityOfPage": url,
                 "dateModified": datetime.date.today().isoformat(),
                 "isPartOf": {"@type": "WebSite", "name": "Sanatan Dharma Saral", "url": SITE}}, ensure_ascii=False), s, 'article data')
    en, alts = alternates(c, None, present)
    s = hreflang_en(s, en, alts)
    s = sub1(r'<p class="kicker">.*?</p>', '<p class="kicker">श्रीमद्भगवद्गीता · अध्याय %d</p>' % c, s, 'kicker')  # the same on every language's chapter pages
    s = sub1(r'<h1>.*?</h1>', '<h1>%s</h1>' % lspan(lang, name), s, 'h1')
    s = sub1(r'<p class="lede[^"]*">.*?</p>', '<p class="lede %s">%s</p>' % (lang, e(desc)), s, 'lede')
    s = sub1(r'<svg aria-label="Chapter 6"', '<svg aria-label="Chapter %d"' % c, s, 'hero number label')
    s = sub1(r'(text-anchor="middle" x="100" y="128">)[^<]*(</text>)', 'text-anchor="middle" x="100" y="128">%d</text>' % c, s, 'hero number')
    nxt = os.path.exists('%s/gita-%d.html' % (lang, c + 1))
    row = ('<div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;margin-top:1.4rem">'
           + '<a class="more" href="/%s/gita-%d.html">%s</a>' % (lang, c - 1, lspan(lang, fmt(lang, 'prev', p=c - 1)))
           + '<a class="more" href="/%s/gita.html#ch%d">%s</a>' % (lang, c, lspan(lang, W['summary']))
           + ('<a class="more" href="/%s/gita-%d.html">%s</a>' % (lang, c + 1, lspan(lang, fmt(lang, 'next', c=c + 1))) if nxt
              else '<span class="ix-hint">%s</span>' % lspan(lang, W['hint'] if c < 18 else W['last']))
           + '</div>')
    intro = fmt(lang, 'intro', c=c, skt=e(meta['skt_name'])).replace('/gita-%s.html' % num(lang, c), '/gita-%d.html' % c)
    if featured:
        intro += ' ' + W['featured_note']
    main = ('<main class="wrap">\n<section id="verses">\n<div class="sec-head">\n'
            + '<p class="eyebrow">%s</p>\n' % lspan(lang, fmt(lang, 'eyebrow', c=c, n=n))
            + '<h2>%s</h2>\n' % lspan(lang, mloc['name'])
            + '<p class="%s">%s</p><p class="%s">%s</p>\n</div>\n' % (lang, intro, lang, e(mloc['outline']))
            + '<div class="toc">%s</div>' % ''.join('<a href="/%s/gita-%d.html#v-gita-%d-%d">%d</a>' % (lang, c, c, v['v'], v['v']) for v in verses)
            + row + '<div class="stack" style="margin-top:1.2rem">\n'
            + '\n'.join(article_l(lang, c, v, trs[v['v']], False, v['v'] in featured) for v in verses)
            + '</div>' + row
            + '<p class="note" style="margin-top:1.4rem">%s</p>\n</section>\n</main>' % lspan(lang, W['note']))
    return sub1(r'<main class="wrap">.*?</main>', main, s, 'main')


def build_lang(lang, c, meta, mloc, verses, trs, featured, present):
    W = LG.L[lang]
    vtpl = open('%s/gita-6-10.html' % lang, encoding='utf-8').read()
    ctpl = open('%s/gita-6.html' % lang, encoding='utf-8').read()
    for v in verses:
        path = '%s/gita-%d-%d.html' % (lang, c, v['v'])
        if v['v'] not in featured and not os.path.exists(path):
            open(path, 'w', encoding='utf-8').write('')
    made = 0
    for v in verses:
        n = v['v']
        path = '%s/gita-%d-%d.html' % (lang, c, n)
        if n in featured:
            s = open(path, encoding='utf-8').read()
            s = sub1(r'<nav class="vnav"[^>]*>.*?</nav>', vnav_l(lang, c, n), s, 'verse links in ' + path)
            s = sub1(r'<p class="vback">.*?</p>', vback_l(lang, c, n), s, 'context link in ' + path)
            open(path, 'w', encoding='utf-8').write(s)
        else:
            open(path, 'w', encoding='utf-8').write(verse_page_l(lang, vtpl, c, meta, mloc, v, trs[n], present))
            made += 1
    open('%s/gita-%d.html' % (lang, c), 'w', encoding='utf-8').write(chapter_page_l(lang, ctpl, c, meta, mloc, verses, trs, featured, present))
    # the chapter before: its last verse and its chapter page now lead here
    last = '%s/gita-%d-%d.html' % (lang, c - 1, COUNTS[c - 1])
    if os.path.exists(last):
        s = open(last, encoding='utf-8').read()
        s = sub1(r'<nav class="vnav"[^>]*>.*?</nav>', vnav_l(lang, c - 1, COUNTS[c - 1]), s, 'verse links in ' + last)
        open(last, 'w', encoding='utf-8').write(s)
    prev = '%s/gita-%d.html' % (lang, c - 1)
    s = open(prev, encoding='utf-8').read()
    s2 = s.replace('<span class="ix-hint">%s</span>' % lspan(lang, W['hint']),
                   '<a class="more" href="/%s/gita-%d.html">%s</a>' % (lang, c, lspan(lang, fmt(lang, 'next', c=c))))
    if s2 != s:
        open(prev, 'w', encoding='utf-8').write(s2)
    # the language's Gita hub sent readers to the English chapter; send them to this one, with the right numbers
    s = open('%s/gita.html' % lang, encoding='utf-8').read()
    m6 = re.search(r'<p style="margin-top:1rem"><a class="more" href="/%s/gita-6\.html"><span class="%s">([^<]*)</span></a></p>' % (lang, lang), s)
    if m6:
        text = m6.group(1).replace(num(lang, 47), num(lang, len(verses)))
        text = re.sub(r'%s(?![%s0-9])' % (re.escape(num(lang, 6)), re.escape(num(lang, '0123456789'))), num(lang, c), text)
        s2 = re.sub(r'<p style="margin-top:1rem"><a class="more" href="(?:/%s/)?gita-%d\.html">.*?</a></p>' % (lang, c),
                    lambda m: '<p style="margin-top:1rem"><a class="more" href="/%s/gita-%d.html">%s</a></p>' % (lang, c, lspan(lang, text)), s, count=1)
        if s2 == s and 'href="/%s/gita-%d.html"' % (lang, c) not in s:
            print('  %s hub link not changed' % lang)
        open('%s/gita.html' % lang, 'w', encoding='utf-8').write(s2)
    else:
        print('  %s hub: chapter 6 link not found' % lang)
    return made


def main():
    c = int(sys.argv[1])
    data = json.load(open(os.path.join(HERE, 'ch%02d.json' % c), encoding='utf-8'))
    meta, verses = data['meta'], data['verses']
    assert len(verses) == COUNTS[c], 'chapter %d should have %d verses' % (c, COUNTS[c])
    featured = set(meta.get('featured', []))
    present = langs_for(c)
    loc = {l: load_lang(l, c, verses, featured) for l in present}
    trs = loc['hi'][1] if 'hi' in loc else None
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
            open(path, 'w', encoding='utf-8').write(verse_page(vtpl, c, meta, v, present))
            made += 1
    open('gita-%d.html' % c, 'w', encoding='utf-8').write(chapter_page(ctpl, c, meta, verses, featured, present))
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
    for l in present:
        made_l = build_lang(l, c, meta, loc[l][0], verses, loc[l][1], featured, present)
        update_sitemap(['%s%s/gita-%d.html' % (SITE, l, c)] + ['%s%s/gita-%d-%d.html' % (SITE, l, c, v['v']) for v in verses])
        print('chapter %d in %s: %d verse pages written, chapter page written' % (c, l, made_l))
    print('chapter %d: %d verse pages written, %d featured pages relinked, chapter page written' % (c, made, len(featured)))


if __name__ == '__main__':
    main()
