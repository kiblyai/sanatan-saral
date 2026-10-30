import { store } from './store.js';
import { t, pick, lang } from './i18n.js';
import { speak, sfx, stopSpeech, voice } from './audio.js';
import { ALL_BADGES, BADGES, BOOKS, TALK, VALUE_BADGES, PLANETS, findLevel } from './content.js';
import { esc, starRow } from './util.js';
import { createKit } from './games/kit.js';
import quiz from './games/quiz.js';
import build from './games/build.js';
import sort from './games/sort.js';
import match from './games/match.js';
import meteor from './games/meteor.js';
import storyGame from './games/story.js';
import spot from './games/spot.js';
import order from './games/order.js';
import talk from './games/talk.js';

const GAMES = { quiz, build, sort, match, meteor, spot, order, talk, story: storyGame };
const app = document.getElementById('app');
let cleanup = null;
let lastResult = null;
let installEvent = null;

// Inside the Claude app the page runs in a frame: no service worker, no home-screen install.
const embedded = (() => {
  try {
    return window.self !== window.top;
  } catch (e) {
    return true;
  }
})();

const TIMTIM = (cls = '') => `
  <svg class="timtim ${cls}" viewBox="0 0 100 100" aria-hidden="true">
    <path d="M50 8 L62.9 36.2 L93.8 39.8 L70.9 60.8 L77 91.2 L50 76 L23 91.2 L29.1 60.8 L6.2 39.8 L37.1 36.2 Z"
      fill="#ffd23f" stroke="#1a1446" stroke-width="5" stroke-linejoin="round"/>
    <circle cx="40" cy="52" r="6.5" fill="#fff" stroke="#1a1446" stroke-width="2"/>
    <circle cx="60" cy="52" r="6.5" fill="#fff" stroke="#1a1446" stroke-width="2"/>
    <circle cx="41.5" cy="53" r="3.4" fill="#1a1446"/><circle cx="61.5" cy="53" r="3.4" fill="#1a1446"/>
    <circle cx="32" cy="63" r="3.6" fill="#ff9ecb"/><circle cx="68" cy="63" r="3.6" fill="#ff9ecb"/>
    <path d="M42 62 Q50 72 58 62" fill="#ff5d8f" stroke="#1a1446" stroke-width="2.5" stroke-linecap="round"/>
  </svg>`;

// ---------- helpers ----------

// Routes are plain anchors like #galaxy or #planet.budh.
function go(path, replace = false) {
  const hash = `#${path.replace('/', '.')}`;
  if (replace) location.replace(hash);
  else location.hash = hash;
}

// Levels open one after another. On book planets every chapter's first level is open,
// so a child can jump to the chapter being taught in class.
function isUnlocked(planet, index) {
  if (index === 0 || store.get().unlockAll) return true;
  const level = planet.levels[index];
  const prev = planet.levels[index - 1];
  if (level.rank) return talkRankOpen(level.rank);
  if (level.ch && level.ch !== prev.ch) return true;
  return store.level(prev.id).stars > 0;
}

// A talk level opens once RANK_UNLOCK conversations in the level below are done.
function talkRankOpen(rankId) {
  const i = TALK.ranks.findIndex((r) => r.id === rankId);
  if (i <= 0 || store.get().unlockAll) return true;
  const below = TALK.ranks[i - 1].scenes.filter((s) => store.level(s.id).stars > 0).length;
  return below >= TALK.rankUnlock;
}

// Today's conversation rotates daily among the talk levels the child has unlocked.
function todaysTalk() {
  const open = TALK.levels.filter((l) => talkRankOpen(l.rank));
  return open[Math.floor(Date.now() / 86400000) % open.length];
}

const chapterDone = (planet, ch) => planet.levels.filter((l) => l.ch === ch).every((l) => store.level(l.id).stars > 0);

const planetStars = (planet) => planet.levels.reduce((sum, l) => sum + store.level(l.id).stars, 0);

const planetStyle = (p) => `--c1:${p.c1};--c2:${p.c2}`;

function langToggle() {
  const l = lang();
  return `
    <div class="lang-toggle" role="group" aria-label="Language / भाषा">
      <button type="button" data-lang="en" aria-pressed="${l === 'en'}">EN</button>
      <button type="button" data-lang="hi" aria-pressed="${l === 'hi'}">हिं</button>
    </div>`;
}

function bindCommon() {
  app.querySelectorAll('[data-lang]').forEach((b) => {
    b.onclick = () => {
      store.set({ lang: b.dataset.lang });
      sfx('tap');
      render();
    };
  });
}

// ---------- screens ----------

function welcome() {
  const s = store.get();
  app.innerHTML = `
    <section class="screen welcome">
      <div class="top-right">${langToggle()}</div>
      <div class="hero">
        ${TIMTIM('float big')}
        <h1 class="title">${t('appName')}</h1>
        <p class="tagline">${t('tagline')}</p>
      </div>
      <form class="card name-form" novalidate>
        <label for="nm">${t('yourName')}</label>
        <input id="nm" maxlength="20" autocomplete="off" autocapitalize="words" spellcheck="false"
          placeholder="${t('namePlaceholder')}" value="${esc(s.name)}">
        <button class="btn btn-primary btn-big" type="submit">🚀 ${t('start')}</button>
      </form>
      <p class="fine">🔒 ${t('privacyShort')}</p>
    </section>`;
  const input = app.querySelector('#nm');
  app.querySelector('form').onsubmit = (e) => {
    e.preventDefault();
    const name = input.value.trim().slice(0, 20);
    if (!name) {
      input.classList.add('shake');
      input.focus();
      setTimeout(() => input.classList.remove('shake'), 400);
      return;
    }
    store.set({ name });
    sfx('tap');
    go(!s.introSeen ? 'story' : s.book ? 'galaxy' : 'books');
  };
}

function story() {
  const lines = [t('story1', { name: esc(store.get().name) }), t('story2'), t('story3')];
  let i = 0;
  function paint() {
    app.innerHTML = `
      <section class="screen story">
        <div class="story-top"><button class="btn btn-ghost btn-sm" type="button" data-skip>${t('skip')}</button></div>
        <div class="story-art" aria-hidden="true">${['🚀', '🌪️', '⛽'][i]}</div>
        <div class="guide">
          ${TIMTIM('float')}
          <div class="bubble">${lines[i]}</div>
        </div>
        <div class="dots" aria-hidden="true">${lines.map((_, k) => `<span class="${k === i ? 'on' : ''}"></span>`).join('')}</div>
        <button class="btn btn-primary btn-big" type="button" data-next>${i < lines.length - 1 ? `${t('next')} →` : `🚀 ${t('letsGo')}`}</button>
      </section>`;
    if (lang() === 'hi') speak(lines[i].replace(/<[^>]+>/g, ''));
    app.querySelector('[data-skip]').onclick = finish;
    app.querySelector('[data-next]').onclick = () => {
      sfx('tap');
      if (++i < lines.length) paint();
      else finish();
    };
  }
  function finish() {
    store.set({ introSeen: true });
    go(store.get().book ? 'galaxy' : 'books', true);
  }
  paint();
}

const currentBook = () => BOOKS.find((b) => b.id === store.get().book) || BOOKS[2];
const bookStars = (b) => b.planets.reduce((sum, p) => sum + (p.levels ? planetStars(p) : 0), 0);
const bookMax = (b) => b.planets.reduce((sum, p) => sum + (p.levels ? p.levels.length * 3 : 0), 0);

// Pick a book level (Book 1–4). Each book has its own galaxy of planets.
function books() {
  const cur = store.get().book;
  app.innerHTML = `
    <section class="screen books">
      <header class="topbar">
        ${store.get().book ? `<a class="icon-btn" href="#galaxy" aria-label="${t('back')}">←</a>` : '<span></span>'}
        <h1 class="h-title">${t('pickBook')}</h1>
        <div class="top-right">${langToggle()}</div>
      </header>
      <div class="guide">${TIMTIM('float')}<div class="bubble">${t('pickBookHelp')}</div></div>
      <div class="book-grid">
        ${BOOKS.map((b) => `
          <button class="book-card ${b.id === cur ? 'current' : ''}" type="button" data-book="${b.id}" style="--c1:${b.c1}">
            <span class="book-ico" aria-hidden="true">${b.icon}</span>
            <b>${t('bookN', { n: b.n })}</b>
            <small>${pick(b.sub)}</small>
            <span class="chip">⭐ ${bookStars(b)} / ${bookMax(b)}</span>
          </button>`).join('')}
      </div>
    </section>`;
  app.querySelectorAll('[data-book]').forEach((el) => {
    el.onclick = () => {
      store.set({ book: el.dataset.book });
      sfx('tap');
      go('galaxy');
    };
  });
}

function galaxy() {
  const s = store.get();
  const book = currentBook();
  const streak = store.dayStreak();
  app.innerHTML = `
    <section class="screen galaxy">
      <header class="topbar">
        <div class="hello">${TIMTIM('mini')}<div><small>${t('hello')}</small><b>${esc(s.name)}</b></div></div>
        <div class="chips">
          <span class="chip" title="${t('stars')}">⭐ ${store.totalStars()}</span>
          ${streak > 1 ? `<span class="chip">🔥 ${streak}</span>` : ''}
        </div>
      </header>
      <div class="row-actions">
        <div class="row-right">
          <a class="btn btn-primary btn-sm" href="#books">${book.icon} ${t('bookN', { n: book.n })}</a>
          <a class="btn btn-ghost btn-sm" href="#badges">🏅 <span class="count">${s.badges.length}/${ALL_BADGES.length}</span></a>
        </div>
        <div class="row-right">
          ${langToggle()}
          <a class="icon-btn" href="#parents" aria-label="${t('parents')}" title="${t('parents')}">⚙️</a>
        </div>
      </div>
      <a class="talk-banner" href="#planet.talk">
        <span class="tb-ico" aria-hidden="true">🎙️</span>
        <span class="tb-text"><b>${pick(TALK.name)}</b><small>${t('todayTalk')}: ${todaysTalk().icon} <span class="deva">${pick(todaysTalk().title)}</span></small></span>
        <span class="tb-go" aria-hidden="true">→</span>
      </a>
      <h2 class="section-title">${t('galaxy')}</h2>
      <ol class="planet-path">
        ${book.planets.map((p, i) => {
          const side = i % 2 ? 'right' : 'left';
          if (p.soon) {
            return `
              <li class="pp soon ${side}">
                <div class="planet" style="${planetStyle(p)}"><span class="q" aria-hidden="true">💤</span></div>
                <div class="pp-label"><b>${pick(p.name)}</b><small>${pick(p.sub)}</small><small>🔒 ${t('comingSoon')}</small></div>
              </li>`;
          }
          return `
            <li class="pp ${side}">
              <a class="pp-link" href="#planet.${p.id}">
                <div class="planet ring" style="${planetStyle(p)}"></div>
                <div class="pp-label">
                  <b>${pick(p.name)}</b><small>${pick(p.sub)}</small>
                  <span class="chip">⭐ ${planetStars(p)} / ${p.levels.length * 3}</span>
                </div>
              </a>
            </li>`;
        }).join('')}
      </ol>
    </section>`;
}

function planet(pid) {
  const p = PLANETS.find((x) => x.id === pid && !x.soon);
  if (!p) return go('galaxy', true);
  app.innerHTML = `
    <section class="screen planet-screen">
      <header class="topbar">
        <a class="icon-btn" href="#galaxy" aria-label="${t('back')}">←</a>
        <h1 class="h-title">${pick(p.name)}</h1>
        <span class="chip">⭐ ${planetStars(p)}/${p.levels.length * 3}</span>
      </header>
      ${p.talk ? `
        <div class="guide">${TIMTIM('float')}<div class="bubble">${t('talkIntro')}</div></div>
        <div class="card form-pick">
          <b>${t('formAsk')}</b>
          <div class="lang-toggle" role="group">
            <button type="button" data-form="m" aria-pressed="${store.get().talkForm === 'm'}">👦 मैं जाता हूँ</button>
            <button type="button" data-form="f" aria-pressed="${store.get().talkForm === 'f'}">👧 मैं जाती हूँ</button>
          </div>
        </div>` : `<div class="planet big ring" style="${planetStyle(p)}"></div>`}
      <p class="muted center">${pick(p.sub)}</p>
      ${p.talk
        ? p.ranks.map((rank, ri) => `
          <section class="chapter">
            <div class="ch-head">
              <div>
                <small>${t('level')} ${ri + 1} · ${pick(rank.sub)}</small>
                <h2>${rank.icon} ${pick(rank.name)}</h2>
              </div>
              ${talkRankOpen(rank.id) ? '' : `<span class="value-chip">🔒 ${t('rankLocked', { n: p.rankUnlock, prev: pick(p.ranks[ri - 1].name) })}</span>`}
            </div>
            ${levelList(p, (lv) => lv.rank === rank.id)}
          </section>`).join('')
        : p.book
        ? p.chapters.map((ch) => `
          <section class="chapter">
            <div class="ch-head">
              <div>
                <small>${t('chapter')} ${ch.n} · <span class="deva">${ch.genre}</span></small>
                <h2 class="deva">${ch.title}</h2>
              </div>
              <span class="value-chip ${chapterDone(p, ch) ? 'won' : ''}" title="${t('valueLabel')}">
                ${ch.valueIcon} <span class="deva">${pick(ch.value)}</span>
              </span>
            </div>
            ${levelList(p, (lv) => lv.ch === ch)}
          </section>`).join('')
        : levelList(p, () => true)}
    </section>`;
}

function bindTalkForm() {
  app.querySelectorAll('[data-form]').forEach((b) => {
    b.onclick = () => {
      store.set({ talkForm: b.dataset.form });
      sfx('tap');
      render();
    };
  });
}

function levelList(p, keep) {
  return `
    <ol class="level-path">
      ${p.levels.map((lv, i) => {
        if (!keep(lv)) return '';
        const open = isUnlocked(p, i);
        const st = store.level(lv.id).stars;
        const cls = [open ? '' : 'locked', st > 0 ? 'done' : '', lv.boss ? 'boss' : ''].join(' ');
        const inner = `
          <span class="ln-btn" aria-hidden="true">${open ? lv.icon : '🔒'}</span>
          <span class="ln-label">
            <small>${lv.ch ? '' : `${t('level')} ${i + 1} · `}<span class="deva">${lv.tag}</span></small>
            <b>${pick(lv.title)}</b>
            ${lv.type === 'talk' && lv.id === todaysTalk().id ? `<small class="today">⭐ ${t('todayTalk')}</small>` : ''}
            ${open ? starRow(st) : `<small>${t('locked')}</small>`}
          </span>`;
        return `<li class="ln ${cls}">${open ? `<a class="ln-link" href="#level.${lv.id}">${inner}</a>` : `<div class="ln-link">${inner}</div>`}</li>`;
      }).join('')}
    </ol>`;
}

function levelIntro(lid) {
  const found = findLevel(lid);
  if (!found || !isUnlocked(found.planet, found.index)) return go('galaxy', true);
  const { planet: p, level: lv, index } = found;
  const best = store.level(lid);
  const howText = pick(lv.how);
  app.innerHTML = `
    <section class="screen intro">
      <header class="topbar">
        <a class="icon-btn" href="#planet.${p.id}" aria-label="${t('back')}">←</a>
        <span class="chip">${lv.ch ? `${t('chapter')} ${lv.ch.n} · <span class="deva">${lv.ch.title}</span>` : `${t('level')} ${index + 1}`}</span>
      </header>
      <div class="intro-hero">
        <span class="intro-ico" aria-hidden="true">${lv.icon}</span>
        <h1>${pick(lv.title)}</h1>
        <span class="tag deva">${lv.tag}</span>
      </div>
      <div class="guide">
        ${TIMTIM('float')}
        <div class="bubble">
          ${howText}
          ${lang() === 'hi' && voice.available() ? `<button class="say-btn sm" type="button" data-say>🔊</button>` : ''}
        </div>
      </div>
      ${best.plays ? `<p class="muted center">${t('yourBest')}: ${starRow(best.stars)}</p>` : ''}
      <a class="btn btn-primary btn-big" href="#play.${lid}">▶ ${t('play')}</a>
    </section>`;
  const say = app.querySelector('[data-say]');
  if (say) say.onclick = () => speak(howText);
}

function play(lid) {
  const found = findLevel(lid);
  if (!found || !isUnlocked(found.planet, found.index)) return go('galaxy', true);
  const { planet: p, level: lv } = found;
  app.innerHTML = `
    <section class="game type-${lv.type}">
      <header class="game-top">
        <a class="icon-btn" href="#planet.${p.id}" aria-label="${t('quit')}" title="${t('quit')}">✕</a>
        <div class="fuel" role="progressbar" aria-label="${lv.type === 'meteor' ? t('timeLeft') : t('fuel')}"
          aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
          <div class="fuel-fill"></div>
        </div>
        <div class="streak" title="${t('streak')}" aria-label="${t('streak')}"><span aria-hidden="true">🔥</span><b>0</b></div>
      </header>
      <div class="game-body"></div>
      <div class="game-foot" aria-live="polite"></div>
    </section>`;
  const kit = createKit(app.querySelector('.game'));
  let finished = false;
  kit.finish = (res) => {
    if (finished) return;
    finished = true;
    kit.cleanup();
    onFinish(found, res, kit.stats);
  };
  cleanup = () => kit.cleanup();
  store.markToday();
  GAMES[lv.type](kit, lv);
}

function onFinish({ planet: p, level: lv }, res, stats) {
  store.saveLevel(lv.id, res);
  const ids = [];
  if (res.stars > 0) ids.push('first');
  if (res.stars === 3) ids.push('perfect');
  if (stats.bestStreak >= 5) ids.push('streak5');
  if (stats.bestStreak >= 10) ids.push('streak10');
  if (store.level('shabd-1').stars === 3 && store.level('shabd-2').stars === 3) ids.push('matra');
  if (lv.type === 'meteor' && res.score >= 15) ids.push('meteor15');
  if (p.levels.every((l) => store.level(l.id).stars > 0)) ids.push('planet');
  if (lv.ch && chapterDone(p, lv.ch)) ids.push(`value-${lv.ch.id}`);
  if (lv.type === 'talk' && TALK.levels.filter((l) => store.level(l.id).stars > 0).length >= 5) ids.push('talk5');
  if (store.get().days.length >= 3) ids.push('days3');
  lastResult = { lid: lv.id, res, earned: store.addBadges(ids) };
  go(`result/${lv.id}`, true);
}

function result(lid) {
  const found = findLevel(lid);
  if (!found || !lastResult || lastResult.lid !== lid) return go(found ? `level/${lid}` : 'galaxy', true);
  const { planet: p, level: lv, index } = found;
  const { res, earned } = lastResult;
  const nextLv = p.levels[index + 1];
  const heading = t(['r0', 'r1', 'r2', 'r3'][res.stars]);
  const scoreLine = lv.type === 'meteor'
    ? t('meteorScore', { n: res.score, best: store.level(lid).best })
    : t('firstTry', { c: res.correct, n: res.total });
  const colors = ['#ffcf33', '#5ad1ff', '#2ee59d', '#ff8fa3', '#9b7bff'];
  const confetti = res.stars > 0
    ? Array.from({ length: 28 }, (_, k) => `<i style="left:${(k * 37) % 100}%;background:${colors[k % 5]};animation-delay:${(k % 7) * 0.12}s;animation-duration:${2.2 + (k % 5) * 0.3}s"></i>`).join('')
    : '';

  app.innerHTML = `
    <section class="screen result">
      <div class="confetti" aria-hidden="true">${confetti}</div>
      ${TIMTIM(`float big ${res.stars ? '' : 'sad'}`)}
      <h1>${heading}</h1>
      <div class="result-stars" aria-label="${res.stars} / 3 ${t('stars')}">
        ${[1, 2, 3].map((n) => `<span class="rstar ${n <= res.stars ? 'on' : ''}" style="--d:${0.2 + n * 0.25}s">★</span>`).join('')}
      </div>
      <p class="score-line">${scoreLine}</p>
      <p class="story-line">${res.stars > 0 ? pick(lv.win) : t('r0line')}</p>
      ${earned.length ? `
        <div class="new-badges">
          <h2>${t('newBadge')}</h2>
          <div class="nb-row">${earned.map((id) => {
            const b = ALL_BADGES.find((x) => x.id === id);
            return `<div class="nb"><span class="b-ico">${b.icon}</span><b>${pick(b.name)}</b></div>`;
          }).join('')}</div>
        </div>` : ''}
      <div class="actions">
        ${res.stars > 0 && nextLv ? `<a class="btn btn-primary btn-big" href="#level.${nextLv.id}">${t('nextLevel')} →</a>` : ''}
        ${res.stars > 0 && !nextLv ? `<a class="btn btn-primary btn-big" href="#galaxy">🪐 ${t('backToMap')}</a>` : ''}
        <a class="btn ${res.stars > 0 ? 'btn-ghost' : 'btn-primary btn-big'}" href="#play.${lid}">↻ ${t('playAgain')}</a>
        <a class="btn btn-ghost" href="#planet.${p.id}">${t('backToPlanet')}</a>
      </div>
    </section>`;
  sfx(res.stars > 0 ? 'win' : 'bad');
  if (res.stars > 0) setTimeout(() => speak('शाबाश!'), 600);
}

function badges() {
  const s = store.get();
  app.innerHTML = `
    <section class="screen badges">
      <header class="topbar">
        <a class="icon-btn" href="#galaxy" aria-label="${t('back')}">←</a>
        <h1 class="h-title">🏅 ${t('badges')}</h1>
        <span class="chip">${s.badges.length}/${ALL_BADGES.length}</span>
      </header>
      <div class="badge-grid">${BADGES.map(badgeCard).join('')}</div>
      <h2 class="section-title">${t('valueBadges')}</h2>
      <div class="badge-grid">${VALUE_BADGES.map(badgeCard).join('')}</div>
    </section>`;
}

function badgeCard(b) {
  const got = store.get().badges.includes(b.id);
  return `
    <div class="badge ${got ? '' : 'locked'}">
      <span class="b-ico" aria-hidden="true">${got ? b.icon : '🔒'}</span>
      <b class="${b.ch ? 'deva' : ''}">${pick(b.name)}</b>
      <small>${pick(b.desc)}</small>
    </div>`;
}

function parents() {
  const s = store.get();
  const ios = !embedded && /iphone|ipad|ipod/i.test(navigator.userAgent) && !navigator.standalone;
  const live = PLANETS.filter((p) => !p.soon);
  let voiceHtml;
  if (voice.available()) {
    voiceHtml = `<p class="muted">✅ ${esc(t('voiceOk', { v: voice.name() }))}${voice.online() ? `<br>${t('voiceOnline')}` : ''}</p>
      <button class="btn btn-ghost btn-sm" type="button" data-test>🔊 ${t('testVoice')}</button>`;
  } else {
    voiceHtml = `<p class="muted">⚠️ ${t('voiceMissing')}</p>`;
  }

  app.innerHTML = `
    <section class="screen parents">
      <header class="topbar">
        <a class="icon-btn" href="${s.name ? '#galaxy' : '#welcome'}" aria-label="${t('back')}">←</a>
        <h1 class="h-title">${t('parents')}</h1>
        <span></span>
      </header>

      <div class="card">
        <h2>${t('settings')}</h2>
        <div class="setting"><span>${t('language')}</span>${langToggle()}</div>
        <label class="setting"><span>${t('sound')}</span><input type="checkbox" class="switch" data-set="sound" ${s.sound ? 'checked' : ''}></label>
        <label class="setting"><span>${t('readAloud')}</span><input type="checkbox" class="switch" data-set="speech" ${s.speech ? 'checked' : ''}></label>
        <label class="setting"><span>🔓 ${t('unlockAll')}</span><input type="checkbox" class="switch" data-set="unlockAll" ${s.unlockAll ? 'checked' : ''}></label>
        <p class="muted">${t('unlockAllHint')}</p>
        ${voiceHtml}
        <form class="setting name-row" data-name>
          <label for="pn">${t('childName')}</label>
          <div class="inline"><input id="pn" maxlength="20" value="${esc(s.name)}" autocomplete="off"><button class="btn btn-ghost btn-sm" type="submit">${t('save')}</button></div>
        </form>
      </div>

      <div class="card">
        <h2>${t('progress')}</h2>
        ${live.map((p) => `
          <h3>${pick(p.name)}</h3>
          <table class="progress-table">
            ${p.levels.map((lv, i) => {
              const r = store.level(lv.id);
              const label = lv.ch ? `${t('chapter')} ${lv.ch.n} · ${pick(lv.title)}` : `${i + 1}. ${pick(lv.title)}`;
              return `<tr><td>${label} <small class="deva">(${lv.tag})</small></td>
                <td>${r.plays ? starRow(r.stars) : `<small class="muted">${t('notPlayed')}</small>`}</td></tr>`;
            }).join('')}
          </table>`).join('')}
        <p class="muted">⭐ ${store.totalStars()} · 🏅 ${s.badges.length}/${ALL_BADGES.length} · 📅 ${s.days.length}</p>
      </div>

      <div class="card">
        <h2>${t('covered')}</h2>
        <ul class="covered">${t('coveredList').map((x) => `<li>${x}</li>`).join('')}</ul>
      </div>

      <div class="card">
        <h2>🔒 ${t('privacyTitle')}</h2>
        <p>${t('privacyBody')}</p>
        <p>🎙️ ${t('privacyVoice')}</p>
      </div>

      <div class="card actions-card">
        <button class="btn btn-primary" type="button" data-install hidden>📲 ${t('install')}</button>
        ${ios ? `<p class="muted">📲 ${t('installIos')}</p>` : ''}
        <button class="btn btn-danger" type="button" data-reset>🗑️ ${t('reset')}</button>
      </div>
      <p class="fine center">${t('appName')} · ${t('version')} 0.12</p>
    </section>`;

  app.querySelectorAll('[data-set]').forEach((el) => {
    el.onchange = () => store.set({ [el.dataset.set]: el.checked });
  });
  const test = app.querySelector('[data-test]');
  if (test) test.onclick = () => speak('नमस्ते! मैं टिमटिम हूँ।', { force: true });
  app.querySelector('[data-name]').onsubmit = (e) => {
    e.preventDefault();
    const name = app.querySelector('#pn').value.trim().slice(0, 20);
    if (!name) return;
    store.set({ name });
    toast(t('saved'));
  };
  const install = app.querySelector('[data-install]');
  if (installEvent) {
    install.hidden = false;
    install.onclick = async () => {
      installEvent.prompt();
      await installEvent.userChoice;
      installEvent = null;
      install.hidden = true;
    };
  }
  // Two taps to reset (browser confirm() dialogs are blocked inside the Claude app).
  const reset = app.querySelector('[data-reset]');
  let armed = false;
  reset.onclick = () => {
    if (!armed) {
      armed = true;
      reset.textContent = `⚠️ ${t('resetConfirm')}`;
      reset.classList.add('armed');
      setTimeout(() => {
        armed = false;
        reset.textContent = `🗑️ ${t('reset')}`;
        reset.classList.remove('armed');
      }, 5000);
      return;
    }
    store.reset();
    toast(t('resetDone'));
    go('welcome', true);
  };
}

function toast(text) {
  const el = document.createElement('div');
  el.className = 'toast-msg';
  el.textContent = text;
  document.getElementById('toast').appendChild(el);
  setTimeout(() => el.remove(), 1200);
}

// ---------- router ----------

function render() {
  if (cleanup) cleanup();
  cleanup = null;
  stopSpeech();
  document.documentElement.lang = lang();
  document.title = t('appName');

  const [route = '', arg = ''] = location.hash.replace(/^#\/?/, '').split(/[./]/);
  const named = !!store.get().name;
  // Players from before the book picker existed were on Book 3.
  if (named && !store.get().book && Object.keys(store.get().levels).length) store.set({ book: 'b3' });
  if (named && store.get().introSeen && !store.get().book && !['books', 'welcome', 'story', 'parents'].includes(route)) return go('books', true);
  if (!named && !['welcome', 'parents'].includes(route)) return go('welcome', true);

  switch (route) {
    case 'welcome': welcome(); break;
    case 'story': story(); break;
    case 'galaxy': galaxy(); break;
    case 'books': books(); break;
    case 'planet': planet(arg); break;
    case 'level': levelIntro(arg); break;
    case 'play': play(arg); break;
    case 'result': result(arg); break;
    case 'badges': badges(); break;
    case 'parents': parents(); break;
    default: return go('galaxy', true);
  }
  bindCommon();
  bindTalkForm();
  window.scrollTo(0, 0);
  const heading = app.querySelector('h1');
  if (heading) heading.setAttribute('tabindex', '-1');
}

window.addEventListener('hashchange', render);
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  installEvent = e;
});
render();

if ('serviceWorker' in navigator && !embedded) {
  window.addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));
}
