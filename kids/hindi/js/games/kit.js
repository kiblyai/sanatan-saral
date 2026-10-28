import { sfx } from '../audio.js';
import { t } from '../i18n.js';
import { esc, pickOne } from '../util.js';

// Shared plumbing for every game: fuel bar, streak, praise, timers, clean exit.
export function createKit(frame) {
  const body = frame.querySelector('.game-body');
  const foot = frame.querySelector('.game-foot');
  const bar = frame.querySelector('.fuel');
  const fill = frame.querySelector('.fuel-fill');
  const streakBox = frame.querySelector('.streak');
  const streakNum = streakBox.querySelector('b');
  const timers = new Set();
  const cleanups = [];
  const stats = { mistakes: 0, streak: 0, bestStreak: 0 };

  function paintStreak() {
    streakNum.textContent = stats.streak;
    streakBox.classList.toggle('hot', stats.streak >= 3);
    streakBox.classList.remove('bump');
    void streakBox.offsetWidth; // restart the animation
    if (stats.streak > 0) streakBox.classList.add('bump');
  }

  const kit = {
    body,
    foot,
    frame,
    stats,
    finish: () => {}, // replaced by app.js

    progress(fraction) {
      const pct = Math.round(Math.max(0, Math.min(1, fraction)) * 100);
      fill.style.width = `${pct}%`;
      bar.setAttribute('aria-valuenow', String(pct));
    },

    right({ quiet = false } = {}) {
      stats.streak++;
      stats.bestStreak = Math.max(stats.bestStreak, stats.streak);
      sfx('good');
      paintStreak();
      if (!quiet) kit.toast(pickOne(t('praise')));
    },

    wrong() {
      stats.mistakes++;
      stats.streak = 0;
      sfx('bad');
      paintStreak();
    },

    toast(text, cls = '') {
      const host = document.getElementById('toast');
      const el = document.createElement('div');
      el.className = `toast-msg ${cls}`;
      el.textContent = text;
      host.appendChild(el);
      setTimeout(() => el.remove(), 1200);
    },

    // Shows the right answer after a slip and waits for the child to tap Next.
    showFix(label, word, onNext) {
      foot.innerHTML = `
        <div class="fix">
          <span>${esc(label)} <b class="deva">${esc(word)}</b></span>
          <button class="btn btn-primary" type="button" data-next>${t('next')} →</button>
        </div>`;
      const btn = foot.querySelector('[data-next]');
      btn.focus({ preventScroll: true });
      btn.onclick = () => {
        foot.innerHTML = '';
        onNext();
      };
    },

    later(fn, ms) {
      const id = setTimeout(() => {
        timers.delete(id);
        fn();
      }, ms);
      timers.add(id);
      return id;
    },

    onCleanup(fn) {
      cleanups.push(fn);
    },

    cleanup() {
      timers.forEach(clearTimeout);
      timers.clear();
      cleanups.splice(0).forEach((fn) => fn());
    },
  };

  return kit;
}
