(function(){
  var root=document.documentElement;
  function setLang(l){
    root.setAttribute('data-lang',l);
    root.setAttribute('lang',l==='hi'?'hi':(l==='gu'?'gu':(l==='te'?'te':(l==='mr'?'mr':(l==='ta'?'ta':(l==='bn'?'bn':'en'))))));
    document.querySelectorAll('.lang button').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-set')===l)});
    try{localStorage.setItem('sd-lang',l)}catch(err){}
  }
  var saved=null;
  try{saved=localStorage.getItem('sd-lang')}catch(err){}
  if(!saved){var nl=(navigator.language||'').toLowerCase();saved=nl.indexOf('hi')===0?'hi':(nl.indexOf('gu')===0?'gu':(nl.indexOf('te')===0?'te':(nl.indexOf('mr')===0?'mr':(nl.indexOf('ta')===0?'ta':(nl.indexOf('bn')===0?'bn':'en')))))}
  setLang(saved);
  document.querySelectorAll('.lang button').forEach(function(b){
    b.addEventListener('click',function(){setLang(b.getAttribute('data-set'))});
  });
})();

try{if(!location.hash){window.scrollTo(0,0)}}catch(e){}
