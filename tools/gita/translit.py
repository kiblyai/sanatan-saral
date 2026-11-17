"""Devanagari to IAST, in the style the site's verse pages already use (anusvara as ṃ, avagraha as ')."""
V = {'अ': 'a', 'आ': 'ā', 'इ': 'i', 'ई': 'ī', 'उ': 'u', 'ऊ': 'ū', 'ऋ': 'ṛ', 'ॠ': 'ṝ', 'ऌ': 'ḷ', 'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au'}
M = {'ा': 'ā', 'ि': 'i', 'ी': 'ī', 'ु': 'u', 'ू': 'ū', 'ृ': 'ṛ', 'ॄ': 'ṝ', 'ॢ': 'ḷ', 'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au'}
C = {'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ṅ', 'च': 'c', 'छ': 'ch', 'ज': 'j', 'झ': 'jh', 'ञ': 'ñ',
     'ट': 'ṭ', 'ठ': 'ṭh', 'ड': 'ḍ', 'ढ': 'ḍh', 'ण': 'ṇ', 'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
     'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm', 'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v',
     'श': 'ś', 'ष': 'ṣ', 'स': 's', 'ह': 'h', 'ळ': 'ḻ'}
O = {'ं': 'ṃ', 'ः': 'ḥ', 'ँ': 'm̐', 'ऽ': "'", '।': '|', '॥': '||', 'ॐ': 'oṃ'}
VIRAMA = '्'


def iast(text):
    out, i, n = [], 0, len(text)
    while i < n:
        ch = text[i]
        if ch in C:
            out.append(C[ch])
            nxt = text[i + 1] if i + 1 < n else ''
            if nxt == VIRAMA:
                i += 2
                continue
            if nxt in M:
                out.append(M[nxt])
                i += 2
                continue
            out.append('a')
        elif ch in V:
            out.append(V[ch])
        elif ch in O:
            out.append(O[ch])
        else:
            out.append(ch)
        i += 1
    return ''.join(out)
