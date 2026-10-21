(function(){
  var root=document.documentElement;
  function setLang(l){
    root.setAttribute('data-lang',l);
    root.setAttribute('lang',l==='hi'?'hi':'en');
    var e=document.getElementById('btn-en'),h=document.getElementById('btn-hi');
    if(e)e.setAttribute('aria-pressed',l==='en');
    if(h)h.setAttribute('aria-pressed',l==='hi');
    try{localStorage.setItem('sd-lang',l)}catch(err){}
  }
  var saved=null;
  try{saved=localStorage.getItem('sd-lang')}catch(err){}
  if(!saved){saved=(navigator.language||'').toLowerCase().indexOf('hi')===0?'hi':'en'}
  setLang(saved);
  document.querySelectorAll('.lang button').forEach(function(b){
    b.addEventListener('click',function(){setLang(b.getAttribute('data-set'))});
  });
})();

try{if(!location.hash){window.scrollTo(0,0)}}catch(e){}
