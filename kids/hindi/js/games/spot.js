import { speak } from '../audio.js';
import { t, pick } from '../i18n.js';
import { esc, sample, starsFromMistakes } from '../util.js';

// Level type "spot": tap every target word in a sentence (संज्ञा now; सर्वनाम, विशेषण,
// क्रिया later). The closing mark (। ? !) is shown but can't be tapped.
export default function spot(kit, level) {
  const items = sample(level.items, level.count || level.items.length);
  let i = 0;
  let cleanSentences = 0;

  function show() {
    const item = items[i];
    const end = /[।?!]$/.test(item.s) ? item.s.slice(-1) : '';
    const words = (end ? item.s.slice(0, -1) : item.s).split(' ').map((w) => w.replace(/_/g, ' '));
    const spoken = item.s.replace(/_/g, ' ');
    const targets = new Set(item.t);
    const found = new Set();
    let misses = 0;
    let done = false;

    kit.body.innerHTML = `
      <p class="q-prompt">${pick(level.prompt)}</p>
      <div class="q-card spot-card">
        <div class="chips-line">
          ${words.map((w, k) => `<button class="wchip deva" type="button" data-k="${k}">${esc(w)}</button>`).join('')}<span class="deva danda">${end}</span>
        </div>
        <small class="muted" data-left>${t('spotFind', { n: targets.size })}</small>
      </div>
      <button class="say-btn center-self" type="button" data-say>🔊 ${t('listen')}</button>`;
    kit.foot.innerHTML = '';
    kit.body.querySelector('[data-say]').onclick = () => speak(spoken);
    const leftEl = kit.body.querySelector('[data-left]');

    kit.body.querySelectorAll('.wchip').forEach((chip) => {
      chip.onclick = () => {
        if (done || chip.classList.contains('good')) return;
        const word = words[Number(chip.dataset.k)];
        if (targets.has(word) && !found.has(word)) {
          found.add(word);
          chip.classList.remove('hint');
          chip.classList.add('good');
          kit.right({ quiet: found.size < targets.size });
          const left = targets.size - found.size;
          leftEl.textContent = left ? t('spotFind', { n: left }) : '✅';
          if (!left) {
            done = true;
            if (!misses) cleanSentences++;
            speak(spoken);
            kit.later(next, 1300);
          }
        } else {
          misses++;
          kit.wrong();
          chip.classList.add('bad');
          kit.later(() => chip.classList.remove('bad'), 450);
          // After two slips, show where the remaining answers are.
          if (misses >= 2) {
            kit.body.querySelectorAll('.wchip').forEach((c) => {
              const w = words[Number(c.dataset.k)];
              if (targets.has(w) && !found.has(w)) c.classList.add('hint');
            });
          }
        }
      };
    });
  }

  function next() {
    i++;
    kit.progress(i / items.length);
    if (i < items.length) return show();
    kit.finish({
      stars: starsFromMistakes(kit.stats.mistakes),
      correct: cleanSentences,
      total: items.length,
      score: cleanSentences,
    });
  }

  show();
}
