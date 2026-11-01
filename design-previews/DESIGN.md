# Personal site redesign: The Wall, Orange (Straight)

The chosen design, final. It is a Publii theme, `publii/wall/`.

## Files
- `publii/wall/` is the theme. `assets/css/main.css` is the only stylesheet, one ordered file: tokens, base, header and menu, home sections, pages and parts, publications, posts and essays, footer, Publii page bodies, one block per breakpoint, motion, print.
- `assets/js/wall.js` shapes Publii's page bodies (sections, citations with BibTeX, grants, courses), assembles the mail links, closes the menu sheet, fills in "last updated", drives the running head and the share button, and curls quotes. The theme has no author template because `createAuthorPages` is off in `config.json`.
- `wall/media/` holds source images, including `originals/` and the logo files `logo.svg` and `logo-light.svg`. Nothing in it is ever downscaled or deleted. `media/` holds four leftover images; it is ignored by git and unused.

## Tokens
- Colour: white page, neutral ink #161616 (#3a3a3a, #5e5e5e), rule #e2e2e2, accent #d0450c (4.63:1 on white, white text on it), accent text #b83d0a. No rounded corners. Light footer.
- Type: Newsreader (light, optical sizes) for display, Geist for text; both are served from `assets/fonts/`, as the privacy page says. Reading text 18/1.6.
- Ladder at 1440: hero line 56, page titles 66, sign-off 177, section heads 33, article titles 64, card titles 39, work and pillar titles 30 to 32, Writing page lead 56 and others 34, numerals on the home page 52.

## Logo
The compass (`partials/logo.hbs`; files in `wall/media/`): an eight-point faceted star, long cardinal points and short diagonals, a lit and a shaded half on each point; the cardinals in the deep orange pair (#f4702f / #b53c08), the diagonals in the light pair (#ffa24a / #d0450c). It sits left of the name in the header and, in very light grey, in the footer. It turns 30 degrees on hover over the logo or name. It is coloured by the classes `.f1` to `.f4` in `main.css`.

## Pages
- Home: the role line, hero with portrait (text and photograph start and end on the same lines; the Poets & Quants badge hangs below the menu on desktop and sits in the photograph's upper-right corner below 1001px, where the crop keeps you left of centre), Latest writing (equal cards), Three pillars of current research, Selected publications (a ledger, edited in `index.hbs`), Teaching (ratings), then In the news and Recent and upcoming side by side as two ledgers (headline left, place or source and year right, hairlines between rows), sign-off. Selected work, the Charles River photograph, the research summary and Work with me were taken off the home page.
- Sub-pages: a title and one sentence (`partials/page-lead.hbs`), then a low photograph (at most 345px high). About (full-length photograph beside the text), Research, Publications (profile sentence, citations with BibTeX on request), Teaching, Students, Speaking, News. Sections are two columns: the heading on the left, sticky.
- Writing: a magazine grid, the newest piece across two columns; a byline card (A) closes the page. Articles close with keywords (Publii tags, shown as plain links; News, Editor's Picks and Essay stay hidden there) and a share button, then previous and next, then the author in a sentence (G). Article text is centered under the photograph. Essays get an orange drop cap and a pull quote, in the margin from 1400px wide and inline below that.

## Signature
- The arrow: on hover or keyboard focus, rows in the news and events ledgers colour their title and an arrow follows the date.
- The hero assembles on load; a running head with a reading-progress rule appears on articles once the title has scrolled away; pages hand over with cross-document view transitions (post images move between home and article; the logo holds still). All of it respects reduced motion. Post images use the transition name `post-<id>` and the default timing.
- Up to 1000px wide (phones and iPad portrait) the menu is a full-screen sheet; on phones (a checkbox holds the open state, no script needed), photographs run edge to edge. Photographs carry a short note beneath at every width.
- The footer sign-off "Let's work together.", two mail routes (assembled by script, so the addresses are not in the source), LinkedIn and Bluesky in the colophon. The badge appears on the home page only; the only file that exists is 271×459 (2.7× its displayed width).

## Publii workflow
1. Edit the theme in `publii/wall/`.
2. Copy `publii/wall/` to the two places Publii reads themes from:
   - `~/Documents/Publii/sites/jermain-c-kaminski/input/themes/wall`
   - `~/Documents/Publii/themes/wall`
3. In the Publii app, open the site and press Preview. Edit content (home text, mail addresses, hero, author lines) under Theme settings; the pillars live in `partials/pillars.hbs`.
4. Publii generates responsive images, so originals stay untouched and no smaller copies are made.

## Publii's CSS compression
`Publii > Site settings > Advanced > CSS compression` runs the stylesheet through clean-css. It cannot read nested at-rules (a media query inside a media query, `@starting-style`), and then unwraps every rule after them, so phone and print rules apply everywhere. It also drops `@view-transition` and `color-mix()`. Keep `main.css` flat: no nested at-rules, no `color-mix()`; the view-transition switch lives in `partials/head.hbs`. To check a change, run the file through `clean-css` and confirm every `@media`, `@supports` and `@keyframes` is still there.

## Images and citations
Publii's image settings are WebP at quality 90, not lossless. After changing them, use Publii's regenerate thumbnails tool. BibTeX records live in `assets/js/citations.js`, one per row of the Publications page; a row without a record shows no BibTeX link.
