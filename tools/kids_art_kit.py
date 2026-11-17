"""Drawing kit for the kids' story pictures: small flat characters with a navy outline, drawn as SVG.

Every function returns SVG markup. Figures are drawn with their feet at (0, 0) and are about 54 units tall
at scale 1; `at(x, y, s, flip, inner)` places them in a 320 x 150 scene.
"""
import math

INK = '#1a1446'
SK = '#F6C9A0'      # skin
SKD = '#E2A878'     # darker skin
BLUE = '#6EC6FF'    # Krishna, Vishnu
PALE = '#CFE3FF'    # Shiva
GREEN = '#86D9B4'   # Rama
YAMA = '#8FC4A8'
PINK = '#F8B9C6'    # Ganesha
GOLD = '#FFD23F'
WHITE = '#FFFFFF'
HAIR = '#2B1B4D'
GREY = '#EDEAF4'    # white hair
BROWN = '#D9955A'   # vanaras


def O(w=2.5):
    return 'stroke="%s" stroke-width="%g" stroke-linecap="round" stroke-linejoin="round"' % (INK, w)


def at(x, y, s=1, flip=False, inner=''):
    return '<g transform="translate(%g %g) scale(%g %g)">%s</g>' % (x, y, -s if flip else s, s, inner)


def limb(d, col, w=3.5):
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%g" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="%s" fill="none" stroke="%s" stroke-width="%g" stroke-linecap="round" stroke-linejoin="round"/>'
            % (d, INK, w + 4.5, d, col, w))


def line(d, col=INK, w=2.5, dash=None):
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%g" stroke-linecap="round" stroke-linejoin="round"%s/>' % (
        d, col, w, ' stroke-dasharray="%s"' % dash if dash else '')


def shape(d, fill, w=2.5):
    return '<path d="%s" fill="%s" %s/>' % (d, fill, O(w))


def circ(x, y, r, fill, w=2.5):
    return '<circle cx="%g" cy="%g" r="%g" fill="%s" %s/>' % (x, y, r, fill, O(w))


def dot(x, y, r=1.8, fill=INK):
    return '<circle cx="%g" cy="%g" r="%g" fill="%s"/>' % (x, y, r, fill)


def ell(x, y, rx, ry, fill, w=2.5):
    return '<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="%s" %s/>' % (x, y, rx, ry, fill, O(w))


# ---------------------------------------------------------------- faces and heads

def features(face='smile', cy=-40):
    e, m = cy - 2, cy + 4
    eyes = dot(-5, e) + dot(5, e)
    if face in ('calm', 'sleep'):
        eyes = line('M-8 %g q3 3 6 0 M2 %g q3 3 6 0' % (e, e), w=2)
    if face == 'happy':
        eyes = line('M-8 %g q3 -3 6 0 M2 %g q3 -3 6 0' % (e + 1, e + 1), w=2)
    brows = ''
    if face == 'angry':
        brows = line('M-9 %g l7 3 M9 %g l-7 3' % (e - 6, e - 6), w=2)
    if face in ('sad', 'worried'):
        brows = line('M-9 %g l6 -3 M9 %g l-6 -3' % (e - 3, e - 3), w=2)
    mouth = line('M-4 %g q4 4 8 0' % m, w=2)
    if face in ('angry', 'sad'):
        mouth = line('M-4 %g q4 -4 8 0' % (m + 3), w=2)
    if face in ('worried', 'sleep'):
        mouth = line('M-3 %g h6' % (m + 2), w=2)
    if face == 'oh':
        mouth = '<circle cx="0" cy="%g" r="2.6" fill="%s"/>' % (m + 2, INK)
    if face == 'happy':
        mouth = '<path d="M-5 %g q5 7 10 0 z" fill="#fff" %s/>' % (m - 1, O(2))
    return eyes + brows + mouth


def human_head(skin=SK, face='smile', hair=HAIR, style='short', crown=None, beard=None, must=False, bindi=False,
               tilak=False, halo=False, cy=-40):
    """Returns (behind, front): parts drawn behind the body and in front of it."""
    back, f = '', ''
    if halo:
        back += '<circle cx="0" cy="%g" r="21" fill="#FFF3B0" opacity=".85"/>' % cy
    if style == 'long':
        back += shape('M-16 %g v-20 a16 16 0 0 1 32 0 v20 q-16 6 -32 0z' % (cy + 18), hair)
    if style in ('bun', 'sage', 'jata'):
        back += circ(0, cy - 17, 6, hair)
    if style == 'jata':
        back += shape('M-15 %g q-6 14 -2 24 q5 -3 5 -12 z M15 %g q6 14 2 24 q-5 -3 -5 -12 z' % (cy - 4, cy - 4), hair)
    if style == 'tuft':
        back += line('M3 %g q7 -9 10 -2' % (cy - 12), hair, 3.5)
    f += circ(0, cy, 13, skin)
    if style in ('short', 'long', 'bun', 'sage', 'jata'):
        f += shape('M-13 %g a13 13 0 0 1 26 0 q-3 -8 -13 -8 q-10 0 -13 8z' % (cy - 2), hair)
    if crown == 'crown':
        f += shape('M-10 %g l2 -9 5 6 3 -8 3 8 5 -6 2 9 z' % (cy - 10), GOLD)
    if crown == 'tall':
        f += shape('M-10 %g q3 -10 10 -22 q7 12 10 22 z' % (cy - 9), GOLD) + dot(0, cy - 17, 2.2, '#E0245E')
    if crown == 'band':
        f += line('M-13 %g q13 -6 26 0' % (cy - 6), '#E0245E', 3)
    if crown in ('feather', 'kfeather'):
        if crown == 'kfeather':
            f += shape('M-10 %g l2 -8 5 5 3 -7 3 7 5 -5 2 8 z' % (cy - 10), GOLD)
        f += shape('M3 %g q2 -15 13 -13 q2 9 -9 14 z' % (cy - 11), '#2E9E4F') + dot(10, cy - 19, 2.5, '#3B6BFF')
    if crown == 'moon':
        f += line('M8 %g q7 -2 7 4' % (cy - 19), '#9EDBFF', 3)
    if beard:
        f += shape('M-11 %g q2 20 11 22 q9 -2 11 -22 q-11 7 -22 0z' % (cy + 3), beard)
    f += features(face, cy)
    if must:
        f += line('M-8 %g q4 -4 8 0 q4 -4 8 0' % (cy + 3), HAIR, 2.5)
    if bindi:
        f += dot(0, cy - 7, 1.8, '#E0245E')
    if tilak:
        f += line('M0 %g v-5' % (cy - 5), '#E0245E', 2)
    return back, f


def ganesha_head(face='smile', tusk='both', crown=True, cy=-40):
    f = ell(-17, cy - 2, 9, 12, '#F3A3B5') + ell(17, cy - 2, 9, 12, '#F3A3B5') + circ(0, cy, 14, PINK)
    if crown:
        f += shape('M-9 %g l2 -9 5 6 2 -8 2 8 5 -6 2 9 z' % (cy - 11), GOLD)
    e = cy - 3
    f += (line('M-8 %g q3 -3 6 0 M2 %g q3 -3 6 0' % (e, e), w=2) if face == 'happy' else dot(-5, e) + dot(5, e))
    t = 'M0 %g c0 10 -2 15 -8 16 c-5 0 -5 -5 -1 -6' % (cy + 3)
    f += limb(t, PINK, 4)
    t = 'l2.5 .8' if tusk == 'broken' else 'l6 2'
    f += '<path d="M7 %g %s" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round"/><path d="M7 %g %s" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>' % (cy + 6, t, INK, cy + 6, t)
    return '', f


def monkey_head(face='smile', crown=False, col=BROWN, cy=-40):
    f = circ(-13, cy - 3, 5, col) + circ(13, cy - 3, 5, col) + circ(0, cy, 13, col) + ell(0, cy + 5, 8.5, 6.5, '#F7D9B5')
    if crown:
        f += shape('M-8 %g l2 -8 4 5 2 -7 2 7 4 -5 2 8 z' % (cy - 10), GOLD)
    f += dot(-5, cy - 3) + dot(5, cy - 3)
    f += (line('M-3 %g q3 3 6 0' % (cy + 6), w=2) if face != 'oh' else dot(0, cy + 7, 2.4))
    return '', f


def bear_head(cy=-40):
    c = '#8B5E3C'
    f = circ(-10, cy - 11, 4.5, c) + circ(10, cy - 11, 4.5, c) + circ(0, cy, 13, c) + ell(0, cy + 5, 7.5, 6, '#E3C29B')
    f += dot(-5, cy - 3) + dot(5, cy - 3) + dot(0, cy + 3, 2.2) + line('M-3 %g q3 3 6 0' % (cy + 7), w=2)
    return '', f


def lion_head(cy=-40):
    pts = []
    for i in range(24):
        a = i * math.pi / 12
        r = 21 if i % 2 == 0 else 16.5
        pts.append('%.1f %.1f' % (r * math.cos(a), cy + r * math.sin(a)))
    f = shape('M' + ' L'.join(pts) + ' z', '#F29E38')
    f += circ(-9, cy - 10, 4, '#FFD27A') + circ(9, cy - 10, 4, '#FFD27A') + circ(0, cy, 12.5, '#FFD27A')
    f += shape('M-9 %g q3 -10 9 -20 q6 10 9 20 z' % (cy - 9), GOLD)
    f += dot(-5, cy - 2) + dot(5, cy - 2) + line('M-9 %g l6 2 M9 %g l-6 2' % (cy - 7, cy - 7), w=2)
    f += '<path d="M-3 %g h6 l-3 3.5 z" fill="%s"/>' % (cy + 2, INK) + line('M0 %g v2 q-3 3 -6 1 M0 %g q3 3 6 1' % (cy + 5, cy + 7), w=2)
    return '', f


# ---------------------------------------------------------------- bodies

ARMS = {
    'down': 'M10 -20 q7 8 4 17', 'up': 'M10 -21 q11 -8 12 -26', 'out': 'M10 -20 q10 1 19 -5', 'fwd': 'M9 -17 h17',
    'hold': 'M10 -20 q9 5 13 -1', 'hip': 'M10 -20 q10 6 2 12', 'point': 'M10 -20 l20 -8', 'cheek': 'M10 -20 q12 -2 5 -13',
    'bless': 'M10 -20 q10 -2 13 -12', 'give': 'M9 -18 q10 4 18 0', 'none': '',
}


def body(cloth, sit=False, wide=0):
    w = 12 + wide
    s = shape('M%g 0 v-18 a%g %g 0 0 1 %g 0 v18z' % (-w, w, w, 2 * w), cloth)
    if sit:
        s += ell(0, -4, 19 + wide, 7, cloth)
    return s


def person(x, y, s=1, flip=False, skin=SK, cloth=GOLD, arms=('down', 'down'), sit=False, head=None, sash=None,
           behind='', front='', top=None, wide=0, **hk):
    """A figure. arms=(left, right) pose names or raw path data; 'namaste' for folded hands.
    head: (behind, front) from a head function; otherwise a human head from **hk.
    top: colour of a bare upper body (skin) above a dhoti."""
    hb, hf = head if head else human_head(skin=skin, **hk)
    g = hb + behind + body(cloth, sit, wide)
    if top:
        w = 12 + wide
        g += shape('M%g -12 v-6 a%g %g 0 0 1 %g 0 v6z' % (-w, w, w, 2 * w), top)
    if sash:
        g += line('M-10 -25 L10 -5', sash, 3.5)
    if arms == 'namaste':
        g += limb('M10 -20 q4 10 -8 6', skin) + at(0, 0, 1, True, limb('M10 -20 q4 10 -8 6', skin)) + ell(0, -14, 3.2, 4.2, skin, 2)
    else:
        l, r = arms
        if l and l != 'none':
            g += at(0, 0, 1, True, limb(ARMS.get(l, l), skin))
        if r and r != 'none':
            g += limb(ARMS.get(r, r), skin)
    g += hf + front
    return at(x, y, s, flip, g)


# ---------------------------------------------------------------- named characters

def shiva(x, y, s=1, **k):
    k.setdefault('face', 'smile')
    spots = dot(-5, -6, 1.6, '#8A4B1E') + dot(4, -9, 1.6, '#8A4B1E') + dot(6, -3, 1.6, '#8A4B1E')
    return person(x, y, s, skin=PALE, cloth='#E79A4E', top=PALE, hair='#3B2A5A', style='jata', crown='moon',
                  front=k.pop('front', '') + spots, **k)


def parvati(x, y, s=1, **k):
    return person(x, y, s, cloth='#FF7FA8', style='long', crown='crown', bindi=True, **k)


def ganesha(x, y, s=1, face='smile', tusk='both', crown=True, **k):
    belly = ell(0, -11, 9, 7, '#FBD0D9', 2)
    return person(x, y, s, skin=PINK, cloth='#FF8A3D', top=PINK, head=ganesha_head(face, tusk, crown),
                  front=belly + k.pop('front', ''), wide=2, **k)


def krishna(x, y, s=1, king=False, **k):
    return person(x, y, s, skin=BLUE, cloth=GOLD, top=BLUE, crown='kfeather' if king else 'feather',
                  sash='#E86A2E' if king else None, **k)


def vishnu(x, y, s=1, **k):
    return person(x, y, s, skin=BLUE, cloth=GOLD, top=BLUE, crown='tall', halo=True, sash='#E0245E', **k)


def rama(x, y, s=1, **k):
    return person(x, y, s, skin=GREEN, cloth='#FF9F45', top=GREEN, style='bun', tilak=True, **k)


def yama(x, y, s=1, **k):
    return person(x, y, s, skin=YAMA, cloth='#B8405E', crown='crown', must=True, sash=GOLD, wide=2, **k)


def sage(x, y, s=1, cloth='#FF9F45', **k):
    k.setdefault('style', 'sage')
    k.setdefault('hair', GREY)
    k.setdefault('beard', GREY)
    return person(x, y, s, cloth=cloth, **k)


def king(x, y, s=1, cloth='#C0392B', **k):
    k.setdefault('must', True)
    return person(x, y, s, cloth=cloth, crown='crown', sash=GOLD, wide=2, **k)


def queen(x, y, s=1, cloth='#9B5DE5', **k):
    return person(x, y, s, cloth=cloth, style='long', crown='crown', bindi=True, **k)


def boy(x, y, s=.8, cloth=GOLD, **k):
    k.setdefault('style', 'short')
    return person(x, y, s, cloth=cloth, **k)


def vanara(x, y, s=1, cloth='#E86A2E', face='smile', crown=False, tail=True, **k):
    t = limb('M-10 -5 q-22 6 -24 -14 q0 -8 6 -8', '#C97B3A') if tail else ''
    return person(x, y, s, skin=BROWN, cloth=cloth, top=BROWN, head=monkey_head(face, crown), behind=t, **k)


def bear(x, y, s=1, **k):
    return person(x, y, s, skin='#8B5E3C', cloth='#7A4F30', head=bear_head(), wide=2, **k)


def narasimha(x, y, s=1, **k):
    return person(x, y, s, skin='#FFD27A', cloth=GOLD, top=BLUE, head=lion_head(), sash='#E0245E', wide=2, **k)


# ---------------------------------------------------------------- animals

def mouse(x, y, s=1, flip=False):
    g = ell(0, -6, 10, 6, '#B9B4C8') + circ(-8, -11, 4, '#B9B4C8') + dot(-9, -6, 1.3) + line('M10 -6 q8 -2 9 -8')
    return at(x, y, s, flip, g)


def peacock(x, y, s=1, flip=False):
    g = ''
    for dy, c in ((-8, '#2E9E4F'), (0, '#3FB56B'), (8, '#2E9E4F')):
        g += shape('M-10 -10 q-30 %g -52 %g q24 %g 52 6 z' % (dy - 6, dy, 8 - dy), c)
        g += dot(-52, dy - 10 + 10, 3, '#3B6BFF')
    g += ell(0, -12, 17, 11, '#2F7FD8') + limb('M12 -18 q8 -8 6 -20', '#2F7FD8', 5) + circ(19, -40, 6, '#2F7FD8')
    g += line('M19 -46 v-6 M15 -45 l-3 -5 M23 -45 l3 -5', '#2E9E4F', 2) + dot(21, -41, 1.3) + shape('M24 -40 l6 2 -6 2 z', GOLD, 1.5)
    g += shape('M-6 -14 q8 -10 14 0 q-7 6 -14 0z', '#5BA8F5', 2)
    return at(x, y, s, flip, g)


def elephant(x, y, s=1, flip=False, bow=False):
    c = '#C9CEDA'
    g = shape('M-34 -2 v-22 a16 16 0 0 1 16 -16 h22 a16 16 0 0 1 16 16 v22 h-12 v-10 h-22 v10 z', c)
    hy = -26 if bow else -34
    g += ell(14, hy, 9, 13, '#B4BACB') + circ(28, hy, 15, c)
    g += limb('M36 %g q10 6 8 20 q-1 6 -7 5' % (hy + 6), c, 6)
    g += dot(31, hy - 3) + line('M26 %g q3 3 6 0' % (hy + 5), w=2)
    g += line('M-34 -22 q-6 4 -5 12')
    return at(x, y, s, flip, g)


def cow(x, y, s=1, flip=False, col='#fff', thin=False):
    h = 11 if thin else 15
    g = '<rect x="-13" y="%g" width="26" height="%g" rx="%g" fill="%s" %s/>' % (-7 - h, h, h / 2, col, O())
    g += circ(-15, -7 - h, 6, col) + line('M-19 %g l-3 -4 M-12 %g l2 -4' % (-12 - h, -12 - h)) + dot(-17, -8 - h, 1.2)
    g += line('M-8 -7 v7 M8 -7 v7') + dot(4, -7 - h / 2, 3, '#C9B8A8') + line('M13 %g q5 2 4 8' % (-5 - h), w=2)
    return at(x, y, s, flip, g)


def buffalo(x, y, s=1, flip=False):
    c = '#5A5470'
    g = '<rect x="-17" y="-26" width="34" height="19" rx="9" fill="%s" %s/>' % (c, O())
    g += circ(-19, -24, 8, c) + line('M-25 -30 q-8 -4 -6 -12 M-13 -30 q8 -4 6 -12', '#EDEAF4', 3.5) + dot(-22, -25, 1.4, '#fff')
    g += line('M-10 -7 v7 M10 -7 v7', c, 4) + line('M-10 -7 v7 M10 -7 v7', INK, 2.5)
    return at(x, y, s, flip, g)


def squirrel(x, y, s=1, flip=False, stripes=False):
    c = '#C98A4B'
    g = shape('M10 -4 q20 -2 16 -22 q-3 -12 -14 -8 q8 4 4 14 q-2 8 -10 10 z', '#E0A868')
    g += ell(0, -9, 12, 8, c) + circ(-11, -16, 7, c) + shape('M-13 -22 l1 -6 5 4 z', c) + dot(-13, -17, 1.5)
    g += line('M-17 -14 l-3 1', w=2) + line('M-6 -2 v3 M5 -2 v3')
    if stripes:
        g += line('M-6 -15 q8 -3 15 2 M-7 -12 q9 -3 17 2 M-7 -9 q9 -2 17 3', '#5B3A1A', 1.8)
    return at(x, y, s, flip, g)


# ---------------------------------------------------------------- props and scenery

def sky(c, ground=None, gy=124, curve=6):
    s = '<rect width="320" height="150" fill="%s"/>' % c
    if ground:
        s += '<path d="M0 %g q80 %g 160 0 t160 0 v60 h-320z" fill="%s"/>' % (gy, -curve, ground)
    return s


def cloud(x, y, s=1, fill='#fff', outline=True):
    d = 'M-24 6 q-10 -2 -6 -10 q2 -8 12 -6 q6 -10 18 -4 q12 -2 12 8 q8 2 4 9 q-2 3 -8 3 z'
    return at(x, y, s, False, '<path d="%s" fill="%s" %s/>' % (d, fill, O() if outline else ''))


def tree(x, y, s=1, leaf='#58C472', trunk='#9A6B43'):
    g = '<rect x="-4" y="-30" width="8" height="30" rx="2" fill="%s" %s/>' % (trunk, O())
    g += circ(-11, -36, 12, leaf) + circ(11, -36, 12, leaf) + circ(0, -48, 14, leaf)
    g += '<circle cx="0" cy="-38" r="11" fill="%s"/>' % leaf
    return at(x, y, s, False, g)


def bush(x, y, s=1, c='#58C472'):
    return at(x, y, s, False, shape('M-22 0 q-4 -14 8 -14 q4 -10 14 -4 q12 -4 12 8 q8 2 4 10 z', c))


def hill(x, y, w, h, c='#6BCB77'):
    return shape('M%g %g q%g %g %g 0 z' % (x - w / 2, y, w / 2, -2 * h, w), c)


def peaks(c='#E8F1FF', y=124):
    return (shape('M-10 %g L50 40 L96 %g z' % (y, y), c) + shape('M70 %g L150 22 L236 %g z' % (y, y), c)
            + shape('M200 %g L270 46 L334 %g z' % (y, y), c)
            + '<path d="M150 22 l-18 24 9 -4 9 8 9 -8 9 5 z" fill="#fff"/>')


def star(x, y, r=7, fill=GOLD, w=2):
    p = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * .45
        p.append('%.1f %.1f' % (x + rr * math.cos(a), y + rr * math.sin(a)))
    return '<path d="M%s z" fill="%s" %s/>' % (' L'.join(p), fill, O(w))


def sparkle(x, y, r=5, c=GOLD):
    return line('M%g %g v%g M%g %g h%g' % (x, y - r, 2 * r, x - r, y, 2 * r), c, 2.5)


def sun(x, y, r=26, face='smile', c='#FFB300', rays='#FF8A3D'):
    g = ''
    for i in range(12):
        a = i * math.pi / 6
        g += line('M%.1f %.1f L%.1f %.1f' % (x + (r + 6) * math.cos(a), y + (r + 6) * math.sin(a), x + (r + 15) * math.cos(a), y + (r + 15) * math.sin(a)), rays, 4)
    g += circ(x, y, r, c)
    if face:
        g += at(x, y + 40 - 2, 1, False, features(face)) + dot(x - 14, y + 6, 4, '#FF8A3D') + dot(x + 14, y + 6, 4, '#FF8A3D')
    return g


def moon(x, y, r=10):
    return '<path d="M%g %g a%g %g 0 1 0 %g %g a%g %g 0 0 1 %g %g z" fill="#FFF3B0" %s/>' % (
        x, y - r, r, r, r * .9, r * 1.6, r * .8, r * .8, -r * .9, -r * 1.6, O(2))


def mango(x, y, s=1):
    return at(x, y, s, False, shape('M0 -8 q9 -2 9 6 q0 9 -9 9 q-9 0 -9 -8 q1 -7 9 -7z', '#FFB300') + line('M0 -8 q2 -6 7 -6', '#2E9E4F', 2.5))


def throne(x, y, s=1, c='#B8405E'):
    g = '<rect x="-20" y="-58" width="40" height="58" rx="8" fill="%s" %s/>' % (c, O())
    g += circ(-20, -58, 4, GOLD) + circ(20, -58, 4, GOLD) + '<rect x="-24" y="-8" width="48" height="8" rx="3" fill="%s" %s/>' % (GOLD, O())
    return at(x, y, s, False, g)


def pillar(x, y, h=96, w=22, c='#E9DCC3', crack=False):
    g = '<rect x="%g" y="%g" width="%g" height="%g" fill="%s" %s/>' % (x - w / 2, y - h, w, h, c, O())
    g += '<rect x="%g" y="%g" width="%g" height="8" rx="2" fill="%s" %s/>' % (x - w / 2 - 5, y - h - 6, w + 10, c, O())
    g += '<rect x="%g" y="%g" width="%g" height="8" rx="2" fill="%s" %s/>' % (x - w / 2 - 5, y - 8, w + 10, c, O())
    if crack:
        g += line('M%g %g l-5 12 6 10 -6 12 5 12 -4 12' % (x, y - h + 6), w=2)
    return g


def flame(x, y, s=1):
    return at(x, y, s, False, shape('M0 0 q-10 -6 -6 -16 q2 4 5 4 q-2 -10 4 -16 q8 10 6 20 q-2 8 -9 8z', '#FF8A3D')
              + '<path d="M1 -2 q-4 -4 -1 -9 q4 4 4 7 q-1 2 -3 2z" fill="#FFD23F"/>')


def pot(x, y, s=1, c='#C97B3A'):
    return at(x, y, s, False, shape('M-7 -14 h14 q-3 3 2 6 q5 4 0 9 q-3 3 -9 3 q-6 0 -9 -3 q-5 -5 0 -9 q5 -3 2 -6z', c))


def bow(x, y, s=1, rot=0, arrow=True):
    g = line('M0 -20 q16 20 0 40', '#8A4B1E', 3) + line('M0 -20 v40', '#555', 1.2)
    if arrow:
        g += line('M-6 0 h26', '#8A4B1E', 2) + '<path d="M20 -3 l6 3 -6 3 z" fill="%s"/>' % INK
    return '<g transform="translate(%g %g) rotate(%g) scale(%g)">%s</g>' % (x, y, rot, s, g)


def rock(x, y, w=18, c='#B7B2C6'):
    return shape('M%g %g q0 -%g %g -%g q%g 0 %g %g z' % (x - w / 2, y, w * .7, w / 2, w * .7, w / 2, w / 2, w * .7), c)


def waves(y, c='#fff', n=7, x0=0, x1=320):
    step = (x1 - x0) / n
    d = 'M%g %g ' % (x0, y) + ' '.join('q%g -5 %g 0' % (step / 2, step) for _ in range(n))
    return line(d, c, 2.5)


def linga(x, y, s=1):
    g = '<rect x="-22" y="-12" width="44" height="12" rx="5" fill="#8C93A6" %s/>' % O()
    g += shape('M-11 -12 v-22 a11 11 0 0 1 22 0 v22 z', '#5B6170')
    g += line('M-7 -30 h14 M-7 -26 h14 M-7 -22 h14', '#EDEAF4', 2) + dot(0, -26, 1.8, '#E0245E')
    return at(x, y, s, False, g)


def hut(x, y, s=1):
    g = '<rect x="-20" y="-24" width="40" height="24" fill="#E9C99A" %s/>' % O() + shape('M-28 -24 L0 -48 L28 -24 z', '#C98A4B')
    g += '<rect x="-6" y="-16" width="12" height="16" rx="2" fill="#8A4B1E" %s/>' % O()
    return at(x, y, s, False, g)


def palace(x, y, s=1, c='#FFE8A3'):
    g = '<rect x="-46" y="-56" width="92" height="56" fill="%s" %s/>' % (c, O())
    g += shape('M-46 -56 q10 -18 20 0 z', GOLD) + shape('M-10 -56 q10 -22 20 0 z', GOLD) + shape('M26 -56 q10 -18 20 0 z', GOLD)
    g += shape('M-12 0 v-22 a12 12 0 0 1 24 0 v22 z', '#B8405E')
    g += '<rect x="-36" y="-40" width="10" height="14" rx="5" fill="#fff" %s/><rect x="26" y="-40" width="10" height="14" rx="5" fill="#fff" %s/>' % (O(2), O(2))
    return at(x, y, s, False, g)


def bubble(x, y, r=15, inner=''):
    return circ(x, y, r, '#fff', 2) + circ(x - r * .8, y + r * 1.05, 3.5, '#fff', 2) + circ(x - r * 1.25, y + r * 1.5, 2, '#fff', 2) + inner


def rain(n=18, c='#5AA9E6', seed=3, heavy=False):
    import random
    r = random.Random(seed)
    g = ''
    for _ in range(n):
        x, y = r.randint(6, 314), r.randint(4, 110)
        g += line('M%d %d l-4 %d' % (x, y, 12 if heavy else 9), c, 2.5)
    return g


def stars(n=14, seed=1, ymax=70):
    import random
    r = random.Random(seed)
    return ''.join(dot(r.randint(8, 312), r.randint(6, ymax), r.choice([1.2, 1.6, 2]), '#fff') for _ in range(n))


def bundle(x, y, s=1):
    return at(x, y, s, False, circ(0, -6, 6.5, '#E9DCC3') + line('M-3 -12 l3 -4 3 4', w=2))


def garland(x0, y0, x1, y1, sag=14, n=9):
    g = ''
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t + sag * 4 * t * (1 - t)
        g += dot(x, y, 2.6, '#FF8A3D' if i % 2 else '#FFD23F')
    return g


def target(x, y, r=10):
    return circ(x, y, r, '#fff', 2) + circ(x, y, r * .62, '#E0245E', 1.5) + dot(x, y, r * .25, '#fff')


def pedestal(x, y, w=34, h=12, c='#B7B2C6'):
    return '<rect x="%g" y="%g" width="%g" height="%g" rx="3" fill="%s" %s/>' % (x - w / 2, y - h, w, h, c, O())


def basket(x, y, s=1):
    return at(x, y, s, False, shape('M-15 -16 h30 l-4 16 h-22 z', '#C98A4B') + line('M-13 -10 h26 M-12 -5 h24', '#8A4B1E', 1.5))


def door(x, y, w=44, h=70, c='#B8405E'):
    g = shape('M%g %g v-%g a%g %g 0 0 1 %g 0 v%g z' % (x - w / 2 - 6, y, h - w / 2, w / 2 + 6, w / 2 + 6, w + 12, h - w / 2), GOLD)
    g += shape('M%g %g v-%g a%g %g 0 0 1 %g 0 v%g z' % (x - w / 2, y, h - w / 2 - 4, w / 2, w / 2, w, h - w / 2 - 4), c)
    return g + line('M%g %g v-%g' % (x, y, h - 6), w=2) + dot(x - 5, y - h / 2 + 6, 2, GOLD) + dot(x + 5, y - h / 2 + 6, 2, GOLD)


def chest(x, y, s=1):
    g = '<rect x="-14" y="-14" width="28" height="14" rx="2" fill="#C98A4B" %s/>' % O()
    g += shape('M-14 -14 q14 -12 28 0 z', '#8A4B1E')
    g += circ(-6, -17, 3.5, GOLD, 1.5) + circ(1, -19, 3.5, GOLD, 1.5) + circ(8, -17, 3.5, GOLD, 1.5)
    return at(x, y, s, False, g)


def coins(x, y, n=3):
    return ''.join(circ(x + i * 5, y - (i % 2) * 3, 3, GOLD, 1.5) for i in range(n))


def umbrella(x, y, s=1):
    return at(x, y, s, False, line('M0 0 v-34', '#8A4B1E', 2.5) + shape('M-16 -34 q16 -16 32 0 z', '#E9C99A'))


def trident(x, y, s=1, h=64):
    return at(x, y, s, False, line('M0 0 v-%g' % h, '#8A4B1E', 3) + line('M-8 -%g q0 10 8 10 q8 0 8 -10 M0 -%g v12' % (h + 6, h + 10), '#9AA3B8', 3))


def axe(x, y, s=1):
    return at(x, y, s, False, line('M0 0 v-30', '#8A4B1E', 3) + shape('M0 -30 q10 -4 12 6 q-6 2 -12 0 z', '#9AA3B8', 2))


def leaf_page(x, y, s=1, rot=0):
    return ('<g transform="translate(%g %g) rotate(%g) scale(%g)"><rect x="-13" y="-4" width="26" height="8" rx="2" fill="#F3E3B5" %s/>'
            '<path d="M-9 -1 h18 M-9 2 h12" fill="none" stroke="#8A4B1E" stroke-width="1.2" stroke-linecap="round"/></g>' % (x, y, rot, s, O(1.8)))


def desk(x, y, s=1):
    return at(x, y, s, False, '<rect x="-20" y="-12" width="40" height="5" rx="2" fill="#C98A4B" %s/>' % O() + line('M-15 -7 v7 M15 -7 v7', '#8A4B1E', 3))


def plate(x, y, s=1):
    return at(x, y, s, False, ell(0, 0, 9, 3, GOLD, 2) + dot(-3, -3, 2.4, '#FF8A3D') + dot(3, -3, 2.4, '#E0245E') + dot(0, -5, 2.4, '#fff'))


def lying(x, y, inner, rot=-90):
    return '<g transform="translate(%g %g) rotate(%g)">%s</g>' % (x, y, rot, inner)


def tear(x, y):
    return shape('M%g %g q-3 5 0 7 q3 -2 0 -7z' % (x, y), '#7EC8FF', 1.2)
