(function(){
  function hi(){return document.documentElement.getAttribute('data-lang')==='hi'}
  function pick(el,sel){
    var box=el.querySelector(sel); if(!box) return '';
    var x=box.querySelector(hi()?'.hi':'.en'); return (x||box).textContent.trim();
  }
  function verseText(card){
    var title=pick(card,'.v-head h3'), ref=pick(card,'.src');
    var skt=Array.prototype.map.call(card.querySelectorAll('.skt'),function(p){return p.innerText.trim()}).join('\n');
    var tr=Array.prototype.filter.call(card.querySelectorAll('div > p.'+(hi()?'hi':'en')),function(p){
      return !p.closest('.simple') && !p.closest('details');
    }).map(function(p){return p.textContent.trim()}).join(' ');
    return title+'\n\n'+skt+'\n\n'+tr+'\n\n— '+ref+' · Sanatan Dharma Saral';
  }
  function toast(btn,msg){
    var old=btn.getAttribute('data-label')||btn.innerHTML; btn.setAttribute('data-label',old);
    btn.textContent=msg; setTimeout(function(){btn.innerHTML=old},1600);
  }
  document.addEventListener('click',function(e){
    var wa=e.target.closest('.share-wa');
    if(wa){var c=wa.closest('.verse'); if(c) wa.href='https://wa.me/?text='+encodeURIComponent(verseText(c)); return}
    var cp=e.target.closest('.share-copy');
    if(cp){
      var card=cp.closest('.verse'); if(!card) return;
      var t=verseText(card);
      var done=function(){toast(cp,hi()?'कॉपी हो गया':'Copied')};
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
