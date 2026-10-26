import { LING, LING_NAME } from '../content.js';
import { speak } from '../audio.js';
import { t, pick } from '../i18n.js';
import { sample, shuffle, starsFromMistakes } from '../util.js';

// Level type "sort": drag (or tap) each word into the पुल्लिंग or स्त्रीलिंग door.
export default function sort(kit, level) {
  const bank = level.items || LING;
  // Two doors. The default is पुल्लिंग / स्त्रीलिंग; a level can name its own (level.bins).
  const bins0 = level.bins || {
    m: { label: LING_NAME.m, icon: '👦', sub: { en: t('masculine'), hi: t('masculine') } },
    f: { label: LING_NAME.f, icon: '👧', sub: { en: t('feminine'), hi: t('feminine') } },
  };
  const [g1, g2] = Object.keys(bins0);
  const nameOf = (g) => bins0[g].label;
  const items = shuffle([
    ...sample(bank.filter((x) => x.g === g1), 5),
    ...sample(bank.filter((x) => x.g === g2), 5),
  ]);
  let i = 0;
  let firstTry = 0;
  let busy = false;
  const counts = { [g1]: 0, [g2]: 0 };

  kit.body.innerHTML = `
    <p class="q-prompt">${t('sortPrompt')}</p>
    <div class="sort-stage"><div class="sort-card" role="img"></div></div>
    <div class="bins">
      ${[g1, g2].map((g, k) => `
        <button class="bin ${k ? 'second' : ''}" type="button" data-g="${g}">
          <span class="bin-ico" aria-hidden="true">${bins0[g].icon}</span>
          <b class="deva">${bins0[g].label}</b><small>${pick(bins0[g].sub)}</small>
          <span class="bin-count">0</span>
        </button>`).join('')}
    </div>`;

  const card = kit.body.querySelector('.sort-card');
  const bins = [...kit.body.querySelectorAll('.bin')];
  const binFor = (g) => bins.find((b) => b.dataset.g === g);

  function show() {
    const item = items[i];
    busy = false;
    card.className = 'sort-card enter';
    card.style.transform = '';
    card.style.opacity = '';
    card.setAttribute('aria-label', item.w);
    card.innerHTML = `<span class="sc-pic" aria-hidden="true">${item.e}</span><span class="sc-word deva">${item.w}</span>`;
    kit.foot.innerHTML = '';
  }

  function flyTo(bin) {
    const from = card.getBoundingClientRect();
    const to = bin.getBoundingClientRect();
    const dx = to.left + to.width / 2 - (from.left + from.width / 2);
    const dy = to.top + to.height / 2 - (from.top + from.height / 2);
    const base = card.style.transform || '';
    card.classList.remove('dragging', 'enter');
    card.style.transform = `${base} translate(${dx}px, ${dy}px) scale(.25)`;
    card.style.opacity = '0';
  }

  function drop(bin) {
    counts[bin.dataset.g]++;
    bin.querySelector('.bin-count').textContent = counts[bin.dataset.g];
  }

  function judge(g) {
    if (busy) return;
    busy = true;
    const item = items[i];
    const chosen = binFor(g);
    bins.forEach((b) => b.classList.remove('over', 'good', 'bad'));
    if (g === item.g) {
      firstTry++;
      kit.right();
      chosen.classList.add('good');
      flyTo(chosen);
      drop(chosen);
      speak(item.w);
      kit.later(next, 700);
    } else {
      kit.wrong();
      chosen.classList.add('bad');
      card.style.transform = '';
      const right = binFor(item.g);
      kit.foot.innerHTML = `<div class="fix"><span class="deva">${t('wordIs', { w: item.w, g: nameOf(item.g) })}</span></div>`;
      speak(item.w);
      kit.later(() => {
        right.classList.add('good');
        flyTo(right);
        drop(right);
      }, 1100);
      kit.later(next, 2300);
    }
  }

  function next() {
    bins.forEach((b) => b.classList.remove('good', 'bad'));
    i++;
    kit.progress(i / items.length);
    if (i < items.length) return show();
    kit.finish({
      stars: starsFromMistakes(items.length - firstTry),
      correct: firstTry,
      total: items.length,
      score: firstTry,
    });
  }

  // Drag with mouse or finger; tapping a door does the same thing.
  const binAt = (x, y) => bins.find((b) => {
    const r = b.getBoundingClientRect();
    return x >= r.left && x <= r.right && y >= r.top && y <= r.bottom;
  });
  let drag = null;

  card.addEventListener('pointerdown', (e) => {
    if (busy) return;
    drag = { x: e.clientX, y: e.clientY };
    card.setPointerCapture(e.pointerId);
    card.classList.remove('enter');
    card.classList.add('dragging');
  });
  card.addEventListener('pointermove', (e) => {
    if (!drag) return;
    const dx = e.clientX - drag.x;
    const dy = e.clientY - drag.y;
    card.style.transform = `translate(${dx}px, ${dy}px) rotate(${dx / 18}deg)`;
    const over = binAt(e.clientX, e.clientY);
    bins.forEach((b) => b.classList.toggle('over', b === over));
  });
  const endDrag = (e) => {
    if (!drag) return;
    drag = null;
    card.classList.remove('dragging');
    const bin = e.type === 'pointerup' ? binAt(e.clientX, e.clientY) : null;
    bins.forEach((b) => b.classList.remove('over'));
    if (bin) judge(bin.dataset.g);
    else card.style.transform = '';
  };
  card.addEventListener('pointerup', endDrag);
  card.addEventListener('pointercancel', endDrag);
  bins.forEach((b) => { b.onclick = () => judge(b.dataset.g); });

  show();
}
