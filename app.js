const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const scene = document.querySelector('.scroll-scene');
if (scene) {
  const panel = scene.querySelector('.landscape');
  const video = scene.querySelector('video');
  const portrait = matchMedia('(max-aspect-ratio: 1/1)');
  let pending = false;
  let active = true;
  let ready = false;
  function refreshVideo() {
    if (!ready || !active || reduced.matches || document.hidden || navigator.connection?.saveData) {
      video.pause();
      return;
    }
    const source = portrait.matches ? video.dataset.tall : video.dataset.wide;
    if (video.getAttribute('src') !== source) video.src = source;
    video.play().catch(() => {});
  }
  video.addEventListener('playing', () => video.classList.add('playing'));
  function paint() {
    const height = panel.clientHeight;
    const width = panel.clientWidth;
    const progress = Math.min(1, Math.max(0, scrollY / Math.max(1, scene.offsetHeight - scene.firstElementChild.offsetHeight)));
    const diameter = Math.min(height,width);
    const inset = dim => 50 * (1 - diameter / dim) * Math.min(1, progress * 1.8) + 50 * diameter / dim * Math.max(0,(progress - 1/1.8)/(1 - 1/1.8));
    panel.style.setProperty('--h', inset(width) + '%');
    panel.style.setProperty('--v', inset(height) + '%');
    panel.style.setProperty('--r', (24 + progress * diameter) + 'px');
    scene.style.setProperty('--copy', Math.max(0, 1-progress*5));
    document.body.classList.toggle('scrolled', progress > .17);
    pending = false;
  }
  function schedule() {
    if (!pending) { pending = true; requestAnimationFrame(paint); }
  }
  addEventListener('scroll',schedule,{passive:true});
  addEventListener('resize',schedule);
  addEventListener('pageshow',schedule);
  portrait.addEventListener('change',refreshVideo);
  reduced.addEventListener('change',refreshVideo);
  document.addEventListener('visibilitychange',refreshVideo);
  new IntersectionObserver(([entry]) => { active = entry.isIntersecting; refreshVideo(); }).observe(scene);
  paint();
  addEventListener('load', () => { setTimeout(() => {ready=true;refreshVideo();},1400); });
}
const eggs=document.querySelectorAll('[data-turn]');
const animation=new IntersectionObserver(entries=>{
  for(const {target,isIntersecting} of entries) {
    target.dataset.still ||= target.getAttribute('src');
    target.src=isIntersecting && !reduced.matches && !navigator.connection?.saveData ? target.dataset.turn : target.dataset.still;
    if(isIntersecting && !reduced.matches && target.closest('.shelf') && !target.dataset.entered){
      target.animate([{transform:'translateY(-45%)',opacity:0},{transform:'translateY(0)',opacity:1}],{duration:650,easing:'ease-out'});
      target.dataset.entered='true';
    }
  }
},{threshold:.12});
eggs.forEach(img=>animation.observe(img));
