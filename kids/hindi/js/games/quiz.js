import { MATRA } from '../content.js';
import { speak } from '../audio.js';
import { t, pick } from '../i18n.js';
import { esc, sample, shuffle, starsFromMistakes } from '../util.js';

// Level type "quiz": see the picture, hear the word, tap the right spelling.
export default function quiz(kit, level) {
  const items = sample(level.items || MATRA, level.count || 10);
  let i = 0;
  let firstTry = 0;

  function show() {
    const item = items[i];
    const options = shuffle([item.w, ...item.x]);
    kit.body.innerHTML = `
      <div class="q-card">
        ${item.s ? `<p class="q-prompt big deva">${esc(item.s)}</p>` : `<div class="q-pic" aria-hidden="true">${item.e}</div>`}
        <button class="say-btn" type="button" data-say>🔊 ${t('listen')}</button>
      </div>
      <p class="q-prompt">${level.prompt ? pick(level.prompt) : t('pickSpelling')}</p>
      <div class="opts ${options.length === 3 ? 'three' : ''}">
        ${options.map((o) => `<button class="opt deva" type="button" data-o="${esc(o)}">${esc(o)}</button>`).join('')}
      </div>`;
    kit.foot.innerHTML = '';

    kit.body.querySelector('[data-say]').onclick = () => speak(item.say || item.s || item.w);
    let answered = false;
    kit.body.querySelectorAll('[data-o]').forEach((btn) => {
      btn.onclick = () => {
        if (answered) return;
        answered = true;
        kit.body.querySelectorAll('[data-o]').forEach((b) => {
          b.disabled = true;
          if (b.dataset.o === item.w) b.classList.add('good');
        });
        if (btn.dataset.o === item.w) {
          firstTry++;
          kit.right();
          kit.later(next, 900);
        } else {
          btn.classList.add('bad');
          kit.wrong();
          speak(item.say || item.s || item.w);
          kit.showFix(item.s ? t('rightAnswerIs') : t('rightWordIs'), item.w, next);
        }
      };
    });
    kit.later(() => speak(item.say || item.s || item.w), 350);
  }

  function next() {
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

  show();
}
