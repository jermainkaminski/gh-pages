# Personal site redesign: The Wall, Orange (Straight)

The chosen design, final. It exists twice: as an HTML preview built from the live pages (`wall/`), and as a Publii theme (`publii/wall/`). Both read the same stylesheet, `wall/wall.css`.

## Files
- `wall/site.py` builds the preview: `cd wall && python3 -B site.py` writes `wall/site/`. `wall/build.py` holds the page helpers (nav, footer, sub-pages, citations); `wall/content.py` the pillars, news and work-with-me text; `wall/home_sections.html` the rest of the home page (selected work, river photo, about, teaching, events). Sub-page text is read from the live pages in the repository root, so the wording stays Jermain's own.
- **Since 31 Oct the live pages in the repository root are rendered by Publii with this theme.** `build.py` parses the older Publii markup (`content__inner content__entry`), so `site.py` no longer builds from them; `wall/site/` stays as the last snapshot of the preview. Work on the design in `wall/wall.css` and the theme, and check it in Publii's Preview.
- Until then `build.py` patched a few things on the way in (`TYPOS`, `ALTS`, `SILICON`, `GITHUB_POST`) because the live pages in `research/`, `students/`, `teaching/`, `publications/`, `the-sistine-chapel-problem/` and `causal-data-science-meeting-2026/` have not been regenerated with those fixes. Drop an entry once its page is fixed in Publii.
- `wall/wall.css` is the only stylesheet. One ordered file: tokens, base, header and menu, home sections, pages and parts, publications, posts and essays, footer, Publii page bodies, one block per breakpoint (from 900, 1001 and 1181 up; to 1180, 1000, 800, 640 and 420 down), motion, print. `publii/wall/assets/css/main.css` is an exact copy.
- `publii/wall/` is the theme. `wall.js` (in `assets/js/`) shapes Publii's page bodies (sections, citations with BibTeX, grants, courses), assembles the mail links, closes the phone menu, fills in "last updated", drives the running head and curls quotes. The theme has no tag or author templates because `createTagPages` and `createAuthorPages` are off in `config.json`.
- `publii/prepare_content.py` and `publii/add_post.py` were one-off scripts against the Publii database. They have been run; do not run them again.

`wall/media/` is mostly copies of images the site already has; only `Jermain-standing.jpg`, `Jermain-Kos.jpg` and `originals/` are tracked, and nothing in it is ever downscaled or deleted. To restore the rest after a fresh clone, copy from the repository root: `assets/40under40logo.jpg`, `media/posts/12/Jermain-Kaminski-1-md-Kopie-3.jpg` (also saved as `Jermain-Kaminski-1-md.jpg`), `media/posts/18/MBA-LR-5.jpg`, `media/posts/11/MITSailing-1.jpg`, `media/posts/16/UM-Tapijn-202011-022.jpg`, `media/posts/9/cdsm-2026-header.jpg`, `media/posts/19/pierre-goiffon-aR_COwiGzP0-unsplash.jpg`, `media/posts/19/Will20Hunting.jpg.webp`, `media/posts/19/image.png`. `design-previews/media/` holds four leftover images from discarded attempts; it is ignored by git and unused.

## Tokens
- Colour: white page, ink #141c30 (#2f3850, #535c75), rule #dde2ec, accent #d0450c (4.63:1 on white, white text on it), accent text #b83d0a. No rounded corners. Light footer.
- Type: Newsreader (light, optical sizes) for display, Geist for text; both come from Google Fonts in `head.hbs` and in the preview. Reading text 18/1.6.
- Ladder at 1440: hero line 56, page titles 104, sign-off 177, section heads 33, card titles 39, work and pillar titles 30 to 32, Writing page lead 56 and others 34, numerals on the home page 52.

## Logo
The compass (`publii/wall/assets/img/logo.svg`, light-grey twin `logo-light.svg`): an eight-point faceted star, long cardinal points and short diagonals, a lit and a shaded half on each point; the cardinals in the deep orange pair (#f4702f / #b53c08), the diagonals in the light pair (#ffa24a / #d0450c). It sits left of the name in the header and, in very light grey, in the footer. It is inlined in `nav.hbs` and `footer.hbs`, coloured by the classes `.f1` to `.f4` in `wall.css`.

## Pages
- Home: hero with portrait (text and photograph start and end on the same lines; the Poets & Quants badge hangs below the menu on desktop and sits in the photograph's upper-right corner below 1001px, where the crop keeps you left of centre), Latest writing (equal cards), Three pillars of current research, Teaching (ratings), then In the news and Recent and upcoming side by side as two ledgers (headline left, place or source and year right, hairlines between rows), sign-off. Selected work, the Charles River photograph, the research summary and Work with me were taken off the home page.
- Sub-pages: About (full-length photograph beside the text), Research, Publications (profiles line, citations with BibTeX on request), Teaching, Students, Speaking, News. Sections are two columns: the heading on the left, sticky.
- Writing: a magazine grid, the newest piece across two columns; a byline card (A) closes the page. Articles close with previous and next, then the author in a sentence (G). Essays get an orange drop cap and a pull quote in the margin.

## Signature
- The arrow: rows in selected work and events draw an orange edge on hover or keyboard focus (260ms) and an arrow follows the last word.
- The hero assembles on load; a running head with a reading-progress rule appears on articles once the title has scrolled away; pages hand over with cross-document view transitions (post images move between home and article; the logo holds still). All of it respects reduced motion. In the preview the two posts have their own transition names; in Publii they are `post-<id>` and use the default timing.
- On phones the menu is a full-screen sheet (a checkbox holds the open state, no script needed) and photographs run edge to edge with a short note beneath.
- The footer sign-off "Let's work together.", two mail routes (assembled by script, so the addresses are not in the source), LinkedIn and Bluesky in the colophon. The badge appears on the home page only; the only file that exists is 271×459 (2.7× its displayed width).

## Publii workflow
1. Edit the theme in `publii/wall/` (templates, `assets/js/wall.js`). For styles, edit `wall/wall.css`, run `python3 -B site.py` from `wall/` to check the preview, then `cp wall/wall.css publii/wall/assets/css/main.css`.
2. Copy `publii/wall/` to the two places Publii reads themes from:
   - `~/Documents/Publii/sites/jermain-c-kaminski/input/themes/wall`
   - `~/Documents/Publii/themes/wall`
3. In the Publii app, open the site and press Preview. Edit content (home text, mail addresses, hero, author lines) under Theme settings; the pillars live in `partials/pillars.hbs`.
4. Publii generates responsive images, so originals stay untouched and no smaller copies are made.

## Still open
- Self-host the two fonts rather than loading them from Google.

## Publii's CSS compression
`Publii > Site settings > Advanced > CSS compression` runs the stylesheet through clean-css. It cannot read nested at-rules (a media query inside a media query, `@starting-style`), and then unwraps every rule after them, so phone and print rules apply everywhere. It also drops `@view-transition` and `color-mix()`. Keep `wall.css` flat: no nested at-rules, no `color-mix()`; the view-transition switch lives in `partials/head.hbs`. To check a change, run the file through `clean-css` and confirm every `@media`, `@supports` and `@keyframes` is still there.
