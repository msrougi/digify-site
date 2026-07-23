(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* header state */
  var hdr = document.getElementById('hdr');
  var onScroll = function(){ hdr.classList.toggle('is-stuck', window.scrollY > 8); };
  onScroll();
  window.addEventListener('scroll', onScroll, {passive:true});

  /* mobile menu */
  var burger = document.getElementById('burger');
  burger.addEventListener('click', function(){
    var open = hdr.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
  });
  document.querySelectorAll('#mnav a').forEach(function(a){
    a.addEventListener('click', function(){
      hdr.classList.remove('is-open');
      burger.setAttribute('aria-expanded','false');
    });
  });

  /* scroll reveal */
  var items = document.querySelectorAll('.rv');
  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach(function(el){ el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, {rootMargin:'0px 0px -8% 0px', threshold:0.08});
    items.forEach(function(el){ io.observe(el); });
  }

  /* interruptor de tema */
  var root = document.documentElement, sw = document.getElementById('sw'), tc = document.getElementById('tc');
  var paint = function(t){
    root.setAttribute('data-theme', t);
    sw.setAttribute('aria-checked', t === 'light' ? 'true' : 'false');
    tc.setAttribute('content', t === 'light' ? '#FFFFFF' : '#0A0B0D');
  };
  paint(root.getAttribute('data-theme') || 'light');
  sw.addEventListener('click', function(){
    var t = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    paint(t);
    try{ localStorage.setItem('digify-theme', t); }catch(e){}
  });

  /* ---------- hero: slider de 3 atos ---------- */
  var hero   = document.getElementById('hero');
  var slides = [].slice.call(hero.querySelectorAll('.hslide'));
  var tabs   = [].slice.call(hero.querySelectorAll('.htab'));
  var rank   = document.getElementById('rank');
  var rows   = rank ? [].slice.call(rank.querySelectorAll('.rank__row')) : [];
  var DUR = 8000, timer = null, rankT = null, cur = 0;

  function settle(){
    rows.forEach(function(r){ r.style.setProperty('--slot', r.dataset.final); });
    rank.classList.add('is-ranked');
  }
  function climb(){
    if (!rank) return;
    clearTimeout(rankT);
    rank.classList.remove('is-ranked');
    rows.forEach(function(r){ r.style.setProperty('--slot', r.dataset.start); });
    void rank.offsetWidth;
    if (reduce) { settle(); return; }
    rankT = setTimeout(settle, 950);
  }

  function activate(i){
    cur = i;
    slides.forEach(function(sl, k){
      sl.classList.toggle('is-live', k === i);
      sl.setAttribute('aria-hidden', k === i ? 'false' : 'true');
    });
    tabs.forEach(function(tb, k){
      tb.classList.remove('is-live');
      tb.setAttribute('aria-selected', k === i ? 'true' : 'false');
      tb.setAttribute('tabindex', k === i ? '0' : '-1');
    });
    void tabs[i].offsetWidth;
    tabs[i].classList.add('is-live');
    if (i === 0) climb();
  }

  function play(){ stop(); timer = setInterval(function(){ activate((cur + 1) % slides.length); }, DUR); }
  function stop(){ if (timer) { clearInterval(timer); timer = null; } }
  function pause(){ stop(); hero.classList.add('is-paused'); }
  function resume(){ hero.classList.remove('is-paused'); play(); }

  tabs.forEach(function(tb, i){
    tb.addEventListener('click', function(){ activate(i); if (!hero.classList.contains('is-paused')) play(); });
  });
  hero.querySelector('.htabs').addEventListener('keydown', function(e){
    var d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1
          : e.key === 'ArrowLeft'  || e.key === 'ArrowUp'   ? -1 : 0;
    if (!d) return;
    e.preventDefault();
    var n = (cur + d + slides.length) % slides.length;
    activate(n); tabs[n].focus();
  });
  var strip = hero.querySelector('.htabs');
  strip.addEventListener('mouseenter', pause);
  strip.addEventListener('mouseleave', resume);
  hero.addEventListener('focusin', pause);
  hero.addEventListener('focusout', function(e){
    if (!hero.contains(e.relatedTarget)) resume();
  });
  document.addEventListener('visibilitychange', function(){ document.hidden ? stop() : play(); });

  climb();
  play();
})();
