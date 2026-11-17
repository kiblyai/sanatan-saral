"""Make the sharing pictures in og/ (the image WhatsApp, Facebook and others show for a link).

    python3 tools/og_images.py            # all pictures
    python3 tools/og_images.py gita-7 kids  # only these

Each picture is 1200 x 630: a small line on top, the page's English title, its Hindi title under it, and the site
name. The words come from the pages themselves (the English page's kicker line and h1, and the Hindi page's h1), so a
picture changes when its page's title changes and this is run again. Gita chapters without a Hindi page use the
chapter's Sanskrit name. Long titles are made smaller until everything fits; the tool stops with an error if a
title still does not fit.

The fonts are in tools/og-fonts (Cormorant Garamond, Poppins and Tiro Devanagari Hindi, all SIL Open Font License),
so the pictures look the same wherever this runs. Needs Python Playwright with Chromium.
"""
import base64, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, 'tools', 'og-fonts')

# Gita chapters with no Hindi page yet: the Hindi line is the chapter's Sanskrit name.
GITA_SKT = {7: 'ज्ञानविज्ञानयोग', 8: 'अक्षरब्रह्मयोग', 9: 'राजविद्याराजगुह्ययोग', 10: 'विभूतियोग', 11: 'विश्वरूपदर्शनयोग',
            12: 'भक्तियोग', 13: 'क्षेत्रक्षेत्रज्ञविभागयोग', 14: 'गुणत्रयविभागयोग', 15: 'पुरुषोत्तमयोग', 16: 'दैवासुरसम्पद्विभागयोग',
            17: 'श्रद्धात्रयविभागयोग', 18: 'मोक्षसंन्यासयोग'}


def text(m):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', m.group(1)))).strip() if m else ''


def words(name):
    page = os.path.join(ROOT, name + '.html')
    s = open(page, encoding='utf-8').read()
    head = s[:s.find('<h1')]
    kickers = re.findall(r'<p class="kicker"[^>]*>(.*?)</p>', head, re.S)
    eyebrow = text(re.match(r'(.*)', kickers[-1], re.S)) if kickers else ''
    title = text(re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S))
    hi = ''
    hp = os.path.join(ROOT, 'hi', name + '.html')
    if os.path.exists(hp):
        hi = text(re.search(r'<h1[^>]*>(.*?)</h1>', open(hp, encoding='utf-8').read(), re.S))
    m = re.fullmatch(r'gita-(\d+)', name)
    if m and not hi and int(m.group(1)) in GITA_SKT:
        hi = 'गीता अध्याय %s: %s' % (m.group(1), GITA_SKT[int(m.group(1))])
    if not eyebrow or not title:
        raise SystemExit('%s: no kicker line or heading found' % page)
    return eyebrow, title, hi


def font_face(family, file, weight, rng):
    data = base64.b64encode(open(os.path.join(FONTS, file), 'rb').read()).decode()
    return ("@font-face{font-family:'%s';font-weight:%d;src:url(data:font/woff2;base64,%s) format('woff2');unicode-range:%s}"
            % (family, weight, data, rng))


LATIN = 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215'
LATIN_EXT = 'U+0100-024F,U+1E00-1EFF'
DEVA = 'U+0900-097F,U+1CD0-1CF9,U+200C-200D,U+20A8,U+20B9,U+25CC,U+A830-A839,U+A8E0-A8FF'
CSS = ''.join([
    font_face('Cormorant', 'cormorant-garamond-latin-600-normal.woff2', 600, LATIN),
    font_face('Cormorant', 'cormorant-garamond-latin-ext-600-normal.woff2', 600, LATIN_EXT),
    font_face('Poppins', 'poppins-latin-400-normal.woff2', 400, LATIN),
    font_face('Poppins', 'poppins-latin-500-normal.woff2', 500, LATIN),
    font_face('Poppins', 'poppins-latin-ext-500-normal.woff2', 500, LATIN_EXT),
    font_face('Poppins', 'poppins-devanagari-400-normal.woff2', 400, DEVA),
    font_face('Poppins', 'poppins-devanagari-500-normal.woff2', 500, DEVA),
    font_face('Tiro', 'tiro-devanagari-hindi-devanagari-400-normal.woff2', 400, DEVA),
    font_face('Tiro', 'tiro-devanagari-hindi-latin-400-normal.woff2', 400, LATIN),
])

PAGE = """<!doctype html><meta charset="utf-8"><style>%s
*{margin:0;box-sizing:border-box}
html,body{width:1200px;height:630px;overflow:hidden}
body{position:relative;font-family:Poppins,sans-serif;color:#20363A;
 background:radial-gradient(520px 360px at 1010px 560px,#e2d6c2 0,rgba(226,214,194,0) 100%%),
 linear-gradient(115deg,#d8e8e2 0,#e2e6ec 40%%,#e8e5ec 70%%,#eee6d8 100%%)}
.om{position:absolute;left:816px;top:122px;width:296px;height:296px;border:3px solid #ab9f87;border-radius:50%%;
 display:flex;align-items:center;justify-content:center;font:400 150px/1 Tiro,serif;color:#7E6A3A;padding-top:22px}
.box{position:absolute;left:86px;top:96px;width:690px;height:400px;display:flex;flex-direction:column}
.eb{font:500 24px/1.3 Poppins,sans-serif;letter-spacing:.09em;text-transform:uppercase;color:#83672C;margin-bottom:26px;
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
h1{font:600 var(--t,64px)/1.06 Cormorant,serif;letter-spacing:-.005em}
.hi{font:400 var(--h,32px)/1.4 Tiro,serif;color:#3C6C72;margin-top:18px}
.ft{position:absolute;left:86px;top:524px;font:400 26px/1.3 Poppins,sans-serif;color:#566B6D;white-space:nowrap}
.ft b{font-weight:500;color:#20363A}
</style><div class="om">ॐ</div>
<div class="box" id="box"><div class="eb">%s</div><h1>%s</h1>%s</div>
<div class="ft"><b>Sanatan Dharma Saral</b> · सनातन धर्म सरल · sanatan.space</div>"""

FIT = """() => { const b = document.getElementById('box'), h = document.querySelector('h1'), hi = document.querySelector('.hi');
  let t = 64; const room = () => b.scrollHeight <= b.clientHeight && h.scrollWidth <= h.clientWidth;
  while (!room() && t > 40) { t -= 2; b.style.setProperty('--t', t + 'px'); b.style.setProperty('--h', Math.max(26, Math.round(t / 2)) + 'px'); }
  return {t, fits: room(), lines: Math.round(h.getBoundingClientRect().height / (t * 1.06))}; }"""


def main(names):
    from playwright.sync_api import sync_playwright
    os.chdir(ROOT)
    if not names:
        names = sorted(f[:-4] for f in os.listdir('og') if f.endswith('.png') and os.path.exists(f[:-4] + '.html'))
    esc = html.escape
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1200, 'height': 630}, device_scale_factor=1)
        bad = []
        for n in names:
            eb, title, hi = words(n)
            pg.set_content(PAGE % (CSS, esc(eb), esc(title), '<div class="hi">%s</div>' % esc(hi) if hi else ''))
            pg.evaluate('document.fonts.ready')
            r = pg.evaluate(FIT)
            if not r['fits']:
                bad.append(n)
            pg.screenshot(path='og/%s.png' % n)
            print('%-18s %2dpx %s | %s | %s' % (n, r['t'], '' if r['fits'] else 'DOES NOT FIT', title, hi))
        b.close()
    if bad:
        raise SystemExit('too long for the picture: ' + ' '.join(bad))


if __name__ == '__main__':
    main(sys.argv[1:])
