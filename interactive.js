/* Tap-to-learn diagrams and maps: any .tip inside an .ix fills that figure's .ix-panel. */
(function(){
  function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;')}
  function show(tip){
    var ix=tip.closest('.ix'); if(!ix) return;
    var panel=ix.querySelector('.ix-panel'); if(!panel) return;
    ix.querySelectorAll('.tip.on').forEach(function(t){t.classList.remove('on');t.setAttribute('aria-pressed','false')});
    tip.classList.add('on'); tip.setAttribute('aria-pressed','true');
    var d=tip.dataset;
    panel.innerHTML='<b><span class="en'+(d.tgu?' xg':'')+'">'+esc(d.ten)+'</span><span class="hi">'+esc(d.thi||d.ten)+'</span>'+(d.tgu?'<span class="gu">'+esc(d.tgu)+'</span>':'')+'</b>'+
      '<span class="en'+(d.igu?' xg':'')+'">'+esc(d.ien)+'</span><span class="hi">'+esc(d.ihi||d.ien)+'</span>'+(d.igu?'<span class="gu">'+esc(d.igu)+'</span>':'');
  }
  document.querySelectorAll('.ix .tip').forEach(function(t){
    t.setAttribute('tabindex','0'); t.setAttribute('role','button'); t.setAttribute('aria-pressed','false');
    t.addEventListener('click',function(e){e.preventDefault();show(t)});
    t.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();show(t)}});
  });
  document.querySelectorAll('.ix').forEach(function(ix){var f=ix.querySelector('.tip'); if(f) show(f)});

  /* Per-viewer reading progress (Gita chapters etc.) */
  var KEY='sd-read';
  function load(){try{return JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){return {}}}
  function save(o){try{localStorage.setItem(KEY,JSON.stringify(o))}catch(e){}}
  var read=load();
  function paint(){
    document.querySelectorAll('[data-read-id]').forEach(function(b){
      var on=!!read[b.dataset.readId]; b.classList.toggle('done',on); b.setAttribute('aria-pressed',on);
    });
    document.querySelectorAll('[data-read-group]').forEach(function(bar){
      var g=bar.dataset.readGroup, ids=bar.dataset.readIds.split(','), n=ids.filter(function(i){return read[i]}).length;
      var fill=bar.querySelector('.rp-fill'), lbl=bar.querySelector('.rp-count');
      if(fill) fill.style.width=(n/ids.length*100)+'%';
      if(lbl) lbl.textContent=n+' / '+ids.length;
    });
    document.querySelectorAll('.chmap a[href^="#ch"]').forEach(function(a){
      a.classList.toggle('done',!!read['gita-'+a.getAttribute('href').slice(1)]);
    });
  }
  document.addEventListener('click',function(e){
    var b=e.target.closest('[data-read-id]'); if(!b) return;
    var id=b.dataset.readId; if(read[id]) delete read[id]; else read[id]=1; save(read); paint();
  });
  paint();
})();

/* close the All pages menu when tapping outside it or choosing a link */
(function(){
  document.addEventListener('click',function(e){
    document.querySelectorAll('details.menu[open]').forEach(function(m){
      if(!m.contains(e.target)||e.target.closest('.menu-panel a'))m.removeAttribute('open');
    });
  });
  document.addEventListener('keydown',function(e){if(e.key==='Escape')document.querySelectorAll('details.menu[open]').forEach(function(m){m.removeAttribute('open')})});
})();
