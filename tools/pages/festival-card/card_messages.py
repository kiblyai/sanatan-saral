#!/usr/bin/env python3
"""Put the card messages from messages.py into the greeting-card script on festival-card.html and hi/festival-card.html,
so a card in any language gets its message in that language. Safe to run again after editing messages.py; then rebuild
the language pages with tools/page_translate.py build festival-card <langs>."""
import json, os, re, sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
from messages import ML, DEAR

LINE = ('var ML=%s,DEAR=%s;\n'
        "function mt(i,L,label){var m=cur().m[i]||cur().m[0],x=(ML[$('fc-f').value]||[])[i];if(x&&x[L])return x[L];"
        "return L==='hi'?m[1]:(L==='both'&&!label?m[0]+'\\n'+m[1]:m[0])}\n") % (
    json.dumps(ML, ensure_ascii=False, separators=(',', ':')), json.dumps(DEAR, ensure_ascii=False, separators=(',', ':')))

SWAPS = [
    ("box.innerHTML='';\n f.m.forEach(function(m,i){var lb=document.createElement('label');lb.innerHTML='<input type=\"radio\" name=\"fc-m\" value=\"'+i+'\"'+(i===0?' checked':'')+'> '+(useHi?m[1]:m[0]);",
     "box.innerHTML='';\n f.m.forEach(function(m,i){var lb=document.createElement('label');lb.innerHTML='<input type=\"radio\" name=\"fc-m\" value=\"'+i+'\"'+(i===0?' checked':'')+'> '+mt(i,L,1);"),
    ("return L==='hi'||L==='mr'?m[1]:(L==='both'?m[0]+'\\n'+m[1]:m[0]);}", "return mt(+r.value,L);}"),
    ("(L==='hi'||L==='both'?'प्रिय ':'Dear ')", "(DEAR[L]||'Dear ')"),
]

for p in ['festival-card.html', 'hi/festival-card.html']:
    path = os.path.join(ROOT, p)
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'var ML=.*?\nfunction mt\(.*?\n', '', s, count=1, flags=re.S)
    s = s.replace('var FONT={', LINE + 'var FONT={', 1)
    for a, b in SWAPS:
        if a in s:
            s = s.replace(a, b)
        elif b not in s:
            raise SystemExit('%s: could not find %s' % (p, a[:60]))
    open(path, 'w', encoding='utf-8').write(s)
    print(p, 'updated')
