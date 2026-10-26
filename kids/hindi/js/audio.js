import { store } from './store.js';

// ---- Read-aloud: the device's own Hindi voice (free, quality varies by phone) ----
const synth = 'speechSynthesis' in window ? window.speechSynthesis : null;
let hindiVoice = null;

function findVoice() {
  if (!synth) return;
  const hindi = synth.getVoices().filter((v) => /^hi([-_]|$)/i.test(v.lang));
  // Prefer voices that run on the device, so words aren't sent to an online service.
  hindiVoice = hindi.find((v) => v.localService) || hindi[0] || null;
}

if (synth) {
  findVoice();
  synth.onvoiceschanged = findVoice;
}

// iPhones only allow speech and sound that start from a tap. The first touch anywhere
// unlocks both, so later automatic read-aloud (a new question, a new page) can play.
function unlock() {
  if (synth) synth.speak(new SpeechSynthesisUtterance(''));
  audioCtx();
  window.removeEventListener('pointerdown', unlock, true);
}
window.addEventListener('pointerdown', unlock, true);

export const voice = {
  supported: !!synth,
  available: () => !!hindiVoice,
  name: () => (hindiVoice ? hindiVoice.name : ''),
  online: () => !!hindiVoice && !hindiVoice.localService,
};

export function speak(text, { force = false } = {}) {
  if (!synth || !hindiVoice) return;
  if (!force && !store.get().speech) return;
  synth.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.voice = hindiVoice;
  u.lang = hindiVoice.lang;
  u.rate = 0.85;
  synth.speak(u);
}

export function stopSpeech() {
  if (synth) synth.cancel();
}

// ---- Sound effects: generated tones, no audio files to download ----
let ctx = null;

function audioCtx() {
  if (!ctx) {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    ctx = new AC();
  }
  if (ctx.state === 'suspended') ctx.resume();
  return ctx;
}

function tone(freq, start, dur, type = 'sine', vol = 0.15) {
  const c = audioCtx();
  if (!c) return;
  const osc = c.createOscillator();
  const gain = c.createGain();
  const t0 = c.currentTime + start;
  osc.type = type;
  osc.frequency.value = freq;
  gain.gain.setValueAtTime(0.0001, t0);
  gain.gain.exponentialRampToValueAtTime(vol, t0 + 0.02);
  gain.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
  osc.connect(gain).connect(c.destination);
  osc.start(t0);
  osc.stop(t0 + dur + 0.05);
}

const SOUNDS = {
  good: () => { tone(660, 0, 0.15); tone(880, 0.1, 0.2); },
  bad: () => { tone(220, 0, 0.22, 'triangle', 0.12); tone(170, 0.12, 0.25, 'triangle', 0.1); },
  tap: () => tone(520, 0, 0.08, 'sine', 0.08),
  bonus: () => { tone(988, 0, 0.1); tone(1319, 0.08, 0.18); },
  win: () => [523, 659, 784, 1047].forEach((f, i) => tone(f, i * 0.12, 0.3, 'triangle', 0.14)),
};

export function sfx(name) {
  if (!store.get().sound) return;
  try {
    SOUNDS[name]?.();
  } catch (e) {
    /* audio not available */
  }
}
