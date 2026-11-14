#!/usr/bin/env python3
"""Make a language's copy of a page from its Hindi page.

    python3 -I tools/page_translate.py extract makar-sankranti       # print what needs translating, numbered
    python3 -I tools/page_translate.py extract rigveda kn            # same, showing what the site already has in Kannada
    python3 -I tools/page_translate.py build makar-sankranti te kn   # write te/makar-sankranti.html, kn/...

The Hindi page (hi/<page>.html) is the pattern: same sections, same Sanskrit, same scripts. Each language's text is in
tools/pages/<page>/<lang>.py:

    TITLE = '...'        # <title> and og:title, before " | site name"
    DESC = '...'         # meta description and og:description
    S = ['...', ...]     # one entry per Hindi text piece, in the order `extract` prints them; None = reuse the
                         # translation the site already has for that exact text (extract <page> <lang> shows them)
    JS = {'Hindi string in a script': 'translation', ...}   # optional: strings inside the page's own scripts
    EXTRA = [('old', 'new'), ...]                            # optional: any other exact replacement in the body
    COUNT = ['... {n} days to go', '... tomorrow!', '... today!']   # optional: the countdown line (date from the Hindi page)
    KICKER = '...'       # optional: the small line above the title (it has no language class on the Hindi page)
    WA = '...'           # optional: WhatsApp share text; the language page's link is added after it

A text piece is the inside of an element whose class includes "hi" (span, p, li, tspan, ul). Links to /hi/x.html go to
/<lang>/x.html when that page exists in the language, otherwise to the English page. The menu bar, footer and the
language's own fonts come from <lang>/gita.html. Afterwards run tools/split_languages.py as usual.
"""
import html as H, importlib.util, json, os, re, sys, urllib.parse

sys.dont_write_bytecode = True
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SITE = 'https://sanatan.space/'
ORDER = ['hi', 'gu', 'te', 'mr', 'ta', 'bn', 'kn', 'ml']
LOCALE = {'gu': 'gu_IN', 'te': 'te_IN', 'mr': 'mr_IN', 'ta': 'ta_IN', 'bn': 'bn_IN', 'kn': 'kn_IN', 'ml': 'ml_IN'}
SEG = re.compile(r'<(span|p|li|tspan|ul)\b([^>]*?)\bclass="([^"]*?)\bhi\b([^"]*)"([^>]*)>(.*?)</\1>', re.S)


def parts(page):
    s = open('hi/%s.html' % page, encoding='utf-8').read()
    b0, f0 = s.index('<body'), s.index('<footer')
    return s, s[:b0], s[b0:f0], s[f0:]


def body_pieces(body):
    """Text pieces of the body, skipping the menu bar (it comes from the language's own pages)."""
    m = re.search(r'<div class="bar">.*?(?=<main)', body, re.S)
    a, b = (m.start(), m.end()) if m else (0, 0)
    out = []
    for x in SEG.finditer(body):
        if a <= x.start() < b:
            continue
        if x.group(1) in ('span', 'p', 'li', 'tspan') and '<' + x.group(1) in x.group(6):
            raise SystemExit('nested <%s> inside a Hindi piece: %s' % (x.group(1), x.group(6)[:120]))
        out.append(x)
    return out


def script_strings(tail):
    """Hindi strings inside the page's own scripts after the footer (shared scripts are files, not inline)."""
    found = []
    for sc in re.findall(r'<script>(.*?)</script>', tail, re.S):
        for q in re.findall(r"'((?:[^'\\]|\\.)*[\u0900-\u097F][^'\\]*(?:\\.[^'\\]*)*)'|\"((?:[^\"\\]|\\.)*[\u0900-\u097F][^\"\\]*)\"", sc):
            t = q[0] or q[1]
            if t not in found:
                found.append(t)
    return found


def extract(page, lang=None):
    """With a language, pieces that already have a translation on the site are shown as "= ..." (write None for them)."""
    known = harvest(lang) if lang else {}
    s, head, body, tail = parts(page)
    print('TITLE:', H.unescape(re.search(r'<title>(.*?)</title>', head).group(1)))
    print('DESC:', H.unescape(re.search(r'<meta name="description" content="([^"]*)"', head).group(1)))
    for i, m in enumerate(body_pieces(body)):
        h = m.group(6)
        t = COMMON.get(h, {}).get(lang) or known.get(h) if lang else None
        print(i, '= ' + t if t else h)
    js = script_strings(tail)
    if js:
        print('JS:')
        for t in js:
            print('  ', t)


# lines that recur on the small prayer pages
COMMON = {
    'पूरे प्रसंग में पढ़ें →': {'gu': 'પૂરા સંદર્ભમાં વાંચો →', 'te': 'పూర్తి సందర్భంలో చదవండి →', 'mr': 'संपूर्ण संदर्भात वाचा →',
                              'ta': 'முழுச் சூழலில் படியுங்கள் →', 'bn': 'পুরো প্রসঙ্গে পড়ুন →', 'kn': 'ಪೂರ್ಣ ಸಂದರ್ಭದಲ್ಲಿ ಓದಿ →',
                              'ml': 'പൂർണ്ണ സന്ദർഭത്തിൽ വായിക്കൂ →'},
}


def load(page, lang):
    p = os.path.join(ROOT, 'tools', 'pages', page, lang + '.py')
    spec = importlib.util.spec_from_file_location('%s_%s' % (page, lang), p)
    d = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(d)
    if hasattr(d, 'FROM') and not hasattr(d, 'S'):
        derive(page, lang, d)
    elif hasattr(d, 'S') and None in d.S:
        # None = "already translated elsewhere on the site": take it from pages that exist in Hindi and this language
        known = harvest(lang)
        pieces = body_pieces(parts(page)[2])
        if len(pieces) != len(d.S):
            raise SystemExit('%s/%s: %d pieces on the Hindi page, %d in S' % (page, lang, len(pieces), len(d.S)))
        for i, (m, t) in enumerate(zip(pieces, d.S)):
            if t is None:
                h = m.group(6)
                t = COMMON.get(h, {}).get(lang) or known.get(h)
                if t is None:
                    raise SystemExit('%s/%s: piece %d has no existing translation: %s' % (page, lang, i, h[:100]))
                d.S[i] = t
    if hasattr(d, 'S') and not (hasattr(d, 'TITLE') and hasattr(d, 'DESC')):
        # default: the title and description are pieces of the page itself (as on the Hindi page)
        head = parts(page)[1]
        htitle = H.unescape(re.search(r'<title>(.*?)</title>', head).group(1)).rsplit(' | ', 1)[0]
        hdesc = H.unescape(re.search(r'<meta name="description" content="([^"]*)"', head).group(1))
        texts = [H.unescape(re.sub(r'<[^>]+>', '', m.group(6))) for m in body_pieces(parts(page)[2])]
        for attr, h in (('TITLE', htitle), ('DESC', hdesc)):
            if not hasattr(d, attr):
                if h not in texts:
                    raise SystemExit('%s/%s: set %s (the Hindi one is not a piece of the page)' % (page, lang, attr))
                setattr(d, attr, H.unescape(re.sub(r'<[^>]+>', '', d.S[texts.index(h)])))
    return d


_HARVEST = {}


def lang_pieces(path, lang):
    s = open(path, encoding='utf-8').read()
    b = s[s.index('<body'):s.index('<footer')]
    m = re.search(r'<div class="bar">.*?(?=<main)', b, re.S)
    a, e = (m.start(), m.end()) if m else (0, 0)
    seg = re.compile(r'<(span|p|li|tspan|ul)\b([^>]*?)\bclass="([^"]*?)\b%s\b([^"]*)"([^>]*)>(.*?)</\1>' % lang, re.S)
    return [x.group(6) for x in seg.finditer(b) if not a <= x.start() < e]


def harvest(lang):
    """Hindi text -> this language's text, from every page that exists in both with the same pieces in the same order."""
    if lang not in _HARVEST:
        import collections
        pairs = collections.defaultdict(collections.Counter)
        for f in sorted(os.listdir(lang)):
            if f.endswith('.html') and os.path.exists('hi/' + f):
                h, k = lang_pieces('hi/' + f, 'hi'), lang_pieces('%s/%s' % (lang, f), lang)
                if h and len(h) == len(k):
                    for a, b in zip(h, k):
                        pairs[a][b] += 1
        _HARVEST[lang] = {a: c.most_common(1)[0][0] for a, c in pairs.items()}
    return _HARVEST[lang]


def derive(page, lang, d):
    """A page whose text all appears on another page (a prayer page and its festival page): take the translations from
    that page's content file. FROM = 'festival-page'; MORE = {'Hindi text': 'translation'} for anything not there."""
    src = load(d.FROM, lang)
    known = {}
    for m, t in zip(body_pieces(parts(d.FROM)[2]), src.S):
        known.setdefault(m.group(6), t)
    more = dict(getattr(d, 'MORE', {}))

    def tr(h):
        if h in more:
            return more[h]
        if h in COMMON:
            return COMMON[h][lang]
        if h in known:
            return known[h]
        if h.endswith(' →') and tr(h[:-2]):
            return tr(h[:-2]) + ' →'
        if h.startswith('← ') and tr(h[2:]):
            return '← ' + tr(h[2:])
        m = re.fullmatch(r'(.+) \((.+)\)', h)
        if m and tr(m.group(1)) and tr(m.group(2)):
            return '%s (%s)' % (tr(m.group(1)), tr(m.group(2)))
        for sep in (' · ', ': '):
            if sep in h:
                bits = [tr(x) for x in h.split(sep)]
                if None not in bits:
                    return sep.join(bits)
        return None
    S, missing = [], []
    for m in body_pieces(parts(page)[2]):
        t = tr(m.group(6))
        if t is None:
            missing.append(m.group(6))
        S.append(t)
    if missing:
        raise SystemExit('%s/%s: no translation for:\n  ' % (page, lang) + '\n  '.join(missing))
    d.S = S
    if not hasattr(d, 'TITLE'):
        d.TITLE = S[1]
    if not hasattr(d, 'DESC'):
        d.DESC = S[2]


def site_name(lang):
    sys.path.insert(0, os.path.join(ROOT, 'tools', 'gita'))
    import langs
    return langs.L[lang]['site']


def relink(text, lang):
    def fix(m):
        name = m.group(1)
        return '"/%s/%s' % (lang, name) if os.path.exists('%s/%s' % (lang, name.split('#')[0].split('?')[0])) else '"/' + name
    return re.sub(r'"/hi/([^"]*)', fix, text)


def esc(t):
    return t.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


def build(page, lang):
    d = load(page, lang)
    ref = open('%s/gita.html' % lang, encoding='utf-8').read()
    s, head, body, tail = parts(page)
    bar = re.search(r'<div class="bar">.*?(?=<main)', ref, re.S).group(0)
    body = re.sub(r'<div class="bar">.*?(?=<main)', lambda m: bar, body, count=1, flags=re.S)
    pieces = body_pieces(body)
    if len(pieces) != len(d.S):
        raise SystemExit('%s/%s: %d pieces on the Hindi page, %d in S' % (page, lang, len(pieces), len(d.S)))
    out, pos = [], 0
    for m, t in zip(pieces, d.S):
        tag, pre, c1, c2, post, _ = m.groups()
        out.append(body[pos:m.start()])
        out.append('<%s%sclass="%s%s%s"%s>%s</%s>' % (tag, pre, c1, lang, c2, post, t, tag))
        pos = m.end()
    out.append(body[pos:])
    body = ''.join(out)
    if hasattr(d, 'KICKER'):
        body = re.sub(r'<p class="kicker">[^<]*</p>', lambda m: '<p class="kicker">%s</p>' % d.KICKER, body, count=1)
    for a, b in getattr(d, 'EXTRA', []):
        if a not in body:
            raise SystemExit('%s/%s: EXTRA text not found: %s' % (page, lang, a[:80]))
        body = body.replace(a, b)
    if hasattr(d, 'WA'):
        old = re.search(r'href="https://wa\.me/\?text=([^"]*)"', body)
        camp = re.search(r'utm_campaign%3D([\w-]+)', old.group(1)).group(1)
        url = '%s%s/%s.html?utm_source=whatsapp&utm_medium=share&utm_campaign=%s' % (SITE, lang, page, camp)
        body = body.replace(old.group(0), 'href="https://wa.me/?text=%s"' % urllib.parse.quote(d.WA + '\n' + url, safe=''), 1)
    body = relink(body, lang)
    # footer and the shared scripts after it come from the language's own page; this page's inline scripts stay
    foot = ref[ref.index('<footer'):ref.index('</footer>') + 9]
    rest = tail[tail.index('</footer>') + 9:]
    for a, b in getattr(d, 'JS', {}).items():
        if a not in rest:
            raise SystemExit('%s/%s: JS string not found: %s' % (page, lang, a[:80]))
        rest = rest.replace(a, b)
    if hasattr(d, 'COUNT'):
        cd = re.search(r"<script>\s*\(function\(\)\{var el=document\.getElementById\('dw-count'\).*?</script>", rest, re.S).group(0)
        date = re.search(r'd=new Date\((\d+,\d+,\d+)\)', cd).group(1)
        many, tom, tod = [json.dumps(x, ensure_ascii=False) for x in d.COUNT]
        num = "String(n).replace(/\\d/g,function(x){return '০১২৩৪৫৬৭৮৯'[x]})" if lang == 'bn' else 'n'
        new = ("<script>\n(function(){var el=document.getElementById('dw-count');if(!el)return;\n"
               "function draw(){var now=new Date(),d=new Date(%s),t=new Date(now.getFullYear(),now.getMonth(),now.getDate());\n"
               "var n=Math.round((d-t)/864e5);\nel.textContent=n>1?%s.replace('{n}',%s):n===1?%s:n===0?%s:'';}\ndraw();})();\n</script>"
               ) % (date, many, num, tom, tod)
        rest = rest.replace(cd, new)
    rest = relink(rest.replace('https://sanatan.space/hi/', 'https://sanatan.space/%s/' % lang), lang)
    tail = foot + rest
    css = re.search(r'<style id="%s-css">.*?</style>' % lang, ref, re.S).group(0)
    if '<style id="lang-top-css">' in head:
        head = head.replace('<style id="lang-top-css">', css + '\n<style id="lang-top-css">', 1)
    else:
        head = head.replace('</head>', css + '\n</head>', 1)
    title = '%s | %s' % (d.TITLE, site_name(lang))
    head = re.sub(r'<title>.*?</title>', lambda m: '<title>%s</title>' % esc(title), head, count=1)
    head = re.sub(r'<meta name="description" content="[^"]*">', lambda m: '<meta name="description" content="%s">' % esc(d.DESC), head, count=1)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', lambda m: '<meta property="og:title" content="%s">' % esc(title), head, count=1)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', lambda m: '<meta property="og:description" content="%s">' % esc(d.DESC), head, count=1)
    head = head.replace('/hi/%s.html' % page, '/%s/%s.html' % (lang, page)).replace('hi_IN', LOCALE[lang])
    head = re.sub(r'("inLanguage":\s*)"hi"', r'\1"%s"' % lang, head)
    left = [x for x in re.findall(r'class="[^"]*\bhi\b[^"]*"', body)]
    if left:
        raise SystemExit('%s/%s: Hindi pieces left: %d' % (page, lang, len(left)))
    open('%s/%s.html' % (lang, page), 'w', encoding='utf-8').write(head + body + tail)
    # Devanagari still in the body outside Sanskrit: worth a look (Sanskrit verses are expected)
    plain = re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)\b.*?</\1>', '', body, flags=re.S))
    runs = sorted(set(re.findall(r'[\u0900-\u097F][\u0900-\u097F\s।॥,-]*', plain)))
    print('%s/%s.html written; Devanagari runs left in the body: %d' % (lang, page, len(runs)))
    if '-v' in sys.argv:
        for r in runs:
            print('   ', r.strip()[:100])


def hreflang(page):
    have = [l for l in ORDER if os.path.exists('%s/%s.html' % (l, page))]
    block = '<link rel="alternate" hreflang="en" href="%s%s.html">\n' % (SITE, page)
    block += ''.join('<link rel="alternate" hreflang="%s" href="%s%s/%s.html">\n' % (l, SITE, l, page) for l in have)
    block += '<link rel="alternate" hreflang="x-default" href="%s%s.html">\n' % (SITE, page)
    for path in ['%s.html' % page] + ['%s/%s.html' % (l, page) for l in have]:
        s = open(path, encoding='utf-8').read()
        s2 = re.sub(r'(?:<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n)+', lambda m: block, s, count=1)
        if s2 != s:
            open(path, 'w', encoding='utf-8').write(s2)


def sitemap(page, langs):
    p = 'sitemap.xml'
    s = open(p, encoding='utf-8').read()
    add = ''
    for l in langs:
        u = '%s%s/%s.html' % (SITE, l, page)
        if '<loc>%s</loc>' % u not in s:
            add += '<url><loc>%s</loc></url>\n' % u
    if add:
        s = s.replace('</urlset>', add + '</urlset>')
        open(p, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    cmd, page = sys.argv[1], sys.argv[2]
    if cmd == 'extract':
        extract(page, sys.argv[3] if len(sys.argv) > 3 else None)
    elif cmd == 'build':
        langs = [a for a in sys.argv[3:] if not a.startswith('-')]
        for l in langs:
            build(page, l)
        hreflang(page)
        sitemap(page, langs)
