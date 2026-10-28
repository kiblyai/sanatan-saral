import { LING, LING_NAME, MATRA, VACHAN } from '../content.js';
import { sfx, speak } from '../audio.js';
import { t } from '../i18n.js';
import { esc, pickOne, sample, shuffle } from '../util.js';

const DURATION = 60;
const BONUS_EVERY = 5;
const BONUS_SECONDS = 3;

// Level type "meteor": 60-second mixed speed round across the whole planet.
export default function meteor(kit) {
  let left = DURATION;
  let score = 0;
  let over = false;
  let lastKey = '';

  kit.body.innerHTML = `
    <div class="meteor-field" aria-hidden="true">${'<span class="falling">☄️</span>'.repeat(6)}</div>
    <div class="meteor-hud">
      <div><small>${t('score')}</small><b data-score>0</b></div>
      <div><small>${t('timeLeft')}</small><b data-time>${DURATION}</b></div>
    </div>
    <div class="m-q"></div>`;
  kit.foot.innerHTML = '';
  const qEl = kit.body.querySelector('.m-q');
  const scoreEl = kit.body.querySelector('[data-score]');
  const timeEl = kit.body.querySelector('[data-time]');

  function paintTime() {
    kit.progress(left / DURATION);
    timeEl.textContent = Math.max(0, Math.ceil(left));
    kit.frame.classList.toggle('hurry', left <= 10);
  }
  paintTime();

  // Counts down only while the app is on screen.
  const tick = setInterval(() => {
    if (over || document.hidden) return;
    left -= 0.1;
    if (left <= 0) end();
    else paintTime();
  }, 100);
  kit.onCleanup(() => clearInterval(tick));

  function makeQuestion() {
    const kind = pickOne(['matra', 'ling', 'vachan']);
    if (kind === 'matra') {
      const it = pickOne(MATRA);
      return {
        key: it.w,
        say: it.w,
        html: `<div class="q-pic sm" aria-hidden="true">${it.e}</div><p class="q-prompt">${t('mMatra')}</p>`,
        options: shuffle([it.w, ...sample(it.x, 2)]),
        answer: it.w,
      };
    }
    if (kind === 'ling') {
      const it = pickOne(LING);
      return {
        key: it.w,
        html: `<p class="q-prompt big deva">${esc(t('mLing', { w: it.w }))}</p>`,
        options: [LING_NAME.m, LING_NAME.f],
        answer: LING_NAME[it.g],
      };
    }
    const it = pickOne(VACHAN);
    return {
      key: it.a,
      html: `<p class="q-prompt big deva">${esc(t('mVachan', { w: it.a }))}</p>`,
      options: shuffle([it.b, ...it.x]),
      answer: it.b,
    };
  }

  function ask() {
    if (over) return;
    let q = makeQuestion();
    while (q.key === lastKey) q = makeQuestion();
    lastKey = q.key;

    qEl.innerHTML = `
      <div class="q-card meteor-card">${q.html}</div>
      <div class="opts ${q.options.length === 3 ? 'three' : ''}">
        ${q.options.map((o) => `<button class="opt deva" type="button" data-o="${esc(o)}">${esc(o)}</button>`).join('')}
      </div>`;
    if (q.say) speak(q.say);

    let answered = false;
    qEl.querySelectorAll('[data-o]').forEach((btn) => {
      btn.onclick = () => {
        if (answered || over) return;
        answered = true;
        qEl.querySelectorAll('[data-o]').forEach((b) => {
          b.disabled = true;
          if (b.dataset.o === q.answer) b.classList.add('good');
        });
        if (btn.dataset.o === q.answer) {
          score++;
          scoreEl.textContent = score;
          kit.right({ quiet: true });
          if (kit.stats.streak % BONUS_EVERY === 0) {
            left += BONUS_SECONDS;
            sfx('bonus');
            kit.toast(t('bonusTime'), 'bonus');
            paintTime();
          }
          kit.later(ask, 300);
        } else {
          btn.classList.add('bad');
          kit.wrong();
          kit.later(ask, 1000);
        }
      };
    });
  }

  function end() {
    if (over) return;
    over = true;
    left = 0;
    paintTime();
    clearInterval(tick);
    const stars = score >= 15 ? 3 : score >= 10 ? 2 : score >= 6 ? 1 : 0;
    kit.finish({ stars, correct: score, total: null, score });
  }

  ask();
}
