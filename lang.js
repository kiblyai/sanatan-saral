(function(){
  var root=document.documentElement;
  /* Pages now carry one language each (data-page-lang on <html>). On those pages the language is fixed
     and the language buttons are links, handled by the small script in the page head. */
  var pageLang=root.getAttribute('data-page-lang');
  function setLang(l,keep){
    root.setAttribute('data-lang',l);
    root.setAttribute('lang',l==='hi'?'hi':(l==='gu'?'gu':(l==='te'?'te':(l==='mr'?'mr':(l==='ta'?'ta':(l==='bn'?'bn':(l==='kn'?'kn':(l==='ml'?'ml':'en'))))))));
    document.querySelectorAll('.lang button').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-set')===l)});
    if(keep!==false){try{localStorage.setItem('sd-lang',l)}catch(err){}}
  }
  if(pageLang){setLang(pageLang,false);return}
  var saved=null;
  try{saved=localStorage.getItem('sd-lang')}catch(err){}
  try{var ql=(new URLSearchParams(location.search).get('lang')||'').toLowerCase();if(['en','hi','gu','te','mr','ta','bn','kn','ml'].indexOf(ql)>=0)saved=ql}catch(err){}/*lang-param*/
  if(!saved){var nl=(navigator.language||'').toLowerCase();saved=nl.indexOf('hi')===0?'hi':(nl.indexOf('gu')===0?'gu':(nl.indexOf('te')===0?'te':(nl.indexOf('mr')===0?'mr':(nl.indexOf('ta')===0?'ta':(nl.indexOf('bn')===0?'bn':(nl.indexOf('kn')===0?'kn':(nl.indexOf('ml')===0?'ml':'en')))))))}
  setLang(saved);
  document.querySelectorAll('.lang button').forEach(function(b){
    b.addEventListener('click',function(){setLang(b.getAttribute('data-set'))});
  });
})();

try{if(!location.hash){window.scrollTo(0,0)}}catch(e){}

/* lang-fit: if the full language names do not fit the screen (large text settings, narrow windows), switch to short names */
(function(){function fit(){document.querySelectorAll('.hero>.lang').forEach(function(g){g.classList.remove('lang-short');if(g.scrollWidth>g.clientWidth+1)g.classList.add('lang-short')})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',fit);else fit();addEventListener('resize',fit);if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit)})();
