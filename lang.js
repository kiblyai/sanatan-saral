(function(){
  var root=document.documentElement;
  function setLang(l){
    root.setAttribute('data-lang',l);
    root.setAttribute('lang',l==='hi'?'hi':(l==='gu'?'gu':'en'));
    document.querySelectorAll('.lang button').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-set')===l)});
    try{localStorage.setItem('sd-lang',l)}catch(err){}
  }
  var saved=null;
  try{saved=localStorage.getItem('sd-lang')}catch(err){}
  if(!saved){var nl=(navigator.language||'').toLowerCase();saved=nl.indexOf('hi')===0?'hi':(nl.indexOf('gu')===0?'gu':'en')}
  setLang(saved);
  document.querySelectorAll('.lang button').forEach(function(b){
    b.addEventListener('click',function(){setLang(b.getAttribute('data-set'))});
  });
})();

try{if(!location.hash){window.scrollTo(0,0)}}catch(e){}
