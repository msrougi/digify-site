// ── CURSOR CUSTOM ──
const cursor = document.querySelector('.cursor');
const ring   = document.querySelector('.cursor-ring');
if (cursor && ring) {
  let mx=0,my=0,rx=0,ry=0;
  document.addEventListener('mousemove', e => { mx=e.clientX; my=e.clientY; });
  const animCursor = () => {
    cursor.style.left = mx+'px'; cursor.style.top = my+'px';
    rx += (mx-rx)*0.14; ry += (my-ry)*0.14;
    ring.style.left = rx+'px'; ring.style.top = ry+'px';
    requestAnimationFrame(animCursor);
  };
  animCursor();
  document.querySelectorAll('a,button,.btn,.svc-row,.client-tag,.process-card').forEach(el=>{
    el.addEventListener('mouseenter',()=>{
      cursor.style.width='20px'; cursor.style.height='20px';
      ring.style.width='56px'; ring.style.height='56px';
    });
    el.addEventListener('mouseleave',()=>{
      cursor.style.width='10px'; cursor.style.height='10px';
      ring.style.width='36px'; ring.style.height='36px';
    });
  });
}

// ── NAV SCROLL ──
const nav = document.querySelector('.site-nav');
if (nav) {
  window.addEventListener('scroll', ()=>nav.classList.toggle('scrolled', scrollY>60), {passive:true});
}

// ── MOBILE MENU ──
const hamburger = document.querySelector('.nav-hamburger');
const mobileMenu = document.querySelector('.mobile-menu');
if (hamburger && mobileMenu) {
  hamburger.addEventListener('click', ()=>mobileMenu.classList.toggle('open'));
  mobileMenu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>mobileMenu.classList.remove('open')));
}

// ── SMOOTH SCROLL ──
document.querySelectorAll('a[href^="#"]').forEach(a=>{
  a.addEventListener('click', e=>{
    const t=document.querySelector(a.getAttribute('href'));
    if(t){e.preventDefault();t.scrollIntoView({behavior:'smooth',block:'start'});}
  });
});

// ── REVEAL ON SCROLL ──
const revealObserver = new IntersectionObserver(entries=>{
  entries.forEach(e=>{
    if(e.isIntersecting){
      e.target.classList.add('visible');
      revealObserver.unobserve(e.target);
    }
  });
},{threshold:0.1,rootMargin:'0px 0px -40px 0px'});
document.querySelectorAll('.reveal').forEach((el,i)=>{
  el.style.transitionDelay = (i%4)*0.08+'s';
  revealObserver.observe(el);
});

// ── COUNTER ──
function animCounter(el){
  const target=parseInt(el.dataset.target,10);
  const suffix=el.dataset.suffix||'';
  const dur=1800;const start=performance.now();
  const ease=t=>1-Math.pow(1-t,4);
  const tick=now=>{
    const p=Math.min((now-start)/dur,1);
    el.textContent=Math.floor(ease(p)*target)+suffix;
    if(p<1)requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}
const counterObs=new IntersectionObserver(entries=>{
  entries.forEach(e=>{if(e.isIntersecting){animCounter(e.target);counterObs.unobserve(e.target);}});
},{threshold:0.5});
document.querySelectorAll('[data-target]').forEach(el=>counterObs.observe(el));
