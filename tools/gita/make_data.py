#!/usr/bin/env python3
"""Put a chapter's checked Sanskrit together with its word lists and translations, and write tools/gita/chNN.json.

    python3 -I tools/gita/make_data.py <folder with the three copies> <content module .py> [--check-words]

The Sanskrit is never typed by hand: it is taken from the open copy (see sources.py) and used only when all
three copies agree once two known typing faults are repaired. The content module holds META and V, where
V[verse] = (speaker, "word = meaning | word = meaning ...", translation).

--check-words compares the Sanskrit words in the word lists with the word division published alongside copy A,
and prints any that do not appear there. It is a spelling check on the word lists; meanings are not compared.
"""
import importlib.util, json, os, re, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sources as S
from translit import iast

SPEAKER_SKT = {'Krishna': 'श्री भगवानुवाच', 'Arjuna': 'अर्जुन उवाच', 'Sanjaya': 'सञ्जय उवाच', 'Dhritarashtra': 'धृतराष्ट्र उवाच'}


def repair(t):
    """Two typing faults in copy A: a short-i sign placed after the virama, and a stray nukta."""
    return re.sub(r'्ि([क-ह])', r'्\1ि', t).replace('़', '')


def src_verse(c, v):
    """Site numbering to the copies' numbering: they count one extra verse at the start of chapter 13."""
    return v + 1 if c == 13 else v


def norm_roman(w, theirs=True):
    """Bring both romanisations to one spelling: copy A's list writes śh, ṣh, ṛi and ch where IAST has ś, ṣ, ṛ and c."""
    w = w.lower().replace('ṁ', 'ṃ')
    if theirs:
        w = w.replace('chh', '\0').replace('ch', 'c').replace('\0', 'ch').replace('śh', 'ś').replace('ṣh', 'ṣ').replace('ṛi', 'ṛ')
    w = re.sub(r"[^a-zāīūṛṝḷṅñṭḍṇśṣḥṃ]", '', w)
    return re.sub(r'[ṃmṅñṇn]', 'N', w)


def made_of(word, parts, depth=4):
    """True if word is one of parts, or several of them joined (they divide compounds further than we do)."""
    if word in parts:
        return True
    if depth == 0:
        return False
    return any(word.startswith(p) and made_of(word[len(p):], parts, depth - 1) for p in parts if p and len(p) < len(word))


def main():
    folder, modpath = sys.argv[1], sys.argv[2]
    spec = importlib.util.spec_from_file_location('content', modpath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    c = mod.META['n']
    A = S.load(folder)
    C = S.copy_c(folder, c)
    raw = json.load(open(folder + '/verse.json', encoding='utf-8'))
    theirs = {(x['chapter_number'], x['verse_number']): x.get('word_meanings', '') for x in raw}
    verses, problems = [], 0
    for v in sorted(mod.V):
        sv = src_verse(c, v)
        a, b, cc = repair(A[(c, sv)]), repair(S.copy_b(folder, c, sv)), repair(C[sv])
        if not (S.key(a) == S.key(b) == S.key(cc)):
            problems += 1
            print('SANSKRIT NOT AGREED %d.%d' % (c, v), S.diff(S.key(a), S.key(b)), S.diff(S.key(a), S.key(cc)))
        speaker, words, tr = mod.V[v]
        opens = bool(S.speaker(a)) or bool(S.speaker(b))
        wl = []
        for part in words.split('|'):
            sk, _, en = part.partition('=')
            sk, en = sk.strip(), en.strip()
            if not sk or not en:
                problems += 1
                print('BAD WORD ENTRY %d.%d: %r' % (c, v, part))
            wl.append([sk, en])
        verses.append({'v': v, 'speaker': speaker, 'opens': SPEAKER_SKT[speaker] if opens else '',
                       'skt': S.lines(a), 'words': wl, 'tr': tr.strip()})
        if '--check-words' in sys.argv:
            # their list: "word—meaning; word—meaning": keep only the part before each dash
            have = set()
            for item in theirs[(c, sv)].split(';'):
                for w in re.split(r'[\s-]+', item.split('—')[0]):
                    if w.strip():
                        have.add(norm_roman(w))
            mine = [w for sk, _ in wl for w in re.split(r'[\s-]+', sk) if w]
            miss = [w for w in mine if not made_of(norm_roman(iast(w), False), have)]
            if miss:
                print('%d.%d words not in the published division: %s   (theirs: %s)' % (c, v, ' '.join(miss), ' '.join(sorted(have))[:160]))
    out = {'meta': mod.META, 'verses': verses}
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ch%02d.json' % c)
    open(path, 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    print('wrote %s: %d verses, %d problems' % (os.path.basename(path), len(verses), problems))


if __name__ == '__main__':
    main()
