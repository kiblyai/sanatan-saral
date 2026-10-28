export function shuffle(list) {
  const a = [...list];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export const sample = (list, n) => shuffle(list).slice(0, n);

export const pickOne = (list) => list[Math.floor(Math.random() * list.length)];

export function esc(value) {
  return String(value).replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[c]));
}

// Same rule for every level: 0–1 slips = 3 stars, 2–3 = 2 stars, more = 1 star.
export const starsFromMistakes = (m) => (m <= 1 ? 3 : m <= 3 ? 2 : 1);

export function starRow(stars, max = 3) {
  let html = '';
  for (let i = 1; i <= max; i++) html += `<span class="${i <= stars ? 'on' : 'off'}">★</span>`;
  return `<span class="stars-row" aria-label="${stars}/${max}">${html}</span>`;
}
