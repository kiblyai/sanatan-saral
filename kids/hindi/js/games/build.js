import { BUILD, MATRAS, wordOf } from '../content.js';
import { speak, sfx } from '../audio.js';
import { t } from '../i18n.js';
import { sample, starsFromMistakes } from '../util.js';

// Level type "build": the word is missing its matras; tap the right one for each gap.
export default function build(kit, level) {
  const items = sample(level.items || BUILD, level.count || 8);
  let i = 0;
  let cleanWords = 0;

  function show() {
    const item = items[i];
    const word = wordOf(item);
    const gaps = item.p.map(([, m], idx) => (m ? idx : -1)).filter((idx) => idx >= 0);
    const filled = new Set();
    let cur = 0;
    let missesHere = 0;
    let wordClean = true;
    let done = false;

    kit.body.innerHTML = `
      <div class="q-card">
        <div class="q-pic" aria-hidden="true">${item.e}</div>
        <button class="say-btn" type="button" data-say>🔊 ${t('listen')}</button>
      </div>
      <p class="q-prompt">${t('buildPrompt')}</p>
      <div class="word-tiles" aria-live="polite"></div>
      <div class="palette">
        ${MATRAS.map(({ m, v }) => `
          <button class="mtile" type="button" data-m="${m}" aria-label="${v} की मात्रा">
            <span class="deva">◌${m}</span><small class="deva">${v}</small>
          </button>`).join('')}
      </div>`;
    kit.foot.innerHTML = '';

    const tilesEl = kit.body.querySelector('.word-tiles');
    function paintTiles() {
      tilesEl.innerHTML = item.p.map(([letter, matra], idx) => {
        if (!matra) return `<span class="tile deva">${letter}</span>`;
        if (filled.has(idx)) return `<span class="tile deva done">${letter}${matra}</span>`;
        const active = gaps[cur] === idx ? ' active' : '';
        return `<span class="tile deva open${active}">${letter}<span class="slot"></span></span>`;
      }).join('');
    }
    paintTiles();

    kit.body.querySelector('[data-say]').onclick = () => speak(word);
    kit.body.querySelectorAll('[data-m]').forEach((btn) => {
      btn.onclick = () => {
        if (done) return;
        const idx = gaps[cur];
        if (btn.dataset.m === item.p[idx][1]) {
          filled.add(idx);
          cur++;
          missesHere = 0;
          kit.body.querySelectorAll('.mtile.hint').forEach((b) => b.classList.remove('hint'));
          paintTiles();
          if (cur < gaps.length) {
            sfx('tap');
            return;
          }
          done = true;
          if (wordClean) cleanWords++;
          kit.right();
          tilesEl.classList.add('win');
          speak(word);
          kit.later(next, 1300);
        } else {
          wordClean = false;
          missesHere++;
          kit.wrong();
          btn.classList.remove('shake');
          void btn.offsetWidth;
          btn.classList.add('shake');
          kit.later(() => btn.classList.remove('shake'), 450);
          // After two slips on the same gap, light up the right matra.
          if (missesHere >= 2) {
            kit.body.querySelector(`[data-m="${item.p[idx][1]}"]`).classList.add('hint');
          }
        }
      };
    });
    kit.later(() => speak(word), 350);
  }

  function next() {
    i++;
    kit.progress(i / items.length);
    if (i < items.length) return show();
    kit.finish({
      stars: starsFromMistakes(kit.stats.mistakes),
      correct: cleanWords,
      total: items.length,
      score: cleanWords,
    });
  }

  show();
}
