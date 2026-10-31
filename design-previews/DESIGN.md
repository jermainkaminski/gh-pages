# Personal site redesign: The Wall, Orange (Straight)

The chosen design. HTML preview only, not yet in Publii. Build with `python3 -B site.py` from `wall/`; output goes to `wall/site/`. Styles are in `wall/wall.css`, content in `wall/content.py` and `wall/home_sections.html`; sub-page text is read from the live site's pages by `wall/build.py`.

`wall/media/` is mostly copies of images the site already has; only `Jermain-standing.jpg` and `originals/` are tracked. To restore the rest after a fresh clone, copy from the repository root: `assets/40under40logo.jpg`, `media/posts/12/Jermain-Kaminski-1-md-Kopie-3.jpg` (also saved as `Jermain-Kaminski-1-md.jpg`), `media/posts/18/MBA-LR-5.jpg`, `media/posts/11/MITSailing-1.jpg`, `media/posts/16/UM-Tapijn-202011-022.jpg`, `media/posts/9/cdsm-2026-header.jpg`, `media/posts/19/pierre-goiffon-aR_COwiGzP0-unsplash.jpg`, `media/posts/19/Will20Hunting.jpg.webp`, `media/posts/19/image.png`.

## Tokens
- Colour: white page, ink #141c30 (#2f3850, #535c75), rule #dde2ec, accent #d0450c (4.63:1 on white, white text on it), accent text #b83d0a. No rounded corners. Light footer.
- Type: Newsreader (light, optical sizes) for display, Geist for text. Reading text 18/1.6.
- Ladder at 1440: hero 63, sign-off 177, section heads 33, post titles 39 and 49, work and pillar titles 30 and 32.

## Signature
- The arrow: rows in selected work and events draw a directed edge on hover or keyboard focus (260ms).
- Footer sign-off "Let's work together.", two mail routes, LinkedIn and Bluesky in the colophon. The Poets & Quants badge appears on the home page only; the only file that exists is 271×459 (2.7× its displayed width).
- Type versions live in `wall/fonts.py` and build into `wall/site-<name>/`: newsreader (chosen: Newsreader + Geist), instrument (Instrument Serif + Geist), fraunces (Fraunces + Hanken Grotesk), host (Host Grotesk + Geist Mono). `wall/site/` is always the Newsreader build without the preview switcher.
- Cross-document view transitions: post images move between home and article; the logo holds still. Respects reduced motion.

## For the Publii port
- Publii generates responsive images, so originals stay untouched and no smaller copies are made here.
- Self-host the two fonts rather than loading them from Google.
- Add a 404 page in the theme.
