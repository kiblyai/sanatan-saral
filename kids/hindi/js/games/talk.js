import { speak, stopSpeech, sfx } from '../audio.js';
import { t, lang } from '../i18n.js';
import { store } from '../store.js';
import { esc, starsFromMistakes } from '../util.js';

// Level type "talk": everyday conversation, checked by the child. Timtim asks, the child
// answers out loud and records it, then hears their own voice next to the right way and
// marks it ✅ or 🔁. Recordings live only in memory and are thrown away after each turn.

const RECORD_MS = 8000;
const RECORD_MS_OPEN = 30000; // free speaking gets more time

// "{name}" → the child's name; "[जाता|जाती]" → the boy/girl form the child picked.
export function personalise(text, { forSpeech = false } = {}) {
  const { name, talkForm } = store.get();
  return text
    .replace(/\{name\}/g, name || '')
    .replace(/\[([^|\]]+)\|([^\]]+)\]/g, (_, boy, girl) =>
      talkForm === 'f' ? girl : talkForm === 'm' || forSpeech ? boy : `${boy}/${girl}`);
}

const canRecord = () =>
  !!(window.isSecureContext && navigator.mediaDevices?.getUserMedia && window.MediaRecorder);

export default function talk(kit, level) {
  const turns = level.turns;
  let i = 0;
  let firstTry = 0;
  let micOk = canRecord();
  let stream = null;
  let recorder = null;
  let clipUrl = null;
  let clip = null;

  function release() {
    try {
      if (recorder && recorder.state === 'recording') recorder.stop();
    } catch (e) { /* already stopped */ }
    if (stream) stream.getTracks().forEach((tr) => tr.stop());
    stream = null;
    if (clip) clip.pause();
    clip = null;
    if (clipUrl) URL.revokeObjectURL(clipUrl);
    clipUrl = null;
  }
  kit.onCleanup(release);

  function show() {
    const turn = turns[i];
    const ask = personalise(turn.a);
    const reply = personalise(turn.r);
    const replySpoken = personalise(turn.r, { forSpeech: true });
    let tries = 0;
    let hinted = false;
    release();

    kit.body.innerHTML = `
      <p class="q-prompt">${t('turnN', { n: i + 1, total: turns.length })}</p>
      <div class="bubble talk-ask">
        <span class="talk-who">📡 टिमटिम</span>
        ${turn.pic ? `<span class="talk-pic" aria-hidden="true">${turn.pic}</span>` : ''}
        <span class="deva talk-line">${esc(ask)}</span>
        ${lang() === 'en' ? `<small class="gloss-line">${esc(turn.ae)}</small>` : ''}
        <button class="say-btn sm" type="button" data-ask>🔊</button>
      </div>
      <div class="q-card talk-card" data-panel></div>`;
    kit.foot.innerHTML = '';
    const panel = kit.body.querySelector('[data-panel]');
    kit.body.querySelector('[data-ask]').onclick = () => speak(ask);
    kit.later(() => speak(ask), 300);

    const modelHtml = () => `
      <div class="talk-model">
        <span class="deva talk-line">${esc(reply)}</span>
        ${lang() === 'en' ? `<small class="gloss-line">${esc(personalise(turn.re))}</small>` : ''}
      </div>`;

    const goals = (turn.use || []).map((w) => personalise(w));
    // Cadet: hint any time. Pilot: hint only after one try. Commander / open turns: never.
    const hintAllowed = () => !turn.open && (level.help === 'full' || (level.help === 'afterTry' && tries > 0));

    function paintAnswer() {
      panel.innerHTML = `
        <p class="q-prompt">${t('yourTurn')}</p>
        ${turn.open ? `
          <small class="muted">${t('atLeast')} ${t('goalWords')}</small>
          <div class="goal-chips">${goals.map((g) => `<span class="goal deva">${esc(g)}</span>`).join('')}</div>` : ''}
        ${hinted ? modelHtml() : ''}
        <div class="talk-actions">
          <button class="btn btn-primary btn-big" type="button" data-rec>${micOk ? `🎙️ ${t('speakNow')}` : `🗣️ ${t('iSaidIt')}`}</button>
          ${!hinted && hintAllowed() ? `<button class="btn btn-ghost btn-sm" type="button" data-hint>💡 ${t('showAnswer')}</button>` : ''}
          ${!turn.open && level.help === 'afterTry' && tries === 0 ? `<small class="muted">${t('hintAfterTry')}</small>` : ''}
        </div>
        ${micOk ? '' : `<small class="muted">${t('noMic')}</small>`}`;
      const hint = panel.querySelector('[data-hint]');
      if (hint) hint.onclick = () => { hinted = true; paintAnswer(); speak(replySpoken); };
      panel.querySelector('[data-rec]').onclick = () => (micOk ? startRecording() : paintCompare());
    }

    async function startRecording() {
      stopSpeech();
      try {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      } catch (e) {
        micOk = false; // permission refused or no microphone: carry on without recording
        paintCompare();
        return;
      }
      const chunks = [];
      recorder = new MediaRecorder(stream);
      recorder.ondataavailable = (ev) => { if (ev.data.size) chunks.push(ev.data); };
      recorder.onstop = () => {
        if (stream) stream.getTracks().forEach((tr) => tr.stop());
        stream = null;
        if (!chunks.length) return paintCompare();
        clipUrl = URL.createObjectURL(new Blob(chunks, { type: recorder.mimeType || 'audio/webm' }));
        paintCompare();
      };
      recorder.start();
      panel.innerHTML = `
        <p class="q-prompt">${t('listening')}</p>
        <button class="btn btn-big rec-live" type="button" data-stop>⏹️ ${t('stopRec')}</button>`;
      const stopBtn = panel.querySelector('[data-stop]');
      const stop = () => { if (recorder.state === 'recording') recorder.stop(); };
      stopBtn.onclick = stop;
      kit.later(stop, turn.open ? RECORD_MS_OPEN : RECORD_MS);
    }

    function paintCompare() {
      const used = new Set();
      panel.innerHTML = `
        ${turn.open ? `
          <p class="q-prompt">${t('tickUsed')}</p>
          <div class="goal-chips">${goals.map((g, k) => `<button class="goal deva" type="button" data-goal="${k}" aria-pressed="false">${esc(g)}</button>`).join('')}</div>
          <small class="muted">${t('sampleAnswer')}</small>` : ''}
        ${modelHtml()}
        ${turn.tip ? `<div class="talk-tip">✏️ <b>${t('tipLabel')}</b> <span class="deva">${esc(lang() === 'en' ? turn.tip[1] : turn.tip[0])}</span></div>` : ''}
        <div class="talk-actions row">
          ${clipUrl ? `<button class="btn btn-ghost btn-sm" type="button" data-mine>▶️ ${t('myVoice')}</button>` : ''}
          <button class="btn btn-ghost btn-sm" type="button" data-model>🔊 ${t('rightWay')}</button>
        </div>
        <p class="q-prompt">${t('didYouSay')}</p>
        <div class="talk-actions row">
          <button class="btn btn-primary" type="button" data-ok>✅ ${t('saidIt')}</button>
          <button class="btn btn-ghost" type="button" data-again>🔁 ${t('tryAgainSay')}</button>
        </div>`;
      panel.querySelectorAll('[data-goal]').forEach((b) => {
        b.onclick = () => {
          const k = Number(b.dataset.goal);
          if (used.has(k)) used.delete(k); else used.add(k);
          b.setAttribute('aria-pressed', String(used.has(k)));
          sfx('tap');
        };
      });
      const mine = panel.querySelector('[data-mine]');
      if (mine) mine.onclick = () => { stopSpeech(); clip = new Audio(clipUrl); clip.play().catch(() => {}); };
      panel.querySelector('[data-model]').onclick = () => { if (clip) clip.pause(); speak(replySpoken); };
      panel.querySelector('[data-ok]').onclick = () => {
        // In free speaking, missing goal words costs a little (the child's own count).
        if (turn.open && used.size < goals.length) kit.stats.mistakes += 1;
        if (tries === 0 && (!turn.open || used.size === goals.length)) firstTry++;
        kit.right();
        release();
        kit.later(next, 700);
      };
      panel.querySelector('[data-again]').onclick = () => {
        tries++;
        kit.stats.mistakes++; // a retry costs a little, but no buzzer: it's the child's own call
        sfx('tap');
        release();
        hinted = true;
        paintAnswer();
      };
      // Play the child's own take first, then the right way, so they can hear the difference.
      if (clipUrl) {
        clip = new Audio(clipUrl);
        clip.onended = () => kit.later(() => speak(replySpoken), 300);
        clip.play().catch(() => speak(replySpoken));
      } else {
        speak(replySpoken);
      }
    }

    paintAnswer();
  }

  function next() {
    i++;
    kit.progress(i / turns.length);
    if (i < turns.length) return show();
    kit.finish({
      stars: starsFromMistakes(kit.stats.mistakes),
      correct: firstTry,
      total: turns.length,
      score: firstTry,
    });
  }

  show();
}
