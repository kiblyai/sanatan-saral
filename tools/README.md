# How the pages are built (read this before editing)

Since November 2026 every page holds **one language**.

- `/page.html` is English. `/hi/page.html`, `/gu/…`, `/te/…`, `/mr/…`, `/ta/…`, `/bn/…`, `/kn/…`, `/ml/…` are the same page in that language.
- Each page names itself as its canonical address and lists the other languages with `hreflang` links.
- The language buttons are links between these addresses. A small script at the top of each page (marked `/*lang-page*/`)
  sends a returning reader to the language they chose last (`localStorage` key `sd-lang`), honours `?lang=xx`, and on a first
  visit follows the browser language when that translation exists.
- There is no generator. The pages in this repository are the source. Edit the page for the language you are changing.

## Before November 2026

Every page carried all nine languages side by side (elements with class `en hi gu te mr ta bn kn ml`, and `xg xt xm xa xb xk xl`
on English text that a translation replaces), and CSS hid all but one. Pages were 3 to 4 times larger, and Google saw nine
languages on one address. The last commit in that form is `719281e`.

## Tools (run from the site root)

- `python3 tools/split_languages.py` cuts every page down to its own language, sets `<html lang>`, the canonical link and the
  head script. It is safe to run again and changes nothing on pages that are already split (`--check` only reports).
  If you paste in a page written in the old all-languages form, copy it to each language folder and run this tool.

## Things that still expect several languages

- `verse-tools.js`, `share.js`, `interactive.js` and `cards-xx.js` build some text in several languages at once and rely on CSS
  to show one. The rules that hide the others now live at the end of `style.css` (and inline on the home pages).
- A page in Gujarati, Telugu, Marathi, Tamil, Bengali, Kannada or Malayalam keeps its own `<style id="xx-css">` block in its
  head, after the page's own styles. Leave it there: its font rules have to come last to win.
- The split tool cannot be run on an already-split page to bring that block back. To redo the split from scratch, take the
  pages from commit `719281e` and run the tool on those.
- The home pages keep their verse-of-the-day list inline; each language's home page holds only English plus its own language.
- `style.css` and `lang.js` are linked as `?v=2`. Raise the number (in the pages, in `sw.js` and in `ASSET_V` in
  `split_languages.py`) whenever either file changes in a way old cached copies would break.

## Kids' story pictures

- `python3 tools/kids_art.py` draws the pictures for the fourteen stories on the kids page (three per story, one for each
  page of the story) and writes them into the site: `kids-art.js` holds all of them, and each `kids.html` gets the cover
  picture for every story card. Safe to run again.
- `python3 tools/kids_art.py --sheet preview.html` writes a page showing every picture, for checking before publishing.
- The characters and scenery are in `tools/kids_art_kit.py`. To change a picture, edit its scene in `tools/kids_art.py`.
- Sad moments are drawn gently on purpose (no arrows in flight, no injuries).

## Gita chapters 7 to 18

Chapters 1 to 6 were written straight into their pages. From chapter 7 on, each chapter is built from a data file.

- `tools/gita/content/cNN.py` holds what was written for the site: the chapter's name and outline, and for each verse the
  speaker, the word-by-word list and the translation. Edit a meaning or a translation here.
- `tools/gita/chNN.json` is that content joined with the Sanskrit. The Sanskrit is never typed by hand. It comes from an
  open public-domain copy and is used only where three copies agree (see `tools/gita/sources.py` for which copies, and
  `tools/gita/make_data.py` for the two typing faults it repairs). `--check-words` is a spelling check on the word lists.
- `python3 tools/gita/build.py N`, then `python3 tools/split_languages.py`, writes `gita-N.html` and one page per verse,
  links them from the chapter before, the Gita hub, the search index and the sitemap. Safe to run again.
- The site follows the 700-verse numbering, in which chapter 13 has 34 verses. The three copies count 35 there, so
  site verse 13.n is their 13.(n+1).
- New chapters are in English only. Their pages list no other languages, and the language buttons leave the reader on
  the English page.
- To rebuild the data you need the three copies in one folder: `verse.json` from github.com/gita/gita (data/),
  `B/<chapter>-<verse>.json` from github.com/vedicscriptures/bhagavad-gita (slok/), and `C/<chapter>.json` from
  github.com/bhavykhatri/DharmicData (SrimadBhagvadGita/).
