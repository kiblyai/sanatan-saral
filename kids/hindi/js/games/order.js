import { speak, sfx } from '../audio.js';
import { t, pick } from '../i18n.js';
import { esc, sample, shuffle, starsFromMistakes } from '../util.js';

// Level type "order": tap the word tiles in order to build the sentence.
// "_" joins words that move together (पेड़_पर, देते_हैं). Hindi word order is flexible,
// so an item may list other correct orders in `alt`; any of them is accepted.
function parse(sentence) {
  const end = /[।?!]$/.test(sentence) ? sentence.slice(-1) : '';
  const body = end ? sentence.slice(0, -1) : sentence;
  return { end, words: body.split(' ').map((w) => w.replace(/_/g, ' ')) };
}

export default function order(kit, level) {
  const items = sample(level.items, level.count || level.items.length);
  let i = 0;
  let cleanSentences = 0;

  function show() {
    const item = items[i];
    const main = parse(item.s);
    const orders = [main.words, ...(item.alt || []).map((a) => parse(a).words)];
    const spoken = item.s.replace(/_/g, ' ');
    let pool = shuffle(main.words.map((w, k) => ({ w, k })));
    // Never hand the child a sentence that is already in order.
    if (orders.some((o) => o.every((w, idx) => pool[idx].w === w))) pool = [...pool.slice(1), pool[0]];
    const placed = [];
    let slips = 0;
    let clean = true;
    let done = false;

    kit.body.innerHTML = `
      <p class="q-prompt">${pick(level.prompt)}</p>
      <div class="q-card sentence-card">
        <div class="chips-line" data-line></div>
      </div>
      <div class="chips-line" data-pool>
        ${pool.map((p) => `<button class="wchip deva" type="button" data-k="${p.k}">${esc(p.w)}</button>`).join('')}
      </div>
      <button class="say-btn center-self" type="button" data-say>🔊 ${t('listen')}</button>`;
    kit.foot.innerHTML = '';
    const card = kit.body.querySelector('.sentence-card');
    const line = kit.body.querySelector('[data-line]');
    const poolChips = [...kit.body.querySelectorAll('[data-pool] .wchip')];

    function paintLine() {
      const left = main.words.length - placed.length;
      line.innerHTML =
        placed.map((w) => `<span class="wchip deva placed">${esc(w)}</span>`).join('') +
        '<span class="slot-chip" aria-hidden="true"></span>'.repeat(left) +
        `<span class="deva danda">${main.end}</span>`;
    }
    paintLine();

    // A word fits if the sentence so far plus this word starts at least one correct order.
    const fits = (w) => orders.some((o) => placed.every((p, idx) => o[idx] === p) && o[placed.length] === w);

    kit.body.querySelector('[data-say]').onclick = () => speak(spoken);
    poolChips.forEach((chip) => {
      chip.onclick = () => {
        if (done || chip.disabled) return;
        const w = main.words[Number(chip.dataset.k)];
        if (fits(w)) {
          placed.push(w);
          chip.disabled = true;
          chip.classList.add('used');
          poolChips.forEach((c) => c.classList.remove('hint'));
          slips = 0;
          paintLine();
          if (placed.length < main.words.length) {
            sfx('tap');
            return;
          }
          done = true;
          if (clean) cleanSentences++;
          kit.right();
          card.classList.add('win');
          speak(spoken);
          kit.later(next, 1400);
        } else {
          clean = false;
          slips++;
          kit.wrong();
          chip.classList.add('bad');
          kit.later(() => chip.classList.remove('bad'), 450);
          // After two slips, light up a word that fits next.
          if (slips >= 2) {
            const helper = poolChips.find((c) => !c.disabled && fits(main.words[Number(c.dataset.k)]));
            if (helper) helper.classList.add('hint');
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
