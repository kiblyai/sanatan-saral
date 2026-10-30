// All progress lives in this browser only. Nothing is sent anywhere.
const KEY = 'hsm.v1';

function defaults() {
  return {
    name: '',
    lang: 'en',
    sound: true,
    speech: true,
    unlockAll: false, // parents can open every level (settings)
    introSeen: false,
    book: null, // 'b1'–'b4', chosen on the book picker
    talkForm: null, // 'm' or 'f': which verb forms Talk Station answers use (जाता / जाती)
    levels: {}, // levelId -> { stars, best, plays }
    badges: [], // badge ids in the order they were earned
    days: [], // 'YYYY-MM-DD' for every day the child played
  };
}

function load() {
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) return { ...defaults(), ...JSON.parse(raw) };
  } catch (e) {
    // Storage blocked (private mode etc.): the app still runs, it just won't remember.
  }
  return defaults();
}

let state = load();

function persist() {
  try {
    localStorage.setItem(KEY, JSON.stringify(state));
  } catch (e) {
    /* see load() */
  }
}

function dayKey(d = new Date()) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

export const store = {
  get: () => state,

  set(patch) {
    Object.assign(state, patch);
    persist();
  },

  level: (id) => state.levels[id] || { stars: 0, best: 0, plays: 0 },

  saveLevel(id, { stars, score }) {
    const prev = store.level(id);
    state.levels[id] = {
      stars: Math.max(prev.stars, stars),
      best: Math.max(prev.best, score || 0),
      plays: prev.plays + 1,
    };
    persist();
  },

  // Returns only the badges that are new this time.
  addBadges(ids) {
    const fresh = [...new Set(ids)].filter((id) => !state.badges.includes(id));
    if (fresh.length) {
      state.badges.push(...fresh);
      persist();
    }
    return fresh;
  },

  markToday() {
    const today = dayKey();
    if (!state.days.includes(today)) {
      state.days.push(today);
      persist();
    }
  },

  totalStars: () => Object.values(state.levels).reduce((sum, l) => sum + l.stars, 0),

  // Consecutive days played, counting back from today (or yesterday, so the streak
  // doesn't vanish in the morning before the child has played).
  dayStreak() {
    const days = new Set(state.days);
    const d = new Date();
    if (!days.has(dayKey(d))) d.setDate(d.getDate() - 1);
    let n = 0;
    while (days.has(dayKey(d))) {
      n++;
      d.setDate(d.getDate() - 1);
    }
    return n;
  },

  reset() {
    state = { ...defaults(), lang: state.lang };
    persist();
  },
};
