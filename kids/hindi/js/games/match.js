import { speak } from '../audio.js';
import { t, pick, lang } from '../i18n.js';
import { esc, sample, shuffle, starsFromMistakes } from '../util.js';

// Level type "match": pair each left word with its partner on the right
// (वचन, विलोम, पर्यायवाची, शब्दार्थ…). Up to 6 pairs per board.
export default function match(kit, level) {
  const pool = level.count ? sample(level.pairs, level.count) : shuffle(level.pairs);
  const boardCount = Math.ceil(pool.length / 6);
  const size = Math.ceil(pool.length / boardCount);
  const boards = Array.from({ length: boardCount }, (_, i) => pool.slice(i * size, (i + 1) * size));
  const total = pool.length;
  let board = 0;
  let matched = 0;
  let firstTry = 0;

  const heading = ({ label, sub }) =>
    `<h3><span class="deva">${label}</span>${sub ? ` <small>(${pick(sub)})</small>` : ''}</h3>`;
  const isLong = (text) => [...text].length > 8;

  function show() {
    const pairs = boards[board];
    const right = shuffle(pairs.map((p, k) => ({ ...p, k })));
    const failed = new Set();
    const sel = { a: null, b: null };
    let pairedHere = 0;

    kit.body.innerHTML = `
      <p class="q-prompt">${level.prompt ? pick(level.prompt) : t('matchPrompt')}</p>
      <div class="match-grid">
        <div class="col">
          ${heading(level.cols.a)}
          ${pairs.map((p, k) => `
            <button class="mbtn deva ${isLong(p.a) ? 'long' : ''}" type="button" data-side="a" data-k="${k}" data-say="${esc(p.a)}">${esc(p.a)}</button>`).join('')}
        </div>
        <div class="col">
          ${heading(level.cols.b)}
          ${right.map((p) => `
            <button class="mbtn deva ${isLong(p.b) ? 'long' : ''}" type="button" data-side="b" data-k="${p.k}" data-say="${esc(p.b)}">
              ${esc(p.b)}${p.en && lang() === 'en' ? `<small class="gloss">${esc(p.en)}</small>` : ''}
            </button>`).join('')}
        </div>
      </div>`;
    kit.foot.innerHTML = '';

    const btn = (side, k) => kit.body.querySelector(`[data-side="${side}"][data-k="${k}"]`);

    kit.body.querySelectorAll('.mbtn').forEach((el) => {
      el.onclick = () => {
        if (el.classList.contains('paired')) return;
        const side = el.dataset.side;
        const k = Number(el.dataset.k);
        if (sel[side] !== null) btn(side, sel[side]).classList.remove('sel');
        sel[side] = k;
        el.classList.add('sel');
        if (/[\u0900-\u097F]/.test(el.dataset.say)) speak(el.dataset.say);
        if (sel.a === null || sel.b === null) return;

        const a = btn('a', sel.a);
        const b = btn('b', sel.b);
        if (sel.a === sel.b) {
          const color = `p${pairedHere % 6}`;
          [a, b].forEach((x) => {
            x.classList.remove('sel');
            x.classList.add('paired', color);
            x.disabled = true;
          });
          if (!failed.has(sel.a)) firstTry++;
          pairedHere++;
          matched++;
          kit.right({ quiet: true });
          kit.progress(matched / total);
          if (pairedHere === pairs.length) {
            kit.toast(t('praise')[0]);
            kit.later(() => {
              board++;
              if (board < boards.length) show();
              else finish();
            }, 900);
          }
        } else {
          failed.add(sel.a);
          kit.wrong();
          [a, b].forEach((x) => x.classList.add('bad'));
          kit.later(() => [a, b].forEach((x) => x.classList.remove('bad', 'sel')), 500);
        }
        sel.a = null;
        sel.b = null;
      };
    });
  }

  function finish() {
    kit.finish({
      stars: starsFromMistakes(kit.stats.mistakes),
      correct: firstTry,
      total,
      score: firstTry,
    });
  }

  show();
}
