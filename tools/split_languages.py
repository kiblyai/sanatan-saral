#!/usr/bin/env python3
"""Make every page of sanatan.space carry one language only.

The pages were written with all nine languages side by side, e.g.
    <span class="en xg">Home</span><span class="hi">मुख्य</span><span class="gu">મુખ્ય</span>
and CSS hid the ones that did not match <html data-lang>. This tool cuts the
hidden ones out of the file, so /page.html holds English, /hi/page.html holds
Hindi, and so on. Where a language has no translation of a passage, the English
stays in (the same fallback the CSS gave).

Run from the repository root:
    python3 tools/split_languages.py            # rewrite every page in place
    python3 tools/split_languages.py --check    # report only, write nothing

It is safe to run again: a page that is already split is left as it is.
A new page can still be written with all languages side by side (in the root
and copied to the language folders); running this tool splits it.
"""
import os, re, sys, json, glob

LANGS = ['hi', 'gu', 'te', 'mr', 'ta', 'bn', 'kn', 'ml']          # folders, besides English in the root
ALL = ['en'] + LANGS
# class that hides the English fallback when a translation exists
XCLASS = {'gu': 'xg', 'te': 'xt', 'mr': 'xm', 'ta': 'xa', 'bn': 'xb', 'kn': 'xk', 'ml': 'xl'}
SITE = 'https://sanatan.space/'
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

TOKEN = re.compile(
    r'<!--.*?-->'
    r'|<(script|style)\b(?:[^>"\']|"[^"]*"|\'[^\']*\')*>.*?</\1\s*>'
    r'|<!\[CDATA\[.*?\]\]>'
    r'|<!(?:[^>"\']|"[^"]*"|\'[^\']*\')*>'
    r'|</([a-zA-Z][^\s>/]*)\s*>'
    r'|<([a-zA-Z][^\s>/]*)((?:[^>"\']|"[^"]*"|\'[^\']*\')*)>',
    re.S)
CLASS = re.compile(r'(?:^|\s)class\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', re.S)
ID = re.compile(r'(?:^|\s)id\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', re.S)


def hidden(classes, lang):
    """True when the stylesheet hides an element with these classes in this language."""
    c = set(classes)
    if 'en' in c and lang == 'hi':
        return True
    if 'hi' in c and lang != 'hi':
        return True
    for other in LANGS[1:]:
        if other in c and lang != other:
            return True
    x = XCLASS.get(lang)
    return bool(x and x in c)


def strip_hidden(html, lang, drop_lang_css=False):
    """Cut out every element (with its contents) that is hidden in `lang`.
    drop_lang_css also removes the <style id="xx-css"> blocks of the *other* languages (style.css carries the rules that
    hide their text). The page's own block stays where it is: its font rules must come after the page's own styles."""
    out, pos = [], 0
    stack = []            # (tag, removing_from_offset or None)
    cut_from = None       # offset where the element being removed starts
    cut_depth = None
    removed = 0
    for m in TOKEN.finditer(html):
        raw = m.group(0)
        if m.group(1):                      # <script> / <style> block, one token
            mid = ID.search(raw[:raw.find('>')])
            sid = (mid.group(1) or mid.group(2)) if mid else ''
            if cut_from is None and drop_lang_css and m.group(1).lower() == 'style' and sid.endswith('-css') and sid[:-4] in LANGS and sid[:-4] != lang:
                out.append(html[pos:m.start()]); pos = m.end() + (1 if html[m.end():m.end() + 1] == '\n' else 0); removed += 1
            continue
        if m.group(3):                      # start tag
            tag = m.group(3).lower()
            attrs = m.group(4) or ''
            selfclosing = attrs.rstrip().endswith('/')
            if cut_from is None:
                mc = CLASS.search(attrs)
                classes = (mc.group(1) or mc.group(2) or '').split() if mc else []
                mi = ID.search(attrs)
                eid = (mi.group(1) or mi.group(2)) if mi else ''
                # the home page's verse of the day switches its English lines on and off itself: keep them
                keep = lang != 'hi' and re.fullmatch(r'votd-(t|r|tr)-en', eid or '')
                if classes and not keep and hidden(classes, lang):
                    if tag in VOID or selfclosing:
                        out.append(html[pos:m.start()]); pos = m.end(); removed += 1
                        continue
                    cut_from, cut_depth = m.start(), len(stack)
            if tag not in VOID and not selfclosing:
                stack.append(tag)
        elif m.group(2):                    # end tag
            tag = m.group(2).lower()
            if tag in stack:
                while stack and stack[-1] != tag:
                    stack.pop()
                stack.pop()
                if cut_from is not None and len(stack) <= cut_depth:
                    out.append(html[pos:cut_from]); pos = m.end(); removed += 1
                    cut_from = cut_depth = None
    if cut_from is not None:
        raise ValueError('element opened at offset %d never closed' % cut_from)
    out.append(html[pos:])
    return ''.join(out), removed


def lang_script(lang, page, available):
    """The small head script: sets the language, sends returning readers to their language, makes the language buttons links."""
    return ('<script>/*lang-page*/(function(){var L=%s,P=%s,A=%s,d=document.documentElement;d.setAttribute("data-lang",L);d.classList.add("lm");'
            'var q=P==="index.html"?"":P;function U(M){var h=M!=="en"&&A.indexOf(M)>=0,s=location.search.replace(/^\\?/,"").split("&").filter(function(x){return x&&x.indexOf("lang=")!==0});'
            'if(M!=="en"&&!h)s.push("lang="+M);return(h?"/"+M+"/":"/")+q+(s.length?"?"+s.join("&"):"")+location.hash}'
            'if(L==="en"){var w=null;try{w=(new URLSearchParams(location.search).get("lang")||"").toLowerCase()||localStorage.getItem("sd-lang")}catch(e){}'
            'if(!w){var n=(navigator.language||"").toLowerCase().slice(0,2);if(A.indexOf(n)>=0)w=n}'
            'if(w&&w!=="en"&&A.indexOf(w)>=0){location.replace(U(w));return}}'
            'else{try{localStorage.setItem("sd-lang",L)}catch(e){}}'
            'document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a");'
            'if(a&&document.querySelector("base")){var h=a.getAttribute("href")||"";if(h.charAt(0)==="#"&&h.length>1){e.preventDefault();'
            'var t=document.getElementById(decodeURIComponent(h.slice(1)));if(t){t.scrollIntoView();history.replaceState(null,"",location.pathname+h)}return}}'
            'var b=e.target.closest&&e.target.closest(".lang button[data-set]");if(!b)return;var M=b.getAttribute("data-set");if(M===L)return;'
            'e.preventDefault();e.stopImmediatePropagation();try{localStorage.setItem("sd-lang",M)}catch(x){}location.href=U(M)},true)})();</script>'
            % (json.dumps(lang), json.dumps(page), json.dumps(available)))


# Raise a number when that file changes, so phones that cached the old copy fetch the new one (also in sw.js).
ASSET_V = {'style.css': '3', 'lang.js': '2'}
STYLESHEET = re.compile(r'<link\b[^>]*href="/?style\.css(?:\?v=\d+)?"')
ASSET = re.compile(r'\b(href|src)="(/?)(style\.css|lang\.js)(?:\?v=\d+)?"')
VOTD = re.compile(r'(var V=)(\[\{.*?\}\])(;\s*var day=)', re.S)


def patch_home(html, lang):
    """The home page has its scripts inline. Three small changes so they work on a one-language page."""
    # a) the inline copy of lang.js: the page language is fixed
    html = html.replace("  function setLang(l){\n    root.setAttribute('data-lang',l);",
                        "  var pageLang=root.getAttribute('data-page-lang');\n  function setLang(l,keep){\n    root.setAttribute('data-lang',l);", 1)
    html = html.replace("    try{localStorage.setItem('sd-lang',l)}catch(e){}\n  }\n  var saved=null;",
                        "    if(keep!==false){try{localStorage.setItem('sd-lang',l)}catch(e){}}\n  }\n  if(pageLang){setLang(pageLang,false);return}\n  var saved=null;", 1)
    # b) verse of the day: write only into the elements this page still has
    html = html.replace("var v=V[k], $=function(id){return document.getElementById(id)};",
                        "var v=V[k], $=function(id){return document.getElementById(id)}, S=function(id,x){var e=$(id);if(e)e.textContent=x};", 1)
    html = re.sub(r"\$\('(votd-(?:t|r|tr)-(?:en|hi))'\)\.textContent=(v\.(?:t|r|tr)\[[01]\]);", r"S('\1',\2);", html)
    html = html.replace("[(function(){try{return localStorage.getItem('sd-lang')}catch(e){}})()]||undefined,{day:'numeric'",
                        "[document.documentElement.getAttribute('data-lang')]||undefined,{day:'numeric'", 1)
    # c) verse of the day data: keep this page's language (and English, which is the fallback) only
    keep = {0, ALL.index(lang)} if lang != 'hi' else {1}

    def slim(m):
        verses = json.loads(m.group(2))
        for v in verses:
            for key in ('t', 'r', 'tr'):
                v[key] = [x if i in keep else '' for i, x in enumerate(v[key])]
        return m.group(1) + json.dumps(verses, ensure_ascii=False) + m.group(3)
    return VOTD.sub(slim, html, count=1)


HTML_TAG = re.compile(r'<html\b[^>]*>', re.I)
OLD_SCRIPT = re.compile(r'<script>/\*lang-page\*/.*?</script>\n?', re.S)
CANON = re.compile(r'<link\b[^>]*\brel="canonical"[^>]*>', re.I)


def process(path, lang, page, available):
    html = open(path, encoding='utf-8').read()
    has_css = bool(STYLESHEET.search(html))
    new, removed = strip_hidden(html, lang, drop_lang_css=has_css)
    # style.css and lang.js changed with the split: a new address keeps old cached copies away from new pages
    new = ASSET.sub(lambda m: '%s="%s%s?v=%s"' % (m.group(1), m.group(2), m.group(3), ASSET_V[m.group(3)]), new)
    if page == 'index.html':
        new = patch_home(new, lang)
    # <html lang data-lang data-page-lang>
    new = HTML_TAG.sub('<html lang="%s" data-lang="%s" data-page-lang="%s">' % (lang, lang, lang), new, count=1)
    # head script
    script = lang_script(lang, page, available)
    if OLD_SCRIPT.search(new):
        new = OLD_SCRIPT.sub(lambda m: script + '\n', new, count=1)
    else:
        new = re.sub(r'(<head\b[^>]*>\n?)', lambda m: m.group(1) + script + '\n', new, count=1)
    # canonical: each page is its own canonical; hreflang links tie the languages together
    url = SITE + ('' if lang == 'en' else lang + '/') + ('' if page == 'index.html' else page)
    canon = '<link rel="canonical" href="%s">' % url
    if CANON.search(new):
        new = CANON.sub(lambda m: canon, new, count=1)
    else:
        new = re.sub(r'(<link\b[^>]*\brel="alternate"[^>]*hreflang)', lambda m: canon + '\n' + m.group(1), new, count=1)
        if canon not in new:
            new = new.replace('</head>', canon + '\n</head>', 1)
    return html, new, removed


def main():
    check = '--check' in sys.argv
    pages = sorted(glob.glob('*.html'))
    avail = {p: [l for l in LANGS if os.path.exists(os.path.join(l, p))] for p in pages}
    total_before = total_after = changed = 0
    for p in pages:
        for lang in ['en'] + avail[p]:
            path = p if lang == 'en' else os.path.join(lang, p)
            old, new, removed = process(path, lang, p, avail[p])
            total_before += len(old.encode()); total_after += len(new.encode())
            if new != old:
                changed += 1
                if not check:
                    open(path, 'w', encoding='utf-8').write(new)
    print('%d files, %d changed, %.1f MB -> %.1f MB' % (sum(1 + len(v) for v in avail.values()), changed, total_before / 1e6, total_after / 1e6))


if __name__ == '__main__':
    main()
