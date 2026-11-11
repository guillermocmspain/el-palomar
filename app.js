const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const scene = document.querySelector('.scroll-scene');
if (scene) {
  const panel = scene.querySelector('.landscape');
  let pending = false;
  function paint() {
    const height = panel.clientHeight;
    const width = panel.clientWidth;
    const progress = Math.min(1, Math.max(0, scrollY / Math.max(1, scene.offsetHeight - scene.firstElementChild.offsetHeight) * 1.4));
    const diameter = Math.min(height,width);
    const inset = dim => 50 * (1 - diameter / dim) * Math.min(1, progress * 1.8) + 50 * diameter / dim * Math.max(0,(progress - 1/1.8)/(1 - 1/1.8));
    panel.style.setProperty('--h', inset(width) + '%');
    panel.style.setProperty('--v', inset(height) + '%');
    panel.style.setProperty('--r', (24 + progress * diameter) + 'px');
    scene.style.setProperty('--copy', Math.max(0, 1-progress*5));
    scene.style.setProperty('--intro', Math.max(0,(progress-.95)*20));
    document.body.classList.toggle('scrolled', progress > .17);
    scene.style.setProperty('--lift', (15 * progress) + 'svh');
    pending = false;
  }
  function schedule() {
    if (!pending) { pending = true; requestAnimationFrame(paint); }
  }
  addEventListener('scroll',schedule,{passive:true});
  addEventListener('resize',schedule);
  addEventListener('pageshow',schedule);
  paint();
}

function animateAsset(image) {
  const parent = image.parentElement;
  const source = image.dataset.motion || image.dataset.turn;
  const detail = parent.classList.contains('sample');
  const button = detail ? parent.querySelector('.turn-control') : image.dataset.motion && image.closest('.sticky, .portrait').querySelector('.pause, .motion-control');
  const video = document.createElement('video');
  video.className = 'asset-motion';
  video.muted = true;
  video.playsInline = true;
  video.loop = true;
  video.preload = 'none';
  video.setAttribute('aria-hidden','true');
  parent.append(video);
  let visible = false;
  let paused = detail || reduced.matches || Boolean(navigator.connection?.saveData);
  let ready = false;
  function align() {
    video.style.left = image.offsetLeft+'px';
    video.style.top = image.offsetTop+'px';
    video.style.width = image.offsetWidth+'px';
    video.style.height = image.offsetHeight+'px';
  }
  function showPoster() {
    video.classList.remove('is-playing');
    image.style.opacity = '';
  }
  function refresh() {
    if (button) {
      button.textContent = detail ? (paused ? 'Girar el huevo' : 'Pausar giro') : (paused ? '▶' : 'Ⅱ');
      button.setAttribute('aria-label',detail ? button.textContent : (paused?'Reproducir movimiento':'Pausar movimiento'));
    }
    if (!visible || paused || document.hidden || !ready) {
      video.pause(); showPoster(); return;
    }
    if (!video.src) video.src = source.replace(/\.webp$/,'.webm');
    video.play().catch(showPoster);
  }
  video.addEventListener('playing',()=>{
    align(); video.classList.add('is-playing'); image.style.opacity='0';
  });
  video.addEventListener('error',showPoster);
  button && button.addEventListener('click',()=>{ paused=!paused;refresh(); });
  new ResizeObserver(align).observe(parent);
  new ResizeObserver(align).observe(image);
  new IntersectionObserver(([entry])=>{
    visible=entry.isIntersecting;
    if(visible && !reduced.matches && parent.classList.contains('shelf') && !parent.dataset.entered){
      parent.animate([{transform:'translateY(-22%)'},{transform:'translateY(0)'}],{duration:650,easing:'ease-out'});
      parent.dataset.entered='true';
    }
    refresh();
  },{threshold:.08}).observe(image);
  reduced.addEventListener('change',()=>{paused=reduced.matches;refresh();});
  document.addEventListener('visibilitychange',refresh);
  const start=()=>{ready=true;refresh();};
  if(document.readyState==='complete')start();else window.addEventListener('load',start,{once:true});
}
document.querySelectorAll('[data-turn], [data-motion]').forEach(animateAsset);

const mobileMenu = document.getElementById('mobile-menu');
function dismissMobileMenu() {
  if (mobileMenu?.hidePopover && mobileMenu.matches(':popover-open')) mobileMenu.hidePopover();
}
matchMedia('(max-width:700px)').addEventListener('change',dismissMobileMenu);
window.addEventListener('pageshow',dismissMobileMenu);

const chapters = [...document.querySelectorAll('.calibre-chapter')];
if (chapters.length) {
  const animateScroll = matchMedia('(prefers-reduced-motion:no-preference) and (min-height:480px)');
  let scheduled = false;
  function drawChapters() {
    scheduled = false;
    document.documentElement.classList.toggle('walk-enabled', animateScroll.matches);
    for (const chapter of chapters) {
      if (!animateScroll.matches) {
        chapter.style.removeProperty('--grow');
        chapter.style.removeProperty('--rise');
        continue;
      }
      const bounds = chapter.getBoundingClientRect();
      const viewport = chapter.firstElementChild.offsetHeight;
      if (bounds.bottom < 0 || bounds.top > innerHeight) continue;
      const distance = Math.max(1, bounds.height - viewport);
      const p = Math.min(1, Math.max(0, (.32 * viewport - bounds.top) / (distance + .32 * viewport)));
      const ease = p * p * (3 - 2 * p);
      chapter.style.setProperty('--grow', (.64 + .48 * ease).toFixed(4));
      chapter.style.setProperty('--rise', ((1-ease)*Math.min(112,viewport*.12)).toFixed(1)+'px');
    }
  }
  function queueChapters() {
    if (!scheduled) { scheduled=true; requestAnimationFrame(drawChapters); }
  }
  drawChapters();
  addEventListener('scroll',queueChapters,{passive:true});
  addEventListener('resize',queueChapters);
  animateScroll.addEventListener('change',queueChapters);
}
