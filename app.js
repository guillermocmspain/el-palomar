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
  const animateScroll = matchMedia('(prefers-reduced-motion:no-preference) and (min-height:300px)');
  const pasture = document.querySelector('.pasture');
  const models = chapters.map(chapter => chapter.querySelector('.shell-model'));
  const flight = document.createElement('div');
  flight.className = 'egg-flight';
  flight.hidden = true;
  flight.setAttribute('aria-hidden','true');
  const surfaces = [new Image(), new Image()];
  surfaces.forEach(image => { image.alt=''; flight.append(image); });
  document.body.append(flight);
  let currentPair = -1;
  function handoff(index, progress, height) {
    if (currentPair !== index) {
      models.forEach(model => model.classList.remove('in-flight'));
      currentPair = index;
      flight.hidden = index < 0;
      if (index >= 0) surfaces.forEach((image, offset) => {
        const model = models[index+offset];
        image.src = model.querySelector('img').src;
        model.classList.add('in-flight');
      });
    }
    if (index < 0) return;
    const a = models[index].getBoundingClientRect();
    const b = models[index+1].getBoundingClientRect();
    const t = progress, blend = t*t*(3-2*t);
    const mix = (start,end) => start+(end-start)*blend;
    const width=mix(a.width,b.width), eggHeight=mix(a.height,b.height);
    const x=mix(a.left+a.width/2,b.left+b.width/2)-width/2;
    const arc=Math.sin(Math.PI*t);
    const y=mix(a.top+t*height+a.height/2,b.top-(1-t)*height+b.height/2)-eggHeight/2
      +Math.min(125,height*.14)*arc*arc;
    flight.style.width=width+'px';
    flight.style.height=eggHeight+'px';
    flight.style.transform='translate3d('+x+'px,'+y+'px,0) rotate('+(-7*arc)+'deg)';
    const skin=Math.min(1,Math.max(0,(t-.25)/.5));
    surfaces[1].style.opacity=skin*skin*(3-2*skin);
  }
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
    let pair=-1, transition=0;
    const height=chapters[0].firstElementChild.offsetHeight;
    if (animateScroll.matches) {
      const second=chapters[1].getBoundingClientRect().top;
      pasture.style.setProperty('--field-mix',Math.max(0,Math.min(1,1-second/height)));
      const span=chapters[3].offsetTop-chapters[1].offsetTop+height;
      pasture.style.setProperty('--field-pan',Math.max(0,Math.min(100,100*(height-second)/span))+'%');
      for(let i=1;i<chapters.length;i++){
        const top=chapters[i].getBoundingClientRect().top;
        if(top>0 && top<height){pair=i-1;transition=1-top/height;break;}
      }
    }
    handoff(pair,transition,height);
  }
  function queueChapters() {
    if (!scheduled) { scheduled=true; requestAnimationFrame(drawChapters); }
  }
  drawChapters();
  addEventListener('scroll',queueChapters,{passive:true});
  addEventListener('resize',queueChapters);
  animateScroll.addEventListener('change',queueChapters);
}
