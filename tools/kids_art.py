#!/usr/bin/env python3
"""The pictures for the kids' stories: three scenes per story, drawn with tools/kids_art_kit.py.

    python3 tools/kids_art.py            # write kids-art.js and put the cover pictures into every kids.html
    python3 tools/kids_art.py --sheet F  # write a preview page of all scenes to F (nothing else is changed)

Each scene is a 320 x 150 drawing. SCENES maps a story id (the same ids as the story data in kids.html) to
three scenes, one per page of the story. COVER says which of the three is shown on the story's card.
Pictures of sad moments are kept gentle on purpose: no arrows in flight, no injuries.
"""
import sys, os, re, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kids_art_kit import *

SCENES, COVER = {}, {}


def story(sid, cover):
    def deco(fn):
        SCENES[sid] = fn()
        COVER[sid] = cover
        return fn
    return deco


# ------------------------------------------------------------------ 1. Ganesha's race around the world
@story('ganesha', 1)
def _():
    kailash = sky('#DDF1FF', '#F4F8FF') + peaks()
    p1 = (kailash + shiva(128, 122, sit=True, arms=('down', 'up')) + parvati(176, 122, sit=True, arms=('up', 'down'))
          + mango(152, 56, 1.2) + sparkle(138, 44) + sparkle(168, 46)
          + boy(52, 132, .8, cloth='#FF8A3D', crown='crown', face='oh', arms=('down', 'up'))
          + ganesha(262, 134, .85, arms=('cheek', 'down')))
    orbit = '<ellipse cx="150" cy="112" rx="104" ry="24" fill="none" stroke="#C98A00" stroke-width="2.5" stroke-dasharray="6 7"/>'
    p2 = (kailash + orbit + shiva(130, 110, sit=True) + parvati(174, 110, sit=True)
          + peacock(262, 44, .6) + boy(262, 34, .45, cloth='#FF8A3D', crown='crown', face='happy')
          + ganesha(66, 136, .85, arms='namaste', face='happy') + mouse(108, 140, .8, flip=True)
          + line('M240 128 l10 6 -11 3', '#C98A00'))
    p3 = (kailash + shiva(110, 122, sit=True, face='happy') + parvati(160, 122, sit=True, face='happy', arms=('down', 'give'))
          + mango(190, 100, 1) + ganesha(214, 134, .85, face='happy', arms=('up', 'down'))
          + sparkle(196, 80) + sparkle(232, 70)
          + peacock(282, 132, .5) + boy(280, 123, .42, cloth='#FF8A3D', crown='crown', face='oh'))
    return [p1, p2, p3]


# ------------------------------------------------------------------ 2. Little Hanuman and the sun
@story('hanuman', 1)
def _():
    dawn = sky('#FFE3C2', '#9AD98B', 126)
    p1 = (dawn + hill(60, 150, 200, 34, '#7BCB6B') + sun(250, 92, 30, 'smile', '#FF6B3D', '#FFB36B')
          + '<path d="M0 126 q80 -6 160 0 t160 0 v30 h-320z" fill="#9AD98B"/>'
          + tree(34, 128, .9) + vanara(104, 122, .9, crown=True, sit=True, arms=('hip', 'point'), face='oh')
          + bubble(150, 52, 14, mango(150, 53, 1)))
    day = sky('#DDF7FF')
    trail = line('M40 138 q60 -30 104 -54', '#fff', 3, '3 8')
    flying = ('<g transform="translate(152 86) rotate(-24)">' + vanara(0, 30, 1, crown=True, arms=('down', 'M10 -21 q14 -8 22 -26'), face='happy') + '</g>')
    p2 = (day + sun(254, 50, 27) + cloud(52, 122, 1.1) + cloud(214, 136, .9) + trail + flying
          + cloud(46, 44, 1, '#E7EBF5') + king(46, 36, .55, cloth='#3B6BFF', must=False, face='worried', arms=('down', 'up'))
          + line('M66 22 l6 8 -6 2 7 9', '#FFB300', 3.5))
    sea = sky('#CFF1FF') + '<rect y="96" width="320" height="54" fill="#5FB7E8"/>' + waves(108) + waves(124) + waves(140)
    island = shape('M236 100 q30 -22 70 0 z', '#E9C99A') + shape('M258 86 l8 -20 8 20 z', GOLD) + shape('M276 88 l7 -16 7 16 z', GOLD)
    shore = shape('M0 150 v-50 q40 -10 66 8 q10 16 -4 42 z', '#E9C99A')
    leap = ('<g transform="translate(160 62) rotate(-12)">' + vanara(0, 30, 1.05, crown=True, arms=('M10 -20 q-10 10 -20 8', 'M10 -21 q14 -4 26 -10'), face='happy') + '</g>')
    p3 = (sea + island + shore + bear(34, 108, .8, arms=('down', 'point')) + line('M96 80 q30 -30 60 -24', '#fff', 3, '3 8') + leap
          + cloud(250, 30, .9) + sparkle(204, 34) + sparkle(118, 40))
    return [p1, p2, p3]


# ------------------------------------------------------------------ 3. Prahlada, the brave boy
@story('prahlada', 2)
def _():
    hall = sky('#FFE4EC') + '<rect y="122" width="320" height="28" fill="#E9B7C6"/>' + pillar(18, 124, 110, 18) + pillar(302, 124, 110, 18)
    vface = at(206, 80, .5, False, ''.join(human_head(skin=BLUE, crown='tall')))
    p1 = (hall + throne(84, 124, 1.15) + king(84, 120, 1.1, sit=True, face='angry', arms=('hip', 'point'))
          + boy(210, 130, .8, arms='namaste', face='calm', tilak=True) + bubble(214, 54, 17, vface))
    court = sky('#FFE4EC', '#E9B7C6', 124)
    glow = '<circle cx="160" cy="102" r="44" fill="#FFF3B0" opacity=".7"/>'
    p2 = (court + glow + elephant(70, 132, .9, bow=True) + boy(160, 130, .85, sit=True, arms='namaste', face='calm', tilak=True)
          + flame(232, 132, 1) + flame(252, 132, 1.3) + flame(274, 132, 1) + sparkle(160, 50) + sparkle(128, 66) + sparkle(194, 66))
    burst = ''.join(line('M%g %g l%g %g' % (160 + dx, 60 + dy, dx * .5, dy * .5), '#FFB300', 3) for dx, dy in ((-34, -30), (-44, 0), (34, -30), (44, 0), (0, -44)))
    p3 = (hall + shape('M132 124 v-100 h18 l-5 14 6 12 -6 14 5 14 -6 14 4 32 z', '#E9DCC3') + shape('M188 124 v-100 h-18 l5 14 -6 12 6 14 -5 14 6 14 -4 32 z', '#E9DCC3')
          + burst + narasimha(160, 124, 1.2, arms=('up', 'up'))
          + boy(232, 132, .8, flip=True, arms='namaste', face='happy', tilak=True)
          + king(66, 130, .9, face='oh', arms=('up', 'up')))
    return [p1, p2, p3]


# ------------------------------------------------------------------ 4. Dhruva and the pole star
@story('dhruva', 2)
def _():
    hall = sky('#E9FBE4') + '<rect y="122" width="320" height="28" fill="#BFE8B4"/>' + pillar(20, 124, 110, 18) + pillar(300, 124, 110, 18)
    p1 = (hall + throne(96, 124, 1.15, '#3B6BFF') + king(96, 120, 1.1, sit=True, cloth='#2F9E6E', face='worried')
          + queen(156, 128, 1, arms=('down', 'point'), face='angry')
          + boy(232, 132, .75, face='sad', arms=('down', 'down')) + line('M226 100 q-2 4 0 6', '#5AA9E6', 2.5))
    forest = sky('#DFF5E1', '#9AD98B', 126) + tree(28, 128, 1.1) + tree(292, 128, 1.2) + tree(66, 126, .8, '#6FCF7F')
    veena = line('M12 -26 l20 -22', '#8A4B1E', 3.5) + circ(12, -24, 5, '#C98A4B', 2)
    p2 = (forest + sage(126, 130, 1, cloth='#FFB36B', hair='#3B2A5A', beard=None, arms=('bless', 'down'), front=veena, flip=True)
          + boy(200, 132, .85, sit=True, arms='namaste', face='calm') + sparkle(164, 60) + sparkle(178, 78, 4))
    night = sky('#2B2A6B', '#3F6B4F', 128) + stars(22, 4, 80)
    ray = '<path d="M196 30 L150 128 L242 128 z" fill="#FFF3B0" opacity=".25"/>'
    p3 = (night + ray + star(196, 26, 13) + sparkle(222, 18, 4, '#fff') + sparkle(170, 22, 4, '#fff')
          + vishnu(110, 130, 1.1, arms=('down', 'bless'), face='happy') + boy(196, 134, .85, sit=True, arms='namaste', face='happy'))
    return [p1, p2, p3]


# ------------------------------------------------------------------ 5. Krishna and his poor friend Sudama
def sudama(x, y, s=1, **k):
    return person(x, y, s, cloth='#F3E9D2', top=SK, style='tuft', tilak=True, **k)


@story('sudama', 2)
def _():
    school = sky('#FFEBD6', '#BFE3A6', 126) + tree(54, 128, 1.5) + hut(268, 126, 1.1)
    p1 = (school + sage(100, 132, .9, sit=True, arms=('down', 'bless'))
          + krishna(176, 132, .8, arms=('down', 'out'), face='happy') + boy(206, 132, .8, cloth='#F3E9D2', style='tuft', face='happy', arms=('out', 'down'))
          + leaf_page(190, 138, .9) + sparkle(192, 64))
    road = sky('#FFEBD6', '#E9D2A6', 128)
    p2 = (road + palace(214, 128, 1.45) + person(246, 130, .7, cloth='#3B6BFF', crown='band', must=True, front=line('M16 0 v-46', '#8A4B1E', 3))
          + sudama(74, 134, 1, face='worried', arms=('down', 'hold')) + bundle(98, 122, 1)
          + line('M96 96 q8 -8 16 -2', '#5AA9E6', 2) )
    hall = sky('#FFEBD6') + '<rect y="122" width="320" height="28" fill="#F2C9A0"/>' + pillar(22, 124, 110, 18, '#FFF3D6') + pillar(298, 124, 110, 18, '#FFF3D6')
    heart = lambda x, y, s=1: at(x, y, s, False, '<path d="M0 4 q-9 -7 -5 -12 q3 -3 5 1 q2 -4 5 -1 q4 5 -5 12z" fill="#FF6B8B" %s/>' % O(1.5))
    p3 = (hall + krishna(144, 130, 1.1, king=True, face='happy', arms=('down', 'fwd')) + sudama(180, 130, 1.05, flip=True, face='happy', arms=('down', 'fwd'))
          + heart(162, 44) + heart(182, 58, .7) + heart(140, 60, .7)
          + bundle(238, 132, 1.2) + dot(250, 130, 1.5, '#fff') + dot(255, 132, 1.5, '#fff') + dot(252, 126, 1.5, '#fff')
          + line('M228 122 q10 -8 20 0', w=1.5))
    return [p1, p2, p3]


# ------------------------------------------------------------------ 6. Ekalavya, the dedicated student
def ekalavya(x, y, s=.85, **k):
    return person(x, y, s, skin=SKD, cloth='#6FA86B', top=SKD, crown='band', **k)


def drona(x, y, s=1, **k):
    return sage(x, y, s, cloth='#F3F0FA', sash='#FF9F45', **k)


@story('ekalavya', 1)
def _():
    field = sky('#EFE8FF', '#CDE8B5', 126)
    p1 = (field + tree(24, 128, 1.1) + target(24, 86, 9)
          + boy(74, 132, .75, cloth='#3B6BFF', crown='crown', front=bow(16, -20, .7, 0, False)) + boy(110, 132, .75, cloth='#E0245E', crown='crown', front=bow(16, -20, .7, 0, False))
          + drona(176, 132, 1.05, face='worried', arms=('down', 'bless'))
          + ekalavya(256, 132, .85, flip=True, arms='namaste', face='sad'))
    forest = sky('#E6F6E0', '#A9DB95', 126) + tree(292, 128, 1.5) + tree(20, 128, 1) + bush(96, 128, .8)
    statue = person(60, 114, .9, skin='#C98A4B', cloth='#B5763A', hair='#A8672E', style='sage', beard='#D9A066', face='calm')
    arrow = line('M196 86 h68', '#8A4B1E', 2) + '<path d="M262 82 l8 4 -8 4 z" fill="%s"/>' % INK
    p2 = (forest + pedestal(60, 128, 44, 14) + statue + garland(46, 96, 74, 96, 7, 7)
          + target(292, 86, 12) + arrow
          + ekalavya(170, 132, .95, arms=('down', 'fwd'), face='calm', front=bow(26, -18, .9, 0, False)))
    p3 = (forest + pedestal(250, 128, 36, 12) + person(250, 116, .7, skin='#C98A4B', cloth='#B5763A', hair='#A8672E', style='sage', beard='#D9A066', face='calm')
          + drona(120, 132, 1.05, face='sad', arms=('down', 'down')) + boy(70, 132, .75, cloth='#E0245E', crown='crown', face='oh')
          + ekalavya(184, 132, .9, flip=True, sit=True, arms='namaste', face='calm'))
    return [p1, p2, p3]


# ------------------------------------------------------------------ 7. Shravan Kumar, the loving son
def elder(x, y, s=.6, woman=False, **k):
    k.setdefault('face', 'smile')
    return person(x, y, s, cloth='#F3F0FA' if not woman else '#E9C1F0', hair=GREY, style='long' if woman else 'short', **k)


@story('shravan', 0)
def _():
    road = sky('#FFF1C9', '#D9E8A6', 128) + hill(60, 128, 160, 22, '#BFE3A6') + hill(250, 128, 180, 26, '#BFE3A6')
    temple = at(280, 104, .7, False, shape('M-12 0 v-20 q12 -26 24 0 v20 z', '#FFB36B') + line('M0 -34 v-8', w=2) + shape('M0 -42 l8 3 -8 3z', '#FF8A3D', 1.5))
    pole = line('M36 104 h248', '#8A4B1E', 4.5)
    ropes = line('M62 104 l-17 18 M62 104 l17 18 M258 104 l-17 18 M258 104 l17 18', '#8A4B1E', 2)
    p1 = (road + temple
          + person(160, 142, 1.6, cloth='#FFB300', top=SK, arms=('M10 -20 q7 0 9 -4', 'M10 -20 q7 0 9 -4'), face='happy') + pole
          + elder(62, 140, .68, face='happy') + elder(258, 140, .68, woman=True, face='happy')
          + basket(62, 141, 1.2) + basket(258, 141, 1.2) + ropes)
    dusk = sky('#F9D2B0', '#B9D69A', 122) + moon(282, 30, 11) + '<path d="M150 150 q20 -34 80 -30 q50 2 90 -8 v38 z" fill="#7EC8F2"/>' + waves(138, '#fff', 4, 190, 320)
    sound = line('M236 96 q6 6 0 12 M244 92 q9 10 0 20', '#8A4B1E', 2)
    p2 = (dusk + bush(40, 126, 1.5, '#4FAE66') + bush(84, 128, 1.1, '#62C077')
          + king(58, 118, .8, face='worried', cloth='#7A4FD6', arms=('down', 'hold'), front=bow(18, -22, .8, 0, False))
          + person(196, 128, .95, cloth='#FFB300', top=SK, sit=True, arms=('down', 'give'), face='smile') + pot(226, 122, 1) + sound)
    night = sky('#3A3A7A', '#55708A', 126) + stars(16, 9, 60) + moon(40, 28, 10)
    p3 = (night + basket(52, 132, .9) + elder(110, 132, .9, sit=True, face='sad') + elder(154, 132, .9, woman=True, sit=True, face='sad')
          + tear(104, 96) + tear(160, 96)
          + king(236, 132, .95, flip=True, sit=True, face='sad', cloth='#7A4FD6', arms=('down', 'give')) + pot(204, 124, 1))
    return [p1, p2, p3]


# ------------------------------------------------------------------ 8. The little squirrel who helped build the bridge
@story('squirrel', 2)
def _():
    sea = sky('#DDF7FF') + '<rect y="92" width="320" height="58" fill="#5FB7E8"/>' + waves(104) + waves(138)
    shore = shape('M0 150 v-54 q44 -8 70 8 q6 20 -6 46 z', '#E9C99A')
    stones = ''.join(rock(84 + i * 26, 128, 26, '#B7B2C6' if i % 2 else '#C9C5D6') for i in range(6))
    lanka = shape('M262 94 q24 -16 58 0 z', '#E9C99A') + shape('M286 84 l6 -14 6 14 z', GOLD)
    carry = lambda x, y, s, c: vanara(x, y, s, cloth=c, arms=('up', 'up'), front=rock(0, -62, 26, '#9E98B3'))
    p1 = (sea + lanka + shore + stones + carry(40, 110, .8, '#E86A2E') + carry(116, 112, .85, '#3B6BFF') + carry(196, 112, .85, '#2F9E6E'))
    big = sky('#DDF7FF') + '<rect y="96" width="320" height="54" fill="#5FB7E8"/>' + waves(106)
    slabs = ''.join(rock(20 + i * 56, 150, 62, '#B7B2C6' if i % 2 else '#C9C5D6') for i in range(6))
    sand = ''.join(dot(118 + (i * 7) % 34, 96 + (i * 5) % 22, 1.6, '#D9A441') for i in range(14))
    p2 = (big + slabs + squirrel(120, 100, 1.5, flip=True) + sand + line('M92 70 q-6 6 0 12 M150 66 q6 6 0 12', '#8A4B1E', 2)
          + vanara(226, 112, .85, cloth='#3B6BFF', face='smile', arms=('down', 'point'), flip=True) + vanara(280, 112, .85, cloth='#2F9E6E', face='smile', arms=('cheek', 'down'), flip=True))
    p3 = (big + slabs + rama(112, 116, 1.3, sit=True, face='happy', arms=('down', 'M10 -19 q14 8 28 2'))
          + squirrel(172, 96, 1.05, flip=True, stripes=True) + sparkle(186, 52) + sparkle(204, 74, 4) + sparkle(150, 44, 4)
          + vanara(262, 112, .8, cloth='#E86A2E', face='smile', crown=True, flip=True, arms='namaste'))
    return [p1, p2, p3]


# ------------------------------------------------------------------ 9. Nachiketa, the boy who questioned Death
@story('nachiketa', 2)
def _():
    ashram = sky('#FFE8F0', '#C9E3A9', 126) + hut(40, 126, 1.2) + tree(296, 128, 1.1)
    p1 = (ashram + sage(150, 132, 1.05, hair=HAIR, beard=HAIR, face='angry', arms=('down', 'out'))
          + boy(100, 132, .8, style='tuft', face='worried', arms=('down', 'up'))
          + cow(222, 132, 1.1, thin=True, col='#EDE3D0') + cow(266, 134, 1, thin=True, col='#E3D8C2', flip=True))
    realm = sky('#3A2F6B') + stars(18, 5, 70) + '<rect y="124" width="320" height="26" fill="#57498F"/>'
    three = moon(52, 28, 8) + moon(86, 28, 8) + moon(120, 28, 8)
    p2 = (realm + three + pillar(170, 126, 96, 16, '#8E7CC3') + pillar(290, 126, 96, 16, '#8E7CC3') + door(230, 126, 56, 86)
          + boy(104, 134, .85, style='tuft', sit=True, face='calm', arms=('down', 'down')))
    hall = sky('#4A3C80') + '<rect y="122" width="320" height="28" fill="#6A5AA8"/>' + pillar(18, 124, 110, 16, '#8E7CC3') + pillar(302, 124, 110, 16, '#8E7CC3')
    light = '<circle cx="232" cy="46" r="20" fill="#FFF3B0" opacity=".5"/>' + flame(232, 58, 1)
    p3 = (hall + throne(72, 124, 1.15, '#2B1B4D') + yama(72, 120, 1.1, sit=True, face='smile', arms=('down', 'give'))
          + chest(130, 132, 1.1) + coins(150, 132, 3) + shape('M166 132 l2 -10 5 6 3 -8 3 8 5 -6 2 10 z', GOLD)
          + boy(232, 134, .85, style='tuft', flip=True, face='calm', arms=('down', 'bless')) + light
          + buffalo(274, 140, .6, flip=True))
    return [p1, p2, p3]


# ------------------------------------------------------------------ 10. Krishna lifts the mountain
def villager(x, y, s=.8, cloth='#FF9ECB', woman=False, **k):
    return person(x, y, s, cloth=cloth, style='long' if woman else 'short', **k)


@story('govardhan', 2)
def _():
    vr = sky('#E6FFE0', '#A9DB95', 126)
    bighill = shape('M150 126 q24 -70 76 -74 q40 -22 70 6 q30 20 30 68 z', '#6BCB77') + line('M214 70 q10 8 22 2 M262 66 q10 8 20 2', '#2E9E4F') + dot(240, 96, 3, '#FF9ECB') + dot(280, 100, 3, GOLD)
    p1 = (vr + bighill + cow(232, 114, .7) + cow(286, 122, .7, flip=True)
          + villager(42, 132, .85, '#FF8A3D', arms=('down', 'give'), front=plate(22, -18)) + villager(84, 132, .85, '#B9A6FF', woman=True, arms=('down', 'give'), front=plate(22, -18))
          + krishna(140, 132, .8, arms=('down', 'point'), face='happy'))
    storm = sky('#7C88A8') + '<rect y="120" width="320" height="30" fill="#5E8F6B"/>' + '<path d="M0 138 q80 -8 160 0 t160 0 v12 h-320z" fill="#5AA9E6"/>'
    dark = lambda x, y, s: cloud(x, y, s, '#4E5674')
    p2 = (storm + dark(60, 26, 1.5) + dark(266, 26, 1.5) + dark(164, 58, 1.7) + king(164, 52, .62, cloth='#3B6BFF', must=False, face='angry', arms=('up', 'up'))
          + line('M204 66 l8 12 -7 2 9 14', '#FFD23F', 3.5)
          + rain(26, '#BFE0FF', 7, True)
          + villager(96, 134, .85, '#FF8A3D', face='worried', arms=('up', 'up')) + villager(134, 134, .85, '#B9A6FF', woman=True, face='worried')
          + boy(168, 134, .65, cloth='#FF9ECB', face='sad') + cow(228, 134, 1) )
    p3 = (sky('#E6FFE0') + rain(12, '#5AA9E6', 11) + '<rect x="44" y="76" width="232" height="74" fill="#E6FFE0"/>'
          + shape('M44 76 q20 -42 72 -38 q24 -18 50 -4 q40 -10 66 16 q26 6 44 26 z', '#6BCB77') + line('M100 50 q10 8 22 2 M172 44 q10 10 24 4', '#2E9E4F') + dot(88, 64, 3, '#FF9ECB') + dot(214, 60, 3, GOLD) + dot(148, 58, 3, '#fff')
          + line('M30 142 h260', '#2E9E4F', 3)
          + krishna(160, 140, 1, face='happy', arms=('down', 'M10 -21 q12 -14 8 -42'))
          + villager(94, 140, .7, '#FF9ECB', woman=True, face='happy') + boy(120, 140, .6, cloth='#FF8A3D', face='happy') + villager(208, 140, .7, '#B9A6FF', face='happy')
          + cow(250, 140, .9) + cow(60, 140, .75, flip=True))
    return [p1, p2, p3]


# ------------------------------------------------------------------ 11. Savitri, who would not give up
def savitri(x, y, s=1, **k):
    return person(x, y, s, cloth='#F0553A', style='long', crown='crown', bindi=True, **k)


def satyavan(x, y, s=1, **k):
    return person(x, y, s, cloth='#6FA86B', top=SK, style='short', **k)


@story('savitri', 1)
def _():
    forest = sky('#FFEBD9', '#A9DB95', 126) + tree(30, 128, 1.3) + tree(296, 128, 1.4) + bush(250, 128, .8)
    veena = line('M-12 -26 l-20 -22', '#8A4B1E', 3.5) + circ(-12, -24, 5, '#C98A4B', 2)
    p1 = (forest + sage(84, 132, .95, cloth='#FFB36B', hair='#3B2A5A', beard=None, face='worried', arms=('down', 'up'), front=veena)
          + savitri(162, 132, 1, face='happy', arms=('down', 'fwd')) + satyavan(214, 132, 1, flip=True, face='happy', arms=('down', 'fwd'), behind=axe(-16, 0, 1))
          + garland(176, 96, 200, 96, 8, 8))
    night = sky('#2B2A6B', '#3F6B4F', 128) + stars(16, 2, 60) + moon(280, 26, 10) + tree(34, 130, 1.3, '#3E8F5A') + tree(304, 130, 1.1, '#3E8F5A')
    soul = '<circle cx="276" cy="110" r="12" fill="#FFF3B0" opacity=".55"/>' + circ(276, 110, 5, '#FFF3B0', 1.5)
    steps = line('M118 140 h10 M140 140 h10 M162 140 h10', '#fff', 2)
    p2 = (night + lying(62, 132, satyavan(0, 0, .9, face='sleep')) + steps
          + savitri(190, 134, 1, face='calm', arms=('down', 'fwd')) + yama(248, 134, 1.05, face='calm', arms=('down', 'hold')) + soul)
    dawn = sky('#FFE3C2', '#A9DB95', 126) + sun(46, 118, 22, None, '#FF8A3D', '#FFB36B') + '<path d="M0 126 q80 -6 160 0 t160 0 v30 h-320z" fill="#A9DB95"/>' + tree(300, 128, 1.3)
    p3 = (dawn + yama(110, 132, 1.05, face='happy', arms=('down', 'bless'))
          + savitri(190, 132, 1, face='happy', arms='namaste') + satyavan(236, 132, 1, face='happy', arms=('down', 'up'))
          + sparkle(160, 60) + sparkle(214, 50) + sparkle(262, 70, 4))
    return [p1, p2, p3]


# ------------------------------------------------------------------ 12. Markandeya, the boy who beat death
@story('markandeya', 2)
def _():
    hills = sky('#EFE8FF', '#D9D2F2', 126) + peaks('#F7F4FF')
    glow = '<circle cx="230" cy="84" r="46" fill="#FFF3B0" opacity=".7"/>'
    p1 = (hills + glow + shiva(230, 130, 1.15, arms=('down', 'bless'), face='happy', behind=trident(-24, 0, 1, 62))
          + sage(84, 134, .95, hair=HAIR, beard=HAIR, sit=True, arms='namaste', face='calm') + person(132, 134, .95, cloth='#FFB36B', style='long', bindi=True, sit=True, arms='namaste', face='calm'))
    temple = sky('#E9E2FF') + '<rect y="124" width="320" height="26" fill="#C9BDEE"/>' + pillar(16, 126, 112, 16, '#F7F4FF') + shape('M226 126 v-70 a34 34 0 0 1 68 0 v70 z', '#8FD0FF') + line('M226 126 v-70 a34 34 0 0 1 68 0 v70', w=2.5)
    rope = line('M246 96 q-10 -4 -8 6 q2 8 10 4 q6 -4 0 -10', '#C98A4B', 3)
    p2 = (temple + linga(96, 128, 1.5) + flame(52, 120, .7) + pedestal(52, 128, 14, 10, GOLD)
          + boy(152, 134, .85, sit=True, arms='namaste', face='calm', tilak=True)
          + buffalo(262, 132, .85) + yama(262, 114, .8, sit=True, flip=True, face='smile', arms=('down', 'hold')) + rope)
    burst = ''.join(line('M%g %g l%g %g' % (120 + dx, 44 + dy, dx * .45, dy * .45), '#FFB300', 3) for dx, dy in ((-44, -18), (-50, 12), (44, -18), (50, 12), (-20, -36), (20, -36)))
    lasso = line('M150 104 q40 -30 96 -8', '#C98A4B', 3) + '<ellipse cx="120" cy="100" rx="30" ry="9" fill="none" stroke="#C98A4B" stroke-width="3"/>'
    p3 = (sky('#E9E2FF') + '<rect y="124" width="320" height="26" fill="#C9BDEE"/>' + burst
          + shiva(120, 110, 1.25, face='angry', arms=('down', 'up'), behind=trident(26, -14, 1, 60))
          + linga(120, 128, 1.5) + lasso
          + boy(160, 134, .8, flip=True, arms=('down', 'fwd'), face='calm', tilak=True)
          + yama(262, 134, 1, face='oh', arms=('up', 'up'), flip=True))
    return [p1, p2, p3]


# ------------------------------------------------------------------ 13. Vamana and the generous king Bali
def bali(x, y, s=1, **k):
    return person(x, y, s, skin=SKD, cloth='#7A4FD6', crown='crown', must=True, sash=GOLD, wide=2, **k)


def vamana(x, y, s=.6, **k):
    return person(x, y, s, cloth='#FFB36B', top=SK, style='tuft', tilak=True, **k)


@story('vamana', 1)
def _():
    hall = sky('#FFF4CF') + '<rect y="122" width="320" height="28" fill="#F2DC9A"/>' + pillar(18, 124, 110, 18, '#FFFBEA') + pillar(302, 124, 110, 18, '#FFFBEA')
    p1 = (hall + throne(70, 124, 1.15, '#4B2FA8') + bali(70, 120, 1.1, sit=True, face='happy', arms=('down', 'give'))
          + coins(100, 104, 3) + villager(150, 132, .85, '#FF8A3D', face='happy', arms=('give', 'down'), flip=False)
          + villager(196, 132, .85, '#7EC8F2', woman=True, face='happy') + boy(236, 132, .65, cloth='#9DFF8A', face='happy', arms=('up', 'down'))
          + chest(118, 132, .9))
    court = sky('#FFF4CF', '#F2DC9A', 124)
    water = line('M168 96 q-8 10 -14 22', '#5AA9E6', 2.5, '2 6')
    p2 = (court + sage(266, 132, .95, cloth='#F3F0FA', face='worried', arms=('up', 'down'), flip=True)
          + bali(204, 132, 1.1, flip=True, face='happy', arms=('down', 'M10 -20 q12 -2 20 -8')) + pot(172, 100, .8, GOLD) + water
          + vamana(110, 134, .8, face='smile', arms=('hold', 'give'), behind=umbrella(-20, 0, 1.1)) + pot(138, 132, .6))
    space = sky('#2B2A6B') + stars(26, 8, 140) + '<circle cx="84" cy="176" r="52" fill="#5FB7E8" %s/>' % O() + '<path d="M52 150 q10 -14 26 -8 q8 10 -2 14 z M96 136 q14 -6 22 6 q-8 10 -20 4 z" fill="#6BCB77"/>'
    leg = limb('M132 108 q50 4 96 -24', '#FFB36B', 9) + ell(238, 80, 15, 8, SK)
    p3 = (space + limb('M100 108 v22', '#FFB36B', 9) + ell(98, 132, 13, 6, SK) + leg
          + person(116, 110, 1.75, cloth='#FFB36B', top=SK, style='tuft', tilak=True, halo=True, face='smile', arms=('down', 'bless'))
          + bali(256, 140, .8, flip=True, sit=True, face='calm', arms='namaste') + sparkle(286, 58, 4, '#fff') + sparkle(196, 30, 4, '#fff'))
    return [p1, p2, p3]


# ------------------------------------------------------------------ 14. Ganesha writes the Mahabharata
def vyasa(x, y, s=1, **k):
    return sage(x, y, s, cloth='#FF9F45', **k)


@story('ganesha-scribe', 1)
def _():
    ash = sky('#DDF7FF', '#BFE3A6', 126) + tree(296, 128, 1.3) + hut(30, 126, 1)
    leaves = ''.join(leaf_page(x, y, .9, r) for x, y, r in ((92, 52, -18), (126, 34, 8), (166, 30, -6), (204, 44, 16), (150, 60, 0)))
    p1 = (ash + leaves + vyasa(108, 134, 1.05, sit=True, face='calm', arms=('cheek', 'down'))
          + ganesha(226, 134, .95, flip=True, face='happy', arms=('down', 'up'), front=line('M22 -47 l4 -12', '#8A4B1E', 2.5)))
    speech = line('M134 84 q8 -4 8 -12 M142 92 q14 -6 14 -20 M150 100 q20 -8 20 -28', '#FF8A3D', 2.5)
    stack = leaf_page(266, 132, 1) + leaf_page(266, 126, 1) + leaf_page(266, 120, 1)
    p2 = (ash + vyasa(96, 134, 1.05, sit=True, face='happy', arms=('down', 'bless')) + speech
          + ganesha(214, 134, 1, flip=True, sit=True, arms=('cheek', 'M10 -18 q8 6 16 8')) + desk(186, 134, 1) + leaf_page(186, 119, 1) + line('M196 112 l-6 6', '#8A4B1E', 2.5)
          + stack + circ(234, 62, 3, '#fff', 2) + circ(242, 50, 5, '#fff', 2))
    broken = line('M120 138 l12 -3 M138 134 l10 3', '#8A4B1E', 2.5)
    tuskpen = '<path d="M196 110 l-7 8" fill="none" stroke="%s" stroke-width="6" stroke-linecap="round"/><path d="M196 110 l-7 8" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>' % INK
    p3 = (ash + vyasa(84, 134, 1.05, sit=True, face='happy', arms=('down', 'down')) + broken
          + ganesha(214, 134, 1, flip=True, sit=True, face='happy', tusk='broken', arms=('down', 'M10 -18 q8 6 16 8')) + desk(186, 134, 1) + leaf_page(186, 119, 1) + tuskpen
          + stack + sparkle(168, 92) + sparkle(204, 60, 4))
    return [p1, p2, p3]


# ------------------------------------------------------------------ output

CSS = ('.kid-art .o{stroke:#1a1446;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}'
       '.kid-art .p{stroke:#1a1446;stroke-linecap:round;stroke-linejoin:round}'
       '.kid-art .r{stroke-linecap:round;stroke-linejoin:round}')
ROUND = ' stroke-linecap="round" stroke-linejoin="round"'


def compact(s):
    """Shorten the markup: the outline attributes repeat thousands of times, so they become classes (see CSS)."""
    s = s.replace(' stroke="%s" stroke-width="2.5"%s' % (INK, ROUND), ' class="o"')
    s = re.sub(r' stroke="%s" (stroke-width="[\d.]+")%s' % (INK, ROUND), r' class="p" \1', s)
    return s.replace(ROUND, ' class="r"')


def svg(inner, label=''):
    return '<svg class="kid-art" viewBox="0 0 320 150" role="img" aria-label="%s">%s</svg>' % (label, inner)


def sheet(path, small=True):
    h = ('<!doctype html><meta charset="utf-8"><style>body{margin:0;padding:16px;background:#FFF8E7;font:14px system-ui}'
         '.g{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:6px}h2{font-size:15px;margin:10px 0 6px}'
         'svg{display:block;width:100%%;height:auto;border:3px solid #1a1446;border-radius:14px;background:#fff}.c{outline:4px solid #E0245E;border-radius:14px}%s</style>' % CSS)
    for sid, sc in SCENES.items():
        h += '<h2>%s (card shows picture %d)</h2><div class="g">' % (sid, COVER[sid] + 1)
        for i, s in enumerate(sc):
            h += '<div class="%s">%s</div>' % ('c' if i == COVER[sid] else '', svg(compact(s) if small else s))
        h += '</div>'
    open(path, 'w', encoding='utf-8').write(h)


LANG_PAGES = ['kids.html'] + [l + '/kids.html' for l in ('hi', 'gu', 'te', 'mr', 'ta', 'bn', 'kn', 'ml')]
TILE = re.compile(r'(data-open="([^"]+)"[^>]*>\s*<span class="k-art">\s*<svg\b[^>]*>)(.*?)(</svg>)', re.S)
HOOK = "function render(){\n    var l=L(), n=cur.p[l].length;"
PAINT = ("\n    /*kids-art*/var A=(window.KIDS_ART||{})[cur.id];if(A){$('k-art').innerHTML='<svg class=\"kid-art\" viewBox=\"0 0 320 150\" role=\"img\" aria-label=\"'"
         "+esc(X(cur.t)).replace(/\"/g,'&quot;')+'\">'+A.p[(mode==='read'&&pg<A.p.length)?pg:A.c]+'</svg>'}")
TAG = '<script defer src="kids-art.js?v=1"></script>\n'
STYLE = '<style id="kidsart-css">%s</style>\n' % CSS


def write_site(root='.'):
    data = {sid: {'p': [compact(x) for x in sc], 'c': COVER[sid]} for sid, sc in SCENES.items()}
    js = '/* Pictures for the kids\' stories. Made by tools/kids_art.py: edit that, not this file. */\nwindow.KIDS_ART=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n'
    open(os.path.join(root, 'kids-art.js'), 'w', encoding='utf-8').write(js)
    print('kids-art.js', len(js) // 1024, 'KB')
    for page in LANG_PAGES:
        path = os.path.join(root, page)
        h = open(path, encoding='utf-8').read()
        seen = []

        def cover(m):
            seen.append(m.group(2))
            return m.group(1) + data[m.group(2)]['p'][data[m.group(2)]['c']] + m.group(4)
        h = TILE.sub(cover, h)
        assert sorted(seen) == sorted(SCENES), (page, seen)
        if '/*kids-art*/' not in h:
            assert h.count(HOOK) == 1, page
            h = h.replace(HOOK, HOOK + PAINT)
        h = re.sub(r'<style id="kidsart-css">.*?</style>\n', '', h, flags=re.S).replace('</head>', STYLE + '</head>', 1)
        if 'kids-art.js' not in h.split('</head>')[1].replace(PAINT, ''):
            i = h.rfind('</body>')
            h = h[:i] + TAG + h[i:]
        open(path, 'w', encoding='utf-8').write(h)
        print(page, len(h) // 1024, 'KB')


if __name__ == '__main__':
    if '--sheet' in sys.argv:
        sheet(sys.argv[sys.argv.index('--sheet') + 1], '--raw' not in sys.argv)
        print('sheet:', len(SCENES), 'stories')
    else:
        write_site()
