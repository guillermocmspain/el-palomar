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

for (const image of document.querySelectorAll('[data-motion]')) {
  const still = image.getAttribute('src');
  const button = image.closest('.sticky, .portrait').querySelector('.pause, .motion-control');
  let stopped = reduced.matches || Boolean(navigator.connection?.saveData);
  let visible = false;
  function update() {
    const source = visible && !document.hidden && !stopped ? image.dataset.motion : still;
    if (image.getAttribute('src') !== source) image.src = source;
    button.textContent = stopped ? '▶' : 'Ⅱ';
    button.setAttribute('aria-label', stopped ? 'Reproducir movimiento' : 'Pausar movimiento');
  }
  button.addEventListener('click', () => { stopped = !stopped; update(); });
  reduced.addEventListener('change', () => { stopped = reduced.matches; update(); });
  document.addEventListener('visibilitychange', update);
  new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; update(); }).observe(image);
}
