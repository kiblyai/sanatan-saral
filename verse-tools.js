/* Verse tools: Save (bookmark) and Picture card, plus text size. Per-viewer data stays in this browser. */
(function(){
  var SKEY='sd-saved', ZKEY='sd-size';
  function L(){return document.documentElement.getAttribute('data-lang')==='hi'?1:0}
  function load(k){try{return JSON.parse(localStorage.getItem(k)||'{}')}catch(e){return {}}}
  function store(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
  function pageName(){var p=location.pathname.split('/').pop()||'index.html';return p.indexOf('.html')<0?'index.html':p}
  function txt(el){return el?el.textContent.replace(/\s+/g,' ').trim():''}
  function both(card,sel){var b=card.querySelector(sel);if(!b)return['',''];return[txt(b.querySelector('.en'))||txt(b),txt(b.querySelector('.hi'))||txt(b)]}
  function verseData(card){
    var trDiv=Array.prototype.find.call(card.children,function(d){return d.tagName==='DIV'&&!d.classList.contains('simple')&&!d.classList.contains('v-head')&&d.querySelector('.label')});
    var tr=['',''];
    if(trDiv){tr=[Array.prototype.map.call(trDiv.querySelectorAll('p.en'),txt).filter(function(s){return s.indexOf('→')<0}).join(' '),
                 Array.prototype.map.call(trDiv.querySelectorAll('p.hi'),txt).filter(function(s){return s.indexOf('→')<0}).join(' ')]}
    return {key:pageName()+'#'+card.id,t:both(card,'.v-head h3'),r:both(card,'.src'),
      skt:Array.prototype.map.call(card.querySelectorAll('.skt'),function(p){return p.innerText.trim()}).join('\n'),tr:tr,at:Date.now()};
  }
  /* ---------- save ---------- */
  function paintSaved(){
    var s=load(SKEY);
    document.querySelectorAll('.v-save').forEach(function(b){
      var c=b.closest('.verse'); var on=c&&!!s[pageName()+'#'+c.id];
      b.classList.toggle('on',on); b.setAttribute('aria-pressed',on);
      b.innerHTML=on?'<span class="en">★ Saved</span><span class="hi">★ सहेजा</span>':'<span class="en">☆ Save</span><span class="hi">☆ सहेजें</span>';
    });
  }
  /* ---------- picture card ---------- */
  function wrap(ctx,text,max){var words=text.split(/\s+/),lines=[],cur='';words.forEach(function(w){var t=cur?cur+' '+w:w;if(ctx.measureText(t).width>max&&cur){lines.push(cur);cur=w}else cur=t});if(cur)lines.push(cur);return lines}
  async function makeCard(d){
    var W=1080,H=1350,c=document.createElement('canvas');c.width=W;c.height=H;var x=c.getContext('2d');
    try{await Promise.all(['500 54px "Tiro Devanagari Sanskrit"','600 44px "Cormorant Garamond"','400 34px Nunito','400 34px Poppins'].map(function(f){return document.fonts.load(f,'ॐ अ A')}))}catch(e){}
    var g=x.createLinearGradient(0,0,W,H);g.addColorStop(0,'#D8E8E2');g.addColorStop(.55,'#E4E3F0');g.addColorStop(1,'#F4EDE1');x.fillStyle=g;x.fillRect(0,0,W,H);
    var rg=x.createRadialGradient(W*.85,H*.92,10,W*.85,H*.92,520);rg.addColorStop(0,'rgba(126,106,58,.22)');rg.addColorStop(1,'rgba(126,106,58,0)');x.fillStyle=rg;x.fillRect(0,0,W,H);
    x.fillStyle='#7E6A3A';x.textAlign='center';x.font='400 86px "Tiro Devanagari Sanskrit", serif';x.fillText('ॐ',W/2,170);
    x.strokeStyle='rgba(126,106,58,.45)';x.lineWidth=2;x.beginPath();x.moveTo(W/2-120,215);x.lineTo(W/2+120,215);x.stroke();
    var l=L();
    x.font='400 64px "Tiro Devanagari Sanskrit", serif';
    var sl=[];d.skt.split('\n').slice(0,6).forEach(function(line){wrap(x,line,W-150).forEach(function(s){sl.push(s)})});
    x.font=(l?'400 46px Poppins, sans-serif':'400 50px Nunito, sans-serif');
    var tl=wrap(x,d.tr[l]||d.tr[0],W-180); if(tl.length>8){tl=tl.slice(0,8);tl[7]=tl[7].replace(/\s+\S*$/,'')+' …'}
    var total=sl.length*96+90+tl.length*70, y=Math.max(300,(H-total)/2+40);
    x.fillStyle='#20363A';x.font='400 64px "Tiro Devanagari Sanskrit", serif';
    sl.forEach(function(s){x.fillText(s,W/2,y);y+=96});
    y+=10;x.fillStyle='rgba(32,54,58,.25)';x.fillRect(W/2-40,y-30,80,3);y+=60;
    x.fillStyle='#3C6C72';x.font=(l?'400 46px Poppins, sans-serif':'400 50px Nunito, sans-serif');
    tl.forEach(function(s){x.fillText(s,W/2,y);y+=70});
    x.fillStyle='#83672C';x.font='600 46px "Cormorant Garamond", serif';x.fillText(d.r[l]||d.r[0],W/2,H-140);
    x.fillStyle='#566B6D';x.font='400 30px Nunito, sans-serif';x.fillText('Sanatan Dharma Saral · सनातन धर्म सरल',W/2,H-90);
    return c;
  }
  var modal=null;
  function showModal(canvas,d){
    if(!modal){modal=document.createElement('div');modal.className='vt-modal';modal.innerHTML='<div class="vt-box" role="dialog" aria-modal="true" aria-label="Verse picture"><img alt=""><p class="vt-hint"></p><div class="vt-row"><button type="button" class="vt-save"></button><button type="button" class="vt-close"></button></div></div>';document.body.appendChild(modal);
      modal.addEventListener('click',function(e){if(e.target===modal||e.target.classList.contains('vt-close'))modal.hidden=true});}
    var l=L(),url=canvas.toDataURL('image/png');
    modal.querySelector('img').src=url; modal.querySelector('img').alt=d.t[l];
    modal.querySelector('.vt-close').textContent=l?'बन्द करें':'Close';
    var sv=modal.querySelector('.vt-save'); sv.textContent=l?'चित्र सहेजें':'Save picture'; sv.hidden=false;
    modal.querySelector('.vt-hint').textContent=l?'चित्र को दबाकर रखें और सहेजें या भेजें।':'Press and hold the picture to save or share it.';
    sv.onclick=async function(){
      try{var dl=window.claude&&claude.use?await claude.use('downloads'):null;
        if(!dl){sv.hidden=true;return}
        var blob=await new Promise(function(r){canvas.toBlob(r,'image/png')});
        await dl.save({filename:(d.r[0]||'verse').replace(/[^\w.-]+/g,'-')+'.png',data:blob});
        sv.textContent=l?'सहेजा गया ✓':'Saved ✓';
      }catch(e){if(e&&e.code==='declined')return; sv.hidden=true}
    };
    modal.hidden=false;
  }
  document.addEventListener('click',async function(e){
    var b=e.target.closest('.v-save');
    if(b){var c=b.closest('.verse');if(!c)return;var s=load(SKEY),d=verseData(c);if(s[d.key])delete s[d.key];else s[d.key]=d;store(SKEY,s);paintSaved();return}
    var im=e.target.closest('.v-img');
    if(im){var c2=im.closest('.verse');if(!c2)return;im.disabled=true;try{var d2=verseData(c2);showModal(await makeCard(d2),d2)}finally{im.disabled=false}}
    var z=e.target.closest('[data-size]');
    if(z&&z.tagName==='BUTTON'){setSize(z.dataset.size)}
  });
  /* ---------- text size ---------- */
  function setSize(sz){document.documentElement.setAttribute('data-size',sz);store(ZKEY,{s:sz});
    document.querySelectorAll('button[data-size]').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.size===sz)})}
  setSize((load(ZKEY).s)||'m');
  paintSaved();
  document.querySelectorAll('.lang button').forEach(function(b){b.addEventListener('click',function(){setTimeout(paintSaved,0)})});
})();

/* Print: a button in the top bar, a link in the footer, and print-friendly styles. */
(function(){
  var css='.print-btn{flex-shrink:0;display:inline-flex;align-items:center;gap:.3rem;font:inherit;font-size:.92rem;color:var(--ink,#20363A);background:var(--paper,#fff);border:1.5px solid var(--line,#ccd);border-radius:99px;padding:.26rem .7rem;cursor:pointer;white-space:nowrap}'+
  '.print-btn:hover{border-color:var(--indigo,#3C6C72)}.print-btn svg{width:16px;height:16px}'+
  '@media (max-width:560px){.print-btn .pl{display:none}.print-btn{padding:.3rem .5rem;order:3}}'+
  '.print-foot{margin:.6rem 0}.print-foot a{cursor:pointer}'+
  '.print-only{display:none}'+
  '@media print{'+
   '@page{margin:16mm 14mm}'+
   'html,body{background:#fff!important;color:#111!important}'+
   '.bar,.topnav,.menu,.lang,.print-btn,.print-foot,.listen,.conn,.v-save,.v-img,.vt-modal,.share,.chat,.ask-box,form,nav,button,.toc,div[style*="space-between"]:has(> a.more),p:has(> a.more:only-child),.read-btn,[data-read-id],.no-print{display:none!important}'+
   '*{box-shadow:none!important;text-shadow:none!important;animation:none!important;transition:none!important}'+
   '.hero{background:none!important;padding:0 0 8mm!important;color:#111!important}'+
   '.verse,.card,figure,table,.tldr{break-inside:avoid;page-break-inside:avoid;background:#fff!important;border-color:#bbb!important}'+
   'h1,h2,h3{break-after:avoid;color:#111!important}'+
   'a{color:#111!important;text-decoration:none!important}'+
   '.wrap{max-width:none!important}'+
   '.print-only{display:block!important;font-size:10pt;color:#555!important;border-top:1px solid #bbb;margin-top:8mm;padding-top:3mm}'+
  '}';
  var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
  var ic='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9V3h12v6"/><rect x="3" y="9" width="18" height="8" rx="2"/><path d="M6 14h12v7H6z"/></svg>';
  var opened=[];
  function doPrint(){window.print()}
  window.addEventListener('beforeprint',function(){opened=[];document.querySelectorAll('main details:not([open])').forEach(function(d){d.open=true;opened.push(d)})});
  window.addEventListener('afterprint',function(){opened.forEach(function(d){d.open=false});opened=[]});
  var bar=document.querySelector('.bar .wrap');
  if(bar){var b=document.createElement('button');b.type='button';b.className='print-btn';b.setAttribute('aria-label','Print this page');
    b.innerHTML=ic+'<span class="pl"><span class="en">Print</span><span class="hi">प्रिंट</span></span>';b.addEventListener('click',doPrint);
    var lang=bar.querySelector('.lang');bar.insertBefore(b,lang||null)}
  var foot=document.querySelector('footer');
  if(foot){var p=document.createElement('p');p.className='print-foot';
    p.innerHTML='<a role="button" tabindex="0">'+'<span class="en">🖨 Print this page</span><span class="hi">🖨 यह पृष्ठ प्रिंट करें</span></a>';
    var a=p.querySelector('a');a.addEventListener('click',doPrint);a.addEventListener('keydown',function(e){if(e.key==='Enter')doPrint()});
    foot.insertBefore(p,foot.firstChild);
    var po=document.createElement('p');po.className='print-only';
    po.textContent='Sanatan Dharma Saral · सनातन धर्म सरल — '+location.href.replace(/^https?:\/\//,'').split('#')[0];
    foot.appendChild(po)}
})();

/* Read aloud with the device's own voice (Sanskrit, then the meaning). Pronunciation depends on the phone. */
(function(){
  if(!('speechSynthesis' in window))return;
  var synth=window.speechSynthesis, current=null, toastShown=false;
  function L(){return document.documentElement.getAttribute('data-lang')==='hi'?1:0}
  function pick(langs){var vs=synth.getVoices();for(var i=0;i<langs.length;i++){var v=vs.find(function(x){return x.lang&&x.lang.replace('_','-').toLowerCase().indexOf(langs[i])===0});if(v)return v}return null}
  function clean(t){return t.replace(/[।॥|]+/g,'. ').replace(/[०-९0-9]+/g,' ').replace(/\s+/g,' ').trim()}
  function label(b,on){b.innerHTML=on?'<span class="en">■ Stop</span><span class="hi">■ रोकें</span>':'<span class="en">🔊 Read aloud</span><span class="hi">🔊 सुनाएँ</span>';b.setAttribute('aria-pressed',on)}
  function toast(){if(toastShown)return;toastShown=true;var t=document.createElement('div');t.className='ra-toast';t.setAttribute('role','status');
    t.innerHTML='<span class="en">Using your phone\'s voice. Sanskrit pronunciation may not be exact; learn chanting from a teacher.</span><span class="hi">आपके फ़ोन की आवाज़ से। संस्कृत उच्चारण पूरी तरह सही न भी हो; पाठ किसी गुरु से सीखें।</span>';
    document.body.appendChild(t);setTimeout(function(){t.remove()},6000)}
  function stop(){synth.cancel();if(current){label(current,false);current=null}}
  function speak(btn){
    var card=btn.closest('.verse');if(!card)return;
    if(current===btn){stop();return}
    stop();current=btn;label(btn,true);toast();
    var skt=Array.prototype.map.call(card.querySelectorAll('.skt'),function(p){return p.innerText}).join(' ');
    var trDiv=Array.prototype.find.call(card.children,function(d){return d.tagName==='DIV'&&!d.classList.contains('simple')&&d.querySelector('.label')});
    var l=L(), tr='';
    if(trDiv)tr=Array.prototype.map.call(trDiv.querySelectorAll(l?'p.hi':'p.en'),function(p){return p.textContent}).filter(function(s){return s.indexOf('→')<0}).join(' ');
    var parts=[[clean(skt),['sa','hi','mr','ne'],.82],[tr,l?['hi']:['en-in','en'],.95]];
    var queue=parts.filter(function(p){return p[0]}).map(function(p){var u=new SpeechSynthesisUtterance(p[0]);var v=pick(p[1]);if(v){u.voice=v;u.lang=v.lang}else{u.lang=p[1][0]==='sa'?'hi-IN':(l?'hi-IN':'en-IN')}u.rate=p[2];return u});
    if(!queue.length){stop();return}
    queue[queue.length-1].onend=function(){if(current===btn){label(btn,false);current=null}};
    queue.forEach(function(u){u.onerror=function(){if(current===btn){label(btn,false);current=null}};synth.speak(u)});
  }
  var st=document.createElement('style');
  st.textContent='.listen .v-say{font:inherit;font-size:.9rem;border:0;background:none;padding:0;color:var(--ink-2);cursor:pointer}.listen .v-say:hover,.listen .v-say[aria-pressed="true"]{color:var(--kumkum)}'+
    '.ra-toast{position:fixed;left:50%;bottom:max(16px,env(safe-area-inset-bottom));transform:translateX(-50%);z-index:70;max-width:min(92vw,440px);background:var(--ink,#20363A);color:var(--paper,#fff);padding:.65rem 1rem;border-radius:14px;font-size:.88rem;box-shadow:0 8px 24px rgba(0,0,0,.2)}'+
    '@media print{.v-say,.ra-toast{display:none!important}}';
  document.head.appendChild(st);
  document.querySelectorAll('.verse .listen').forEach(function(row){
    if(row.querySelector('.v-say'))return;
    var b=document.createElement('button');b.type='button';b.className='v-say';label(b,false);
    b.title='Uses your device voice';
    row.insertBefore(b,row.firstChild);
  });
  document.addEventListener('click',function(e){var b=e.target.closest('.v-say');if(b)speak(b)});
  if(synth.onvoiceschanged!==undefined)synth.onvoiceschanged=function(){};
  addEventListener('pagehide',stop);
})();

/* Tap a word: turns each verse's word-by-word list into tappable Sanskrit words. */
(function(){
  function L(){return document.documentElement.getAttribute('data-lang')==='hi'?1:0}
  var st=document.createElement('style');
  st.textContent='.wbw{margin:.2rem 0 .6rem}.wbw-h{font-size:.74rem;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:var(--gold);margin:0 0 .35rem}'+
   '.wbw-row{display:flex;flex-wrap:wrap;gap:.3rem}.wbw-row button{font:inherit;font-family:var(--f-skt,"Tiro Devanagari Sanskrit",serif);font-size:1.05rem;line-height:1.3;border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:10px;padding:.12rem .55rem;cursor:pointer}'+
   '.wbw-row button[aria-pressed="true"]{background:var(--indigo);border-color:var(--indigo);color:var(--paper)}'+
   '.wbw-out{margin:.45rem 0 0;padding:.55rem .8rem;border-radius:12px;background:var(--paper-2);font-size:.98rem;min-height:2.4rem}.wbw-out b{font-family:var(--f-skt,"Tiro Devanagari Sanskrit",serif);font-weight:400;font-size:1.1rem;margin-right:.4rem}'+
   '.wbw-all{font:inherit;font-size:.85rem;border:0;background:none;color:var(--ink-2);text-decoration:underline;cursor:pointer;padding:0;margin-top:.35rem}'+
   '.verse details.words.wbw-src{display:none}.verse details.words.wbw-src.wbw-show{display:block}'+
   '@media print{.wbw{display:none!important}.verse details.words.wbw-src{display:block!important}}';
  document.head.appendChild(st);
  document.querySelectorAll('.verse details.words').forEach(function(d){
    var dts=d.querySelectorAll('dt'); if(!dts.length)return;
    var box=document.createElement('div'); box.className='wbw';
    box.innerHTML='<p class="wbw-h"><span class="en">Tap a word for its meaning</span><span class="hi">अर्थ जानने के लिए शब्द छुएँ</span></p><div class="wbw-row"></div><p class="wbw-out" aria-live="polite"><span class="en">Tap any Sanskrit word above.</span><span class="hi">ऊपर किसी भी संस्कृत शब्द को छुएँ।</span></p><button type="button" class="wbw-all"><span class="en">Show the full word list</span><span class="hi">पूरी शब्द-सूची दिखाएँ</span></button>';
    var row=box.querySelector('.wbw-row'), out=box.querySelector('.wbw-out');
    dts.forEach(function(dt){
      var dd=dt.nextElementSibling; var b=document.createElement('button'); b.type='button'; b.textContent=dt.textContent; b.setAttribute('aria-pressed','false');
      b.addEventListener('click',function(){
        row.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed','false')}); b.setAttribute('aria-pressed','true');
        var en=dd&&dd.querySelector('.en'), hi=dd&&dd.querySelector('.hi');
        out.innerHTML='<b></b><span class="en"></span><span class="hi"></span>';
        out.querySelector('b').textContent=dt.textContent;
        out.querySelector('.en').textContent=(en?en.textContent:(dd?dd.textContent:''));
        out.querySelector('.hi').textContent=(hi?hi.textContent:(dd?dd.textContent:''));
      });
      row.appendChild(b);
    });
    box.querySelector('.wbw-all').addEventListener('click',function(){d.classList.toggle('wbw-show');d.open=d.classList.contains('wbw-show')});
    d.classList.add('wbw-src');
    d.parentNode.insertBefore(box,d);
  });
})();

/* Report a mistake: links each verse to the contact page with the reference filled in. */
(function(){
  document.querySelectorAll('.verse .listen').forEach(function(row){
    if(row.querySelector('.v-report'))return;
    var card=row.closest('.verse'), src=card&&card.querySelector('.src .en');
    var ref=(src?src.textContent.trim():'')+(card&&card.id?' ('+(location.pathname.split('/').pop()||'index.html')+'#'+card.id+')':'');
    var a=document.createElement('a'); a.className='v-report'; a.href='contact.html?topic=correction&ref='+encodeURIComponent(ref);
    a.innerHTML='<span class="en">⚑ Report a mistake</span><span class="hi">⚑ त्रुटि बताएँ</span>';
    row.appendChild(a);
  });
  var st=document.createElement('style');st.textContent='.listen .v-report{font-size:.9rem;color:var(--ink-2);text-decoration:none}.listen .v-report:hover{color:var(--kumkum)}@media print{.v-report{display:none!important}}';document.head.appendChild(st);
})();
