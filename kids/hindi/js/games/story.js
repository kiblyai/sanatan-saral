import { speak } from '../audio.js';
import { t } from '../i18n.js';
import { esc, shuffle, starsFromMistakes } from '../util.js';

// Level type "story": an original short story, one page at a time with read-aloud,
// then comprehension questions.
export default function story(kit, level) {
  const { title, pages, qs } = level.story;
  const steps = pages.length + qs.length;
  let page = 0;
  let q = 0;
  let firstTry = 0;

  function showPage() {
    const p = pages[page];
    const last = page === pages.length - 1;
    kit.body.innerHTML = `
      <div class="story-card">
        ${page === 0 ? `<h2 class="story-title deva">${esc(title)}</h2>` : ''}
        <div class="story-pic" aria-hidden="true">${p.e}</div>
        <p class="story-text deva">${esc(p.t)}</p>
        <button class="say-btn" type="button" data-say>🔊 ${t('listen')}</button>
      </div>
      <div class="dots" aria-hidden="true">${pages.map((_, i) => `<span class="${i === page ? 'on' : ''}"></span>`).join('')}</div>`;
    kit.foot.innerHTML = `
      <div class="story-nav">
        ${page > 0 ? `<button class="btn btn-ghost" type="button" data-prev aria-label="${t('back')}">←</button>` : ''}
        <button class="btn btn-primary btn-grow" type="button" data-next>${last ? `✏️ ${t('toQuestions')}` : `${t('nextPage')} →`}</button>
      </div>`;
    kit.body.querySelector('[data-say]').onclick = () => speak(p.t);
    const prev = kit.foot.querySelector('[data-prev]');
    if (prev) prev.onclick = () => { page--; showPage(); };
    kit.foot.querySelector('[data-next]').onclick = () => {
      if (last) {
        kit.progress(pages.length / steps);
        showQuestion();
      } else {
        page++;
        kit.progress(page / steps);
        showPage();
      }
    };
    kit.later(() => speak(p.t), 300);
  }

  function showQuestion() {
    const item = qs[q];
    const options = shuffle([item.a, ...item.x]);
    kit.body.innerHTML = `
      <div class="q-card">
        <small class="muted">${t('questionN', { n: q + 1, total: qs.length })}</small>
        <p class="q-prompt big deva">${esc(item.q)}</p>
        <button class="say-btn" type="button" data-say>🔊 ${t('listen')}</button>
      </div>
      <div class="opts three">
        ${options.map((o) => `<button class="opt deva small-text" type="button" data-o="${esc(o)}">${esc(o)}</button>`).join('')}
      </div>`;
    kit.foot.innerHTML = '';
    kit.body.querySelector('[data-say]').onclick = () => speak(item.q);

    let answered = false;
    kit.body.querySelectorAll('[data-o]').forEach((btn) => {
      btn.onclick = () => {
        if (answered) return;
        answered = true;
        kit.body.querySelectorAll('[data-o]').forEach((b) => {
          b.disabled = true;
          if (b.dataset.o === item.a) b.classList.add('good');
        });
        if (btn.dataset.o === item.a) {
          firstTry++;
          kit.right();
          kit.later(nextQuestion, 1000);
        } else {
          btn.classList.add('bad');
          kit.wrong();
          speak(item.a);
          kit.showFix(t('rightAnswerIs'), item.a, nextQuestion);
        }
      };
    });
    kit.later(() => speak(item.q), 300);
  }

  function nextQuestion() {
    q++;
    kit.progress((pages.length + q) / steps);
    if (q < qs.length) return showQuestion();
    kit.finish({
      stars: starsFromMistakes(qs.length - firstTry),
      correct: firstTry,
      total: qs.length,
      score: firstTry,
    });
  }

  showPage();
}
