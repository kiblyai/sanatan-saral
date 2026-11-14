"""Square (1080x1080) Gita Jayanti pictures for WhatsApp, one per language: python3 tools/share_squares.py og/share"""
import base64, os, sys
from playwright.sync_api import sync_playwright
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# fonts for the other scripts: npm i @fontsource/hind-guntur@5 @fontsource/hind-vadodara@5 @fontsource/hind-madurai@5
#   @fontsource/hind-siliguri@5 @fontsource/noto-sans-kannada@5 @fontsource/noto-sans-malayalam@5
FS=os.environ.get('FONTSOURCE', 'node_modules/@fontsource/')
OUT=sys.argv[1]
def f64(p): return base64.b64encode(open(p,'rb').read()).decode()
FONTS={
 'Corm': REPO+'/tools/og-fonts/cormorant-garamond-latin-600-normal.woff2',
 'Pop': REPO+'/tools/og-fonts/poppins-latin-500-normal.woff2',
 'PopDev': REPO+'/tools/og-fonts/poppins-devanagari-500-normal.woff2',
 'Tiro': REPO+'/tools/og-fonts/tiro-devanagari-hindi-devanagari-400-normal.woff2',
 'gu': FS+'hind-vadodara/files/hind-vadodara-gujarati-600-normal.woff2',
 'te': FS+'hind-guntur/files/hind-guntur-telugu-600-normal.woff2',
 'ta': FS+'hind-madurai/files/hind-madurai-tamil-600-normal.woff2',
 'bn': FS+'hind-siliguri/files/hind-siliguri-bengali-600-normal.woff2',
 'kn': FS+'noto-sans-kannada/files/noto-sans-kannada-kannada-600-normal.woff2',
 'ml': FS+'noto-sans-malayalam/files/noto-sans-malayalam-malayalam-600-normal.woff2',
}
FACE=''.join("@font-face{font-family:'%s';src:url(data:font/woff2;base64,%s) format('woff2')}"%(k,f64(v)) for k,v in FONTS.items())
T={
'en':('Gita Jayanti','Sunday, 20 December 2026','All 700 verses of the Bhagavad Gita, each with a simple translation','Read one chapter a day from 3 December','gita-jayanti.html'),
'hi':('गीता जयन्ती','रविवार, 20 दिसम्बर 2026','भगवद्गीता के सभी 700 श्लोक, सरल हिन्दी अनुवाद के साथ','3 दिसम्बर से रोज़ एक अध्याय पढ़ें','hi/gita-jayanti.html'),
'gu':('ગીતા જયંતી','રવિવાર, 20 ડિસેમ્બર 2026','ભગવદ્ગીતાના બધા 700 શ્લોક, સરળ ગુજરાતી અનુવાદ સાથે','3 ડિસેમ્બરથી રોજ એક અધ્યાય વાંચો','gu/gita-jayanti.html'),
'te':('గీతా జయంతి','ఆదివారం, 20 డిసెంబర్ 2026','భగవద్గీతలోని మొత్తం 700 శ్లోకాలు, సరళమైన తెలుగు అనువాదంతో','3 డిసెంబర్ నుండి రోజుకు ఒక అధ్యాయం చదవండి','te/gita-jayanti.html'),
'mr':('गीता जयंती','रविवार, 20 डिसेंबर 2026','भगवद्गीतेचे सर्व 700 श्लोक, सोप्या मराठी अनुवादासह','3 डिसेंबरपासून रोज एक अध्याय वाचा','mr/gita-jayanti.html'),
'ta':('கீதா ஜயந்தி','ஞாயிறு, 20 டிசம்பர் 2026','பகவத் கீதையின் 700 ஸ்லோகங்களும், எளிய தமிழ் மொழிபெயர்ப்புடன்','3 டிசம்பர் முதல் தினமும் ஒரு அத்தியாயம் படியுங்கள்','ta/gita-jayanti.html'),
'bn':('গীতা জয়ন্তী','রবিবার, ২০ ডিসেম্বর ২০২৬','ভগবদ্গীতার ৭০০টি শ্লোকই, সহজ বাংলা অনুবাদ সহ','৩ ডিসেম্বর থেকে রোজ একটি অধ্যায় পড়ুন','bn/gita-jayanti.html'),
'kn':('ಗೀತಾ ಜಯಂತಿ','ಭಾನುವಾರ, 20 ಡಿಸೆಂಬರ್ 2026','ಭಗವದ್ಗೀತೆಯ ಎಲ್ಲ 700 ಶ್ಲೋಕಗಳು, ಸರಳ ಕನ್ನಡ ಅನುವಾದದೊಂದಿಗೆ','3 ಡಿಸೆಂಬರ್‌ನಿಂದ ದಿನಕ್ಕೊಂದು ಅಧ್ಯಾಯ ಓದಿ','kn/gita-jayanti.html'),
'ml':('ഗീതാ ജയന്തി','ഞായർ, 20 ഡിസംബർ 2026','ഭഗവദ്ഗീതയിലെ 700 ശ്ലോകങ്ങളും, ലളിതമായ മലയാളം പരിഭാഷയോടെ','3 ഡിസംബർ മുതൽ ദിവസം ഒരു അധ്യായം വായിക്കൂ','ml/gita-jayanti.html'),
}
def fam(l):
    if l=='en': return "'Pop'"
    if l in ('hi','mr'): return "'PopDev','Pop'"
    return "'%s','Pop'"%l
def head(l):
    if l=='en': return "'Corm'"
    if l in ('hi','mr'): return "'Tiro','PopDev'"
    return "'%s','Pop'"%l
HTML='''<!doctype html><html><head><meta charset="utf-8"><style>%(face)s
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1080px;overflow:hidden;background:#F6F1E7;font-family:%(fam)s;color:#24343A}
.card{position:absolute;inset:40px;border:3px solid #B08D57;border-radius:28px;background:linear-gradient(180deg,#FBF7EF 0%%,#F1E8D8 100%%);
display:flex;flex-direction:column;align-items:center;text-align:center;padding:64px 70px 56px}
.skt{font-family:'Tiro';font-size:40px;color:#8A6A3A;letter-spacing:1px}
.ring{width:220px;height:220px;border-radius:50%%;border:4px solid #B08D57;display:flex;align-items:center;justify-content:center;margin:34px 0 30px;background:#fff8}
.ring b{font-family:'Corm';font-size:120px;color:#3C6C72;line-height:1}
.ring small{display:block;font-family:%(fam)s;font-size:%(vs)spx;white-space:nowrap;color:#8A6A3A;margin-top:4px}
h1{font-family:%(head)s;font-size:%(h1)spx;line-height:1.15;color:#3C6C72;font-weight:600}
.date{font-size:40px;margin-top:18px;color:#8A4B2A;font-weight:600}
.rule{width:140px;height:3px;background:#B08D57;margin:34px 0}
.msg{font-size:%(msg)spx;line-height:1.45;max-width:860px}
.sub{font-size:%(sub)spx;max-width:820px;line-height:1.35;margin-top:22px;color:#3C6C72}
.url{margin-top:auto;padding-top:24px;font-family:'Pop';font-size:30px;color:#24343A;letter-spacing:.5px}
.url span{color:#8A6A3A}
</style></head><body><div class="card">
<div class="skt">श्रीमद्भगवद्गीता</div>
<div class="ring"><div><b>700</b><small>%(verses)s</small></div></div>
<h1>%(t)s</h1><div class="date">%(d)s</div><div class="rule"></div>
<div class="msg">%(m)s</div><div class="sub">%(s)s</div>
<div class="url">sanatan.space/<span>%(u)s</span></div>
</div></body></html>'''
VERSES={'en':'verses','hi':'श्लोक','mr':'श्लोक','gu':'શ્લોક','te':'శ్లోకాలు','ta':'ஸ்லோகங்கள்','bn':'শ্লোক','kn':'ಶ್ಲೋಕಗಳು','ml':'ശ്ലോകങ്ങൾ'}
os.makedirs(OUT,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1080},device_scale_factor=1)
    for l,(t,d,m,s,u) in T.items():
        num='৭০০' if l=='bn' else '700'
        html=HTML%dict(face=FACE,fam=fam(l),head=head(l),h1=110 if l=='en' else 96,msg=44 if len(m)<60 else 40,vs=26 if len(VERSES[l])<7 else 21,sub=32 if len(s)<38 else 29,t=t,d=d,m=m,s=s,u=u,verses=VERSES[l])
        html=html.replace('<b>700</b>','<b>%s</b>'%num)
        pg.set_content(html); pg.wait_for_timeout(300)
        h=pg.evaluate("document.querySelector('.card').scrollHeight>document.querySelector('.card').clientHeight")
        pg.screenshot(path=os.path.join(OUT,'gita-jayanti-%s.png'%l))
        print(l,'overflow' if h else 'ok')
    b.close()
