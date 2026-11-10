(function(){
  function lang(){return document.documentElement.getAttribute('data-lang')||'en'}
  function hi(){return lang()==='hi'}
  function inLang(box){
    if(!box) return null;
    return box.querySelector('.'+lang())||box.querySelector('.en')||box;
  }
  function pick(el,sel){var x=inLang(el.querySelector(sel)); return x?x.textContent.trim():''}
  function verseUrl(card,wa){
    var id=card.id||'';
    if(!id){var sec=card.closest('section'),a=sec&&sec.querySelector('#votd-link');if(a)id=(a.getAttribute('href')||'').split('#')[1]||''}
    if(!id) return location.origin+location.pathname;
    var slug=id.replace(/^v-/,''), q=[], L=lang(), dir='';
    if(/^(hi|gu|te|mr|ta|bn)$/.test(L)) dir=L+'/'; else if(L!=='en') q.push('lang='+L);
    if(wa) q.push('utm_source=whatsapp','utm_medium=share','utm_campaign=verse');
    return 'https://sanatan.space/'+dir+slug+'.html'+(q.length?'?'+q.join('&'):'');
  }
  function verseText(card,wa){
    var title=pick(card,'.v-head h3'), ref=pick(card,'.src');
    var skt=Array.prototype.map.call(card.querySelectorAll('.skt'),function(p){return p.innerText.trim()}).join('\n');
    var trs=function(c){return Array.prototype.filter.call(card.querySelectorAll('div > p.'+c),function(p){
      return !p.closest('.simple') && !p.closest('details') && !p.querySelector('a.more');
    }).map(function(p){return p.textContent.trim()}).join(' ')};
    var tr=trs(lang())||trs('en');
    return title+'\n\n'+skt+'\n\n'+tr+'\n\n— '+ref+' · Sanatan Dharma Saral\n'+verseUrl(card,wa);
  }
  function toast(btn,msg){
    var old=btn.getAttribute('data-label')||btn.innerHTML; btn.setAttribute('data-label',old);
    btn.textContent=msg; setTimeout(function(){btn.innerHTML=old},1600);
  }
  document.addEventListener('click',function(e){
    var wa=e.target.closest('.share-wa');
    if(wa){var c=wa.closest('.verse'); if(c) wa.href='https://wa.me/?text='+encodeURIComponent(verseText(c,true)); return}
    var cp=e.target.closest('.share-copy');
    if(cp){
      var card=cp.closest('.verse'); if(!card) return;
      var t=verseText(card,false);
      var done=function(){toast(cp,hi()?'कॉपी हो गया':'Copied ✓')};
      var fail=function(){
        var ta=document.createElement('textarea'); ta.value=t; ta.setAttribute('readonly','');
        ta.style.cssText='width:100%;min-height:8rem;margin-top:.5rem;font:inherit';
        cp.parentNode.after(ta); ta.focus(); ta.select();
        toast(cp,hi()?'चुने हुए पाठ को कॉपी करें':'Select and copy the text below');
      };
      try{navigator.clipboard.writeText(t).then(done,fail)}catch(err){fail()}
    }
  });
})();
