#!/usr/bin/env python3
"""Four ways to show the profile links on the Publications page. Builds options/a.html to d.html for comparison."""
import re
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import build as b

HERE = Path(__file__).parent
spec = spec_from_file_location("wallsite", HERE / "site.py")  # not the standard library's site
site = module_from_spec(spec)
spec.loader.exec_module(site)
OUT = HERE / "options"

PROFILES = [
    ("Google Scholar", "https://scholar.google.com/citations?user=b-HX-AYAAAAJ&amp;hl=en", "Citations and co-authors"),
    ("Semantic Scholar", "https://www.semanticscholar.org/author/Jermain-Kaminski/39736726", "Papers and influence"),
    ("Sage Policy Impact", "https://policyprofiles.sagepub.com/profile/6676/jermain-kaminski", "Citations in policy documents"),
    ("Rankless", "https://www.rankless.org/authors/jermain-kaminski", "Author rankings"),
]
ARROW = '<svg viewBox="0 0 12 12" width="11" height="11" aria-hidden="true"><path d="M2.5 9.5 9.5 2.5M4 2.5h5.5V8" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'

OPTIONS = {
    # A: one quiet line of text links under the title, no boxes
    "a": ('<p class="prof-line"><span class="lbl">Profiles</span>' + "".join(
        f'<a href="{u}">{n}{ARROW}</a>' for n, u, _ in PROFILES) + "</p>", """
.prof-line{display:flex;flex-wrap:wrap;align-items:center;gap:10px 0;margin:28px 0 0;font-size:16px}
.prof-line .lbl{margin-right:24px}
.prof-line a{display:inline-flex;align-items:center;gap:6px;text-decoration:none;padding:4px 0;color:var(--ink)}
.prof-line a+a{margin-left:24px;padding-left:24px;border-left:1px solid var(--rule)}
.prof-line a svg{color:var(--ink-3);transition:transform 160ms cubic-bezier(.2,.7,.2,1),color 160ms}
.prof-line a:hover{color:var(--accent-text)}
.prof-line a:hover svg{color:var(--accent);transform:translate(1px,-1px)}
"""),
    # B: the links sit beside the title, on its baseline, like the facts under the hero
    "b": ("", """
.head{display:grid;grid-template-columns:7fr 5fr;column-gap:64px;align-items:end}
.head h1{grid-column:1}
.prof-col{grid-column:2;margin:0;padding:0 0 .12em;list-style:none;border-top:1px solid var(--rule)}
.prof-col li{border-bottom:1px solid var(--rule)}
.prof-col a{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding:11px 0;text-decoration:none;font-size:16px;position:relative}
.prof-col a span:last-child{color:var(--ink-3);font-size:14.5px;text-align:right}
.prof-col a::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:1px;background:var(--accent);transform:scaleX(0);transform-origin:left;transition:transform 260ms cubic-bezier(.2,.7,.2,1)}
.prof-col a:hover::after{transform:scaleX(1)}
.prof-col a:hover span:first-child{color:var(--accent-text)}
@media (max-width:1000px){.head{grid-template-columns:minmax(0,1fr)}.prof-col{grid-column:1;margin-top:28px;max-width:440px}}
"""),
    # C: a sentence in the page's lead type, with the profiles as links in the prose
    "c": ('<p class="prof-lead">My papers are indexed on <a href="{0}">Google Scholar</a> and <a href="{1}">Semantic Scholar</a>, '
          'their use in policy is tracked by <a href="{2}">Sage</a>, and <a href="{3}">Rankless</a> ranks the lot.</p>'.format(*(u for _, u, _ in PROFILES)), """
.prof-lead{margin:28px 0 0;max-width:30ch;font:var(--display-weight) clamp(22px,2.2vw,30px)/1.3 var(--serif);letter-spacing:-.01em;color:var(--ink-2);text-wrap:pretty}
.prof-lead a{color:var(--ink);text-decoration:underline;text-decoration-thickness:1px;text-decoration-color:var(--accent);text-underline-offset:5px}
.prof-lead a:hover{color:var(--accent-text)}
"""),
    # D: a first section of the page itself, in the two-column structure the other sections use
    "d": ("", """
.prof-rows{list-style:none;margin:0;padding:0}
.prof-rows a{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 24px;padding:16px 0;border-top:1px solid var(--rule);text-decoration:none;position:relative}
.prof-rows li:last-child a{border-bottom:1px solid var(--rule)}
.prof-rows .n{font:var(--display-weight) clamp(22px,2vw,26px)/1.2 var(--serif);letter-spacing:-.01em}
.prof-rows .s{grid-column:1;color:var(--ink-3);font-size:var(--small)}
.prof-rows .go{grid-column:2;grid-row:1/3;align-self:center;color:var(--ink-3)}
.prof-rows .go svg{width:16px;height:16px}
.prof-rows a::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:1px;background:var(--accent);transform:scaleX(0);transform-origin:left;transition:transform 260ms cubic-bezier(.2,.7,.2,1)}
.prof-rows a:hover::after{transform:scaleX(1)}
.prof-rows a:hover .n{color:var(--accent-text)}
.prof-rows a:hover .go{color:var(--accent)}
"""),
}


def page(key):
    html = b.subpage("publications")
    chips = re.search(r'<div class="chips">.*?</div>', html, flags=re.S).group(0)
    head, css = OPTIONS[key]
    if key == "b":
        head = '<ul class="prof-col">' + "".join(
            f'<li><a href="{u}"><span>{n}</span><span>{s}</span></a></li>' for n, u, s in PROFILES) + "</ul>"
    html = html.replace(chips, head, 1)
    if key == "d":
        rows = '<section class="part"><h2>Profiles</h2><ul class="prof-rows">' + "".join(
            f'<li><a href="{u}"><span class="n">{n}</span><span class="s">{s}</span><span class="go">{ARROW}</span></a></li>'
            for n, u, s in PROFILES) + "</ul></section>"
        html = html.replace('<div class="pad page">', '<div class="pad page">' + rows, 1)
    html = html.replace("</head>", f"<style>{css}</style></head>", 1)
    return site.localize(html).replace('src="../media/', 'src="media/')


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "wall.css").write_text((HERE / "wall.css").read_text(encoding="utf8"), encoding="utf8")
    for key in OPTIONS:
        (OUT / f"{key}.html").write_text(page(key), encoding="utf8")
