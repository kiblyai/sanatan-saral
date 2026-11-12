#!/usr/bin/env python3
"""Put a short notice in the footer of every translated page: the translation is machine-made and
checked only by the site's editor. Safe to run again (it replaces its own notice). Run from the site root.

    python3 tools/translation_notice.py           # write
    python3 tools/translation_notice.py --check   # report only
"""
import glob, os, re, sys

# (notice, link text) per language. English pages carry no notice; the About page explains how the site is made.
NOTICE = {
    'hi': ('यह अनुवाद मशीन की सहायता से बना है और अभी तक केवल साइट के सम्पादक ने इसे जाँचा है; इसमें त्रुटियाँ हो सकती हैं।', 'यह साइट कैसे बनती है'),
    'gu': ('આ અનુવાદ મશીનની મદદથી બન્યો છે અને હજી સુધી ફક્ત સાઇટના સંપાદકે તેને તપાસ્યો છે; તેમાં ભૂલો હોઈ શકે છે.', 'આ સાઇટ કેવી રીતે બને છે'),
    'te': ('ఈ అనువాదం యంత్రం సహాయంతో చేయబడింది; ఇప్పటివరకు సైట్ సంపాదకుడు మాత్రమే దీన్ని పరిశీలించారు. ఇందులో తప్పులు ఉండవచ్చు.', 'ఈ సైట్ ఎలా తయారవుతుంది'),
    'mr': ('हे भाषांतर यंत्राच्या मदतीने केले आहे आणि आतापर्यंत फक्त साइटच्या संपादकाने ते तपासले आहे; यात चुका असू शकतात.', 'ही साइट कशी तयार होते'),
    'ta': ('இந்த மொழிபெயர்ப்பு இயந்திரத்தின் உதவியுடன் செய்யப்பட்டது; இதுவரை தளத்தின் ஆசிரியர் மட்டுமே இதைச் சரிபார்த்துள்ளார். இதில் பிழைகள் இருக்கலாம்.', 'இந்தத் தளம் எப்படி உருவாகிறது'),
    'bn': ('এই অনুবাদ যন্ত্রের সাহায্যে তৈরি এবং এখনও পর্যন্ত শুধু সাইটের সম্পাদক এটি দেখেছেন; এতে ভুল থাকতে পারে।', 'এই সাইট কীভাবে তৈরি হয়'),
    'kn': ('ಈ ಅನುವಾದವನ್ನು ಯಂತ್ರದ ಸಹಾಯದಿಂದ ಮಾಡಲಾಗಿದೆ; ಇದುವರೆಗೆ ಸೈಟ್‌ನ ಸಂಪಾದಕರು ಮಾತ್ರ ಇದನ್ನು ಪರಿಶೀಲಿಸಿದ್ದಾರೆ. ಇದರಲ್ಲಿ ತಪ್ಪುಗಳು ಇರಬಹುದು.', 'ಈ ಸೈಟ್ ಹೇಗೆ ತಯಾರಾಗುತ್ತದೆ'),
    'ml': ('ഈ വിവർത്തനം യന്ത്രസഹായത്തോടെ തയ്യാറാക്കിയതാണ്; ഇതുവരെ സൈറ്റിന്റെ എഡിറ്റർ മാത്രമാണ് ഇത് പരിശോധിച്ചിട്ടുള്ളത്. ഇതിൽ തെറ്റുകൾ ഉണ്ടാകാം.', 'ഈ സൈറ്റ് എങ്ങനെ തയ്യാറാക്കുന്നു'),
}
FOOTER = re.compile(r'<footer\b.*?</footer>', re.S)
OLD = re.compile(r'\n?<p class="[a-z]+ tr-note"[^>]*>.*?</p>', re.S)


def add(html, lang):
    text, link = NOTICE[lang]
    note = '\n<p class="%s tr-note" style="margin-top:.5rem">%s <a href="/%s/about.html#made">%s</a></p>' % (lang, text, lang, link)
    m = FOOTER.search(html)
    if not m:
        return html
    foot = OLD.sub('', m.group(0))
    # after the footer's first paragraph in this language (the "translations are simplified" line)
    p = re.search(r'<p class="%s">.*?</p>' % lang, foot, re.S)
    if not p:
        return html
    foot = foot[:p.end()] + note + foot[p.end():]
    return html[:m.start()] + foot + html[m.end():]


def main():
    check = '--check' in sys.argv
    n = changed = 0
    for lang in NOTICE:
        for path in sorted(glob.glob(os.path.join(lang, '*.html'))):
            old = open(path, encoding='utf-8').read()
            new = add(old, lang)
            n += 1
            if 'tr-note' not in new:
                print('no place for the notice:', path)
            if new != old:
                changed += 1
                if not check:
                    open(path, 'w', encoding='utf-8').write(new)
    print('%d translated pages, %d changed' % (n, changed))


if __name__ == '__main__':
    main()
