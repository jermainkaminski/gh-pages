#!/usr/bin/env python3
"""Four layouts for the Writing page, built into writing-options/ for comparison."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import build as b

HERE = Path(__file__).parent
OUT = HERE / "writing-options"
spec = spec_from_file_location("wallsite", HERE / "site.py")  # not the standard library's site
site = module_from_spec(spec)
spec.loader.exec_module(site)

KICKER = {"cdsm-2026.html": "Announcement", "essay.html": "Essay"}
READ = {"cdsm-2026.html": "3 min", "essay.html": "9 min"}


def img(p):
    return site.img(p)


def posts():
    return site.POSTS


def head_html(title="Writing", deck=None):
    deck = f'<p class="deck">{deck}</p>' if deck else ""
    return f'<div class="pad head"><h1>{title}</h1>{deck}</div>'


# A: the Gazette front. One lead story, then the rest as a ruled list with small pictures.
def a():
    lead, *rest = posts()
    lead_html = (f'<a class="lead-story" href="{lead["file"]}"><span class="pic">{img(lead)}</span>'
                 f'<span class="kick">{KICKER[lead["file"]]} · {lead["date"]}</span><span class="t">{lead["title"]}</span>'
                 f'<span class="s">{lead["blurb"]}</span><span class="rt">{READ[lead["file"]]} read</span></a>')
    rows = "".join(f'<a class="more-row" href="{p["file"]}"><span class="pic">{img(p)}</span><span class="tx"><span class="kick">{KICKER[p["file"]]} · {p["date"]}</span>'
                   f'<span class="t">{p["title"]}</span><span class="s">{p["blurb"]}</span></span></a>' for p in rest)
    main = head_html() + f'<div class="pad page gaz">{lead_html}<h2 class="sec-h rule">More writing</h2><div class="more-rows">{rows}</div></div>'
    return main, """
.gaz{padding-top:0}
.lead-story{display:block;text-decoration:none;color:inherit;padding-bottom:48px;border-bottom:1px solid var(--rule)}
.lead-story .pic{display:block;aspect-ratio:21/9;overflow:hidden;margin-bottom:28px}
.lead-story .pic img{width:100%;height:100%;object-fit:cover;display:block}
.kick{display:block;font:500 12.5px/1.3 var(--sans);letter-spacing:.09em;text-transform:uppercase;color:var(--accent-text);margin-bottom:14px}
.lead-story .t{display:block;font:var(--display-weight) clamp(40px,5.6vw,84px)/1 var(--serif);letter-spacing:-.03em;max-width:18ch;text-wrap:balance}
.lead-story .s{display:block;margin-top:20px;font:var(--display-weight) clamp(22px,2.1vw,30px)/1.3 var(--serif);letter-spacing:-.01em;color:var(--ink-2);max-width:48ch;text-wrap:pretty}
.rt{display:block;margin-top:18px;font-size:14px;color:var(--ink-3)}
.lead-story:hover .t{color:var(--accent-text)}
.sec-h.rule{margin:48px 0 0;padding-bottom:16px;border-bottom:1px solid var(--ink);font-size:clamp(22px,1.9vw,26px)}
.more-rows{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 48px}
.more-row{display:grid;grid-template-columns:160px minmax(0,1fr);gap:24px;padding:28px 0;border-bottom:1px solid var(--rule);text-decoration:none;color:inherit;align-items:start}
.more-row .pic{aspect-ratio:1;overflow:hidden}
.more-row .pic img{width:100%;height:100%;object-fit:cover;display:block}
.more-row .t{display:block;font:var(--display-weight) clamp(24px,2.2vw,32px)/1.1 var(--serif);letter-spacing:-.015em}
.more-row .s{display:block;margin-top:8px;font-size:var(--small);line-height:1.45;color:var(--ink-2)}
.more-row:hover .t{color:var(--accent-text)}
@media (max-width:800px){.more-rows{grid-template-columns:minmax(0,1fr)}.more-row{grid-template-columns:96px minmax(0,1fr)}.lead-story .pic{aspect-ratio:3/2;margin-inline:-24px}}
"""


# B: the archive. A ruled index with the year in the margin, no pictures; the writing speaks.
def b_():
    rows = "".join(f'<a class="ix" href="{p["file"]}"><span class="yr">{p["date"][-4:]}</span><span class="tx"><span class="kick">{KICKER[p["file"]]}</span>'
                   f'<span class="t">{p["title"]}</span><span class="s">{p["blurb"]}</span><span class="meta">{p["date"]} · {READ[p["file"]]} read</span></span></a>' for p in posts())
    main = head_html("Writing", "Essays and announcements, newest first.") + f'<div class="pad page"><div class="index">{rows}</div></div>'
    return main, """
.deck{margin:16px 0 0;font:var(--display-weight) clamp(20px,1.8vw,24px)/1.35 var(--serif);color:var(--ink-3)}
.index{border-top:1px solid var(--ink)}
.ix{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);column-gap:64px;padding:40px 0;border-bottom:1px solid var(--rule);text-decoration:none;color:inherit}
.ix .yr{font:var(--display-weight) clamp(28px,2.6vw,36px)/1 var(--serif);color:var(--ink-3);font-variant-numeric:lining-nums}
.kick{display:block;font:500 12.5px/1.3 var(--sans);letter-spacing:.09em;text-transform:uppercase;color:var(--accent-text);margin-bottom:12px}
.ix .t{display:block;font:var(--display-weight) clamp(32px,3.6vw,52px)/1.05 var(--serif);letter-spacing:-.025em;text-wrap:balance;max-width:22ch}
.ix .s{display:block;margin-top:14px;font-size:var(--text);line-height:1.55;color:var(--ink-2);max-width:56ch}
.ix .meta{display:block;margin-top:14px;font-size:14px;color:var(--ink-3)}
.ix:hover .t{color:var(--accent-text)}
@media (max-width:800px){.ix{grid-template-columns:minmax(0,1fr);row-gap:8px;padding:28px 0}.ix .yr{font-size:16px}}
"""


# C: the broadsheet. Two columns divided by a hairline, each piece with kicker, picture, headline and the opening lines.
def c():
    cols = "".join(f'<a class="col" href="{p["file"]}"><span class="kick">{KICKER[p["file"]]}</span><span class="pic">{img(p)}</span>'
                   f'<span class="t">{p["title"]}</span><span class="s">{p["blurb"]}</span><span class="meta">{p["date"]} · {READ[p["file"]]} read</span></a>' for p in posts())
    main = head_html() + f'<div class="pad page"><div class="sheet">{cols}</div></div>'
    return main, """
.sheet{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:0;border-top:1px solid var(--ink);padding-top:32px}
.col{display:block;text-decoration:none;color:inherit;padding:0 40px 32px}
.col:first-child{padding-left:0;border-right:1px solid var(--rule)}
.col:last-child{padding-right:0}
.kick{display:block;font:500 12.5px/1.3 var(--sans);letter-spacing:.09em;text-transform:uppercase;color:var(--accent-text);margin-bottom:14px}
.col .pic{display:block;aspect-ratio:3/2;overflow:hidden;margin-bottom:20px}
.col .pic img{width:100%;height:100%;object-fit:cover;display:block}
.col .t{display:block;font:var(--display-weight) clamp(30px,3vw,44px)/1.06 var(--serif);letter-spacing:-.022em;text-wrap:balance}
.col .s{display:block;margin-top:14px;font-size:var(--text);line-height:1.55;color:var(--ink-2)}
.col .s::first-letter{font:400 2.4em/.8 var(--serif);float:left;margin:6px 8px 0 0;color:var(--accent)}
.col .meta{display:block;margin-top:16px;font-size:14px;color:var(--ink-3)}
.col:hover .t{color:var(--accent-text)}
@media (max-width:800px){.sheet{grid-template-columns:minmax(0,1fr)}.col{padding:0 0 32px}.col:first-child{border-right:0;border-bottom:1px solid var(--rule);margin-bottom:32px}}
"""


# D: the magazine grid. Kicker, picture, headline, dek; the newest piece spans two columns.
def d():
    cards = "".join(f'<a class="mag" href="{p["file"]}"><span class="pic">{img(p)}</span><span class="kick">{KICKER[p["file"]]} · {READ[p["file"]]} read</span>'
                    f'<span class="t">{p["title"]}</span><span class="s">{p["blurb"]}</span><span class="meta">{p["date"]}</span></a>' for p in posts())
    main = head_html() + f'<div class="pad page"><div class="maggrid">{cards}</div></div>'
    return main, """
.maggrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:48px clamp(24px,3vw,48px);border-top:1px solid var(--ink);padding-top:32px}
.mag{display:block;text-decoration:none;color:inherit}
.mag:first-child{grid-column:span 2}
.mag .pic{display:block;aspect-ratio:3/2;overflow:hidden;margin-bottom:18px}
.mag:first-child .pic{aspect-ratio:2/1}
.mag .pic img{width:100%;height:100%;object-fit:cover;display:block}
.kick{display:block;font:500 12.5px/1.3 var(--sans);letter-spacing:.09em;text-transform:uppercase;color:var(--accent-text);margin-bottom:10px}
.mag .t{display:block;font:var(--display-weight) clamp(26px,2.4vw,34px)/1.1 var(--serif);letter-spacing:-.018em;text-wrap:balance}
.mag:first-child .t{font-size:clamp(34px,4vw,56px);letter-spacing:-.025em;max-width:20ch}
.mag .s{display:block;margin-top:10px;font-size:var(--small);line-height:1.5;color:var(--ink-2);max-width:52ch}
.mag:first-child .s{font-size:var(--text)}
.mag .meta{display:block;margin-top:12px;font-size:14px;color:var(--ink-3)}
.mag:hover .t{color:var(--accent-text)}
@media (max-width:1000px){.maggrid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.maggrid{grid-template-columns:minmax(0,1fr)}.mag:first-child{grid-column:auto}.mag .pic{margin-inline:-24px}}
"""


OPTIONS = {"a": a, "b": b_, "c": c, "d": d}

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "wall.css").write_text((HERE / "wall.css").read_text(encoding="utf8"), encoding="utf8")
    for key, fn in OPTIONS.items():
        main, css = fn()
        html = b.page("Writing: Jermain C. Kaminski", main, "writing")
        html = html.replace("</head>", f"<style>{css}</style></head>", 1)
        (OUT / f"{key}.html").write_text(site.localize(html).replace('src="../media/', 'src="../media/'), encoding="utf8")
