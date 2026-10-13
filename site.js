(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const names = window.STAGE_NAMES || {};
  const shots = [...document.querySelectorAll('.shot')];
  const byP = {};
  shots.forEach((s) => (byP[s.dataset.p] ||= []).push(s));
  const order = [...document.querySelectorAll('.w')].map((w) => w.dataset.p);
  const sname = document.getElementById('sname');
  const sline = document.getElementById('sline');
  const ok = document.getElementById('ok');
  const READY = 'Draft ready. Reply ok to publish.';
  let cur = null, idx = 0, timer = null;

  function show(p, i = 0) {
    if (!byP[p]) return;
    const list = byP[p];
    idx = (i + list.length) % list.length;
    shots.forEach((s) => {
      const on = s.dataset.p === p && +s.dataset.s === idx;
      s.classList.toggle('on', on);
      if (s.tagName === 'VIDEO') { if (on && !reduce) { s.preload = 'auto'; s.play().catch(() => {}); } else s.pause(); }
    });
    if (p !== cur) {
      cur = p;
      sname.textContent = names[p] || p;
      sline.textContent = READY;
      ok.textContent = 'ok'; ok.classList.remove('done');
      document.querySelectorAll('.w').forEach((w) => w.classList.toggle('on', w.dataset.p === p));
    }
    restart();
  }
  function restart() {
    clearInterval(timer);
    if (reduce || !byP[cur] || byP[cur].length < 2) return;
    timer = setInterval(() => { if (!document.hidden) show(cur, idx + 1); }, 5600);
  }
  document.getElementById('prev').onclick = () => show(cur, idx - 1);
  document.getElementById('next').onclick = () => show(cur, idx + 1);
  ok.onclick = () => {
    if (ok.classList.contains('done')) return;
    ok.classList.add('done'); ok.textContent = 'Sent';
    sline.textContent = 'Approved. Scheduled for 19:30 Cairo time.';
    setTimeout(() => { const n = order[(order.indexOf(cur) + 1) % order.length]; show(n, 0); }, 2200);
  };

  // The stage follows the section being read
  const first = document.querySelector('[data-stage]');
  show(first ? first.dataset.stage : order[0], 0);
  const so = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) show(e.target.dataset.stage, 0); }), { rootMargin: '-45% 0px -45% 0px' });
  document.querySelectorAll('[data-stage]').forEach((el) => so.observe(el));

  // Work index: hover or focus previews, click opens
  document.querySelectorAll('.w').forEach((w) => {
    const b = w.querySelector('.wn');
    const pick = () => { if (w.dataset.p !== cur) show(w.dataset.p, 0); };
    b.addEventListener('mouseenter', pick);
    b.addEventListener('focus', pick);
    b.addEventListener('click', () => {
      const open = !w.classList.contains('open');
      document.querySelectorAll('.w.open').forEach((x) => { x.classList.remove('open'); x.querySelector('.wn').setAttribute('aria-expanded', 'false'); });
      if (open) { w.classList.add('open'); b.setAttribute('aria-expanded', 'true'); }
      show(w.dataset.p, 0);
    });
  });
  const firstW = document.querySelector('.w');
  if (firstW) { firstW.classList.add('open'); firstW.querySelector('.wn').setAttribute('aria-expanded', 'true'); }

  // Role fit list: the active line swaps the picture
  const fpics = [...document.querySelectorAll('.fpic img')];
  const rows = [...document.querySelectorAll('.f')];
  const act = (r) => {
    rows.forEach((x) => x.classList.toggle('on', x === r));
    fpics.forEach((im) => im.classList.toggle('on', im.dataset.img === r.dataset.img));
  };
  rows.forEach((r) => { r.addEventListener('mouseenter', () => act(r)); r.addEventListener('focus', () => act(r)); r.addEventListener('click', () => act(r)); });
  if (matchMedia('(hover: none)').matches || innerWidth < 720) {
    const fo = new IntersectionObserver((es) => es.forEach((e) => e.isIntersecting && act(e.target)), { rootMargin: '-45% 0px -45% 0px' });
    rows.forEach((r) => fo.observe(r));
  }

  // Entrances, once, in reading order
  const groups = [['.pc'], ['.w'], ['.f']];
  groups.forEach(([sel]) => document.querySelectorAll(sel).forEach((el, k) => el.style.setProperty('--k', k)));
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
  document.querySelectorAll('[data-reveal],.pc,.w,.f').forEach((el) => io.observe(el));

  // One field: write the email
  const cf = document.getElementById('cf');
  cf.addEventListener('submit', (e) => {
    e.preventDefault();
    const v = document.getElementById('q').value.trim();
    location.href = `mailto:${window.MAILTO}?subject=${encodeURIComponent(v ? v.slice(0, 80) : 'Hello Mahmoud')}&body=${encodeURIComponent(v + '\n\n')}`;
  });
})();
