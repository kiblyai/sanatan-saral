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

/* lang-menu: on phones the language bar shows only the current language; tapping it opens the full list */
(function(){var mq=window.matchMedia('(max-width:560px)'),pop=null;
function close(){if(pop){pop.remove();pop=null}}
document.addEventListener('click',function(e){
  var b=e.target.closest?e.target.closest('.lang button[data-set]'):null;
  var cur=document.documentElement.getAttribute('data-lang');
  if(b&&b.getAttribute('data-set')===cur){
    if(b.closest('.lang-pop')||pop){close();return}
    if(!mq.matches)return;
    var r=b.getBoundingClientRect();
    pop=document.createElement('div');pop.className='lang lang-pop';pop.setAttribute('role','group');pop.setAttribute('aria-label','Language');
    Array.prototype.forEach.call(b.closest('.lang').querySelectorAll('button[data-set]'),function(x){var c=x.cloneNode(true);c.removeAttribute('id');c.setAttribute('aria-pressed',c.getAttribute('data-set')===cur);pop.appendChild(c)});
    document.body.appendChild(pop);
    pop.style.top=(r.bottom+6)+'px';pop.style.right=Math.max(8,window.innerWidth-r.right)+'px';
    return}
  if(pop&&!(b&&b.closest('.lang-pop')))close();
});
addEventListener('scroll',close,{passive:true});addEventListener('resize',close);
document.addEventListener('keydown',function(e){if(e.key==='Escape')close()});
})();
