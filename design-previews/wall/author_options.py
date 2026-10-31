#!/usr/bin/env python3
"""Eight ways to close an article: previous/next links, then the author. Built into author-options/ as short stub articles."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import build as b

HERE = Path(__file__).parent
OUT = HERE / "author-options"
spec = spec_from_file_location("wallsite", HERE / "site.py")
site = module_from_spec(spec)
spec.loader.exec_module(site)

PORTRAIT = '<img src="media/Jermain-Kaminski-1-md-Kopie-3.jpg" alt="Jermain Kaminski" loading="lazy">'
BIO = "Associate Professor of Entrepreneurship and Innovation at Maastricht University. I work on causal inference and machine learning for the decisions entrepreneurs make, and on the economic complexity of software."
SHORT = "Associate Professor of Entrepreneurship and Innovation, Maastricht University."
MAIL = b.mail("j.kaminski", "maastrichtuniversity.nl", "Email")

PREVNEXT = ('<nav class="pn" aria-label="More writing">'
            '<a class="prev" href="cdsm-2026.html"><span class="lbl">← Previous</span><span class="t">Causal Data Science Meeting 2026</span></a>'
            '<a class="next" href="essay.html"><span class="lbl">Next →</span><span class="t">Can we intervene inside a neural network?</span></a></nav>')
PN_CSS = """
.pn{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:32px;margin:56px 0 0;padding:28px 0 0;border-top:1px solid var(--rule)}
.pn a{text-decoration:none;color:inherit;min-width:0}
.pn .next{text-align:right}
.pn .lbl{display:block;margin-bottom:8px}
.pn .t{display:block;font:var(--display-weight) clamp(20px,1.8vw,26px)/1.2 var(--serif);letter-spacing:-.01em;text-wrap:balance}
.pn a:hover .t{color:var(--accent-text)}
@media (max-width:640px){.pn{grid-template-columns:minmax(0,1fr)}.pn .next{text-align:left}}
"""

OPTIONS = {
    # A: the byline card. Square portrait, name, role, two lines, one link.
    "a": (f'<div class="au au-a">{PORTRAIT}<div><span class="n">Jermain C. Kaminski</span><span class="r">Associate Professor, Maastricht University</span>'
          f'<p>I work on causal inference and machine learning for the decisions entrepreneurs make, and on the economic complexity of software.</p>'
          f'<a class="more" href="about.html">More about me</a></div></div>', """
.au-a{display:grid;grid-template-columns:96px minmax(0,1fr);gap:24px;align-items:start;padding:40px 0 8px;border-top:1px solid var(--rule)}
.au-a img{width:96px;height:96px;object-fit:cover;object-position:50% 18%;display:block}
.au-a .n{display:block;font:var(--display-weight) 26px/1.1 var(--serif);letter-spacing:-.015em}
.au-a .r{display:block;margin-top:4px;font-size:14px;color:var(--ink-3)}
.au-a p{margin:12px 0 0;font-size:var(--small);line-height:1.5;color:var(--ink-2);max-width:56ch}
.au-a .more{margin-top:12px;font-size:15px}
"""),
    # B: the signature. No picture; the name set like a signature, the role in small capitals.
    "b": (f'<div class="au au-b"><span class="sig">Jermain C. Kaminski</span><span class="lbl">Associate Professor of Entrepreneurship and Innovation · Maastricht University</span>'
          f'<p>{BIO}</p><a class="more" href="writing.html">More writing</a></div>', """
.au-b{padding:48px 0 8px;border-top:1px solid var(--ink);max-width:60ch}
.au-b .sig{display:block;font:italic 300 clamp(34px,3.2vw,44px)/1 var(--serif);letter-spacing:-.02em;color:var(--accent)}
.au-b .lbl{display:block;margin:14px 0 0}
.au-b p{margin:16px 0 0;font-size:var(--small);line-height:1.55;color:var(--ink-2)}
.au-b .more{margin-top:14px;font-size:15px}
"""),
    # C: the large portrait card, with two quiet buttons.
    "c": (f'<div class="au au-c">{PORTRAIT}<div><span class="lbl">Written by</span><span class="n">Jermain C. Kaminski</span><p>{BIO}</p>'
          f'<div class="btns"><a href="about.html">About me</a><a href="writing.html">All writing</a></div></div></div>', """
.au-c{display:grid;grid-template-columns:160px minmax(0,1fr);gap:36px;align-items:center;padding:48px 0 8px;border-top:1px solid var(--rule)}
.au-c img{width:160px;height:160px;object-fit:cover;object-position:50% 18%;display:block}
.au-c .lbl{display:block;margin-bottom:8px}
.au-c .n{display:block;font:var(--display-weight) clamp(28px,2.6vw,36px)/1.05 var(--serif);letter-spacing:-.02em}
.au-c p{margin:12px 0 18px;font-size:var(--small);line-height:1.5;color:var(--ink-2);max-width:56ch}
.btns{display:flex;flex-wrap:wrap;gap:10px}
.btns a{display:inline-block;padding:9px 16px;border:1px solid var(--ink);text-decoration:none;font-size:14.5px;color:var(--ink)}
.btns a:hover{background:var(--ink);color:#fff}
@media (max-width:640px){.au-c{grid-template-columns:minmax(0,1fr)}.au-c img{width:120px;height:120px}}
"""),
    # D: the page's own two-column section: "About the author" on the left, portrait and text on the right.
    "d": (f'<section class="part au au-d"><h2>About the author</h2><div class="body"><div class="row">{PORTRAIT}<div><span class="n">Jermain C. Kaminski</span>'
          f'<p>{BIO}</p><a class="more" href="about.html">About</a></div></div></div></section>', """
.au-d{margin-top:40px}
.au-d .row{display:grid;grid-template-columns:88px minmax(0,1fr);gap:20px;align-items:start}
.au-d img{width:88px;height:88px;object-fit:cover;object-position:50% 18%;display:block}
.au-d .n{display:block;font:var(--display-weight) 24px/1.1 var(--serif);letter-spacing:-.015em}
.au-d p{margin:10px 0 0;font-size:var(--small);line-height:1.5;color:var(--ink-2);max-width:54ch}
.au-d .more{margin-top:10px;font-size:15px}
"""),
    # E: the monogram. A large orange JK instead of a photograph.
    "e": (f'<div class="au au-e"><span class="mono">JK</span><div><span class="n">Jermain C. Kaminski</span><p>{BIO}</p>'
          f'<a class="more" href="about.html">More about me</a></div></div>', """
.au-e{display:grid;grid-template-columns:120px minmax(0,1fr);gap:28px;align-items:center;padding:44px 0 8px;border-top:1px solid var(--rule)}
.au-e .mono{font:300 88px/1 var(--serif);letter-spacing:-.05em;color:var(--accent)}
.au-e .n{display:block;font:var(--display-weight) 26px/1.1 var(--serif);letter-spacing:-.015em}
.au-e p{margin:10px 0 0;font-size:var(--small);line-height:1.5;color:var(--ink-2);max-width:56ch}
.au-e .more{margin-top:10px;font-size:15px}
"""),
    # F: a full-width warm band, portrait and text side by side.
    "f": (f'<div class="au au-f"><div class="in">{PORTRAIT}<div><span class="lbl">The author</span><span class="n">Jermain C. Kaminski</span><p>{BIO}</p>'
          f'<a class="more" href="about.html">More about me</a></div></div></div>', """
.au-f{margin:56px -48px 0;padding:40px 48px;background:#f6f4f2}
.au-f .in{display:grid;grid-template-columns:128px minmax(0,1fr);gap:32px;align-items:center;max-width:960px}
.au-f img{width:128px;height:128px;object-fit:cover;object-position:50% 18%;display:block}
.au-f .lbl{display:block;margin-bottom:8px}
.au-f .n{display:block;font:var(--display-weight) 28px/1.05 var(--serif);letter-spacing:-.02em}
.au-f p{margin:10px 0 0;font-size:var(--small);line-height:1.5;color:var(--ink-2);max-width:56ch}
.au-f .more{margin-top:12px;font-size:15px}
@media (max-width:900px){.au-f{margin-inline:-24px;padding:32px 24px}}
@media (max-width:640px){.au-f .in{grid-template-columns:minmax(0,1fr)}}
"""),
    # G: a serif sentence in the author's voice, with a small portrait.
    "g": (f'<div class="au au-g">{PORTRAIT}<div><p class="say">I study how entrepreneurs decide, and what data can and cannot tell them.</p>'
          f'<span class="n">Jermain C. Kaminski</span><span class="r">Associate Professor of Entrepreneurship and Innovation, Maastricht University · <a href="about.html">About</a></span></div></div>', """
.au-g{display:grid;grid-template-columns:72px minmax(0,1fr);gap:24px;align-items:start;padding:44px 0 8px;border-top:1px solid var(--rule)}
.au-g img{width:72px;height:72px;object-fit:cover;object-position:50% 18%;display:block;margin-top:6px}
.au-g .say{margin:0 0 14px;font:var(--display-weight) clamp(22px,2.2vw,30px)/1.3 var(--serif);letter-spacing:-.01em;color:var(--ink);max-width:40ch;text-wrap:pretty}
.au-g .n{display:block;font-size:15px;font-weight:500}
.au-g .r{display:block;margin-top:2px;font-size:14px;color:var(--ink-3)}
.au-g .r a{color:var(--accent-text);text-decoration:none}
"""),
    # H: the compact byline, one line.
    "h": (f'<div class="au au-h">{PORTRAIT}<p><strong>Written by Jermain C. Kaminski</strong>, Associate Professor of Entrepreneurship and Innovation at Maastricht University. '
          f'<a href="about.html">About</a> · <a href="writing.html">All writing</a></p></div>', """
.au-h{display:grid;grid-template-columns:56px minmax(0,1fr);gap:18px;align-items:center;padding:32px 0 8px;border-top:1px solid var(--rule)}
.au-h img{width:56px;height:56px;object-fit:cover;object-position:50% 18%;display:block}
.au-h p{margin:0;font-size:var(--small);line-height:1.5;color:var(--ink-2);max-width:64ch}
.au-h strong{font-weight:500;color:var(--ink)}
.au-h a{color:var(--accent-text);text-decoration:none}
"""),
}

STUB = ('<div class="pad head post-head"><span class="d">8 September 2025</span><h1>The Sistine Chapel Problem</h1></div>'
        '<div class="pad page"><article class="body article">'
        '<p>When language models can write a seemingly beautiful essay in seconds, what is the most important thing about learning?</p>'
        '<p>Ironically, while modern LLMs might pass Turing’s Imitation Game through text, they fail what we might call the ‘Sistine Chapel Test’: '
        'not whether they can describe experience convincingly, but whether they’ve had experience at all.</p>'
        '{pn}</article></div>')


def page(key):
    card, css = OPTIONS[key]
    main = STUB.format(pn=PREVNEXT)
    html = b.page("The Sistine Chapel Problem: Jermain C. Kaminski", main, "writing", article=("2025-09-08", "The Sistine Chapel Problem"))
    foot = ('<footer class="close slim" id="contact"><div class="pad in">' + card
            + '<div class="colophon">' + b.FOOT.split('<div class="colophon">', 1)[1])
    html = html.replace(b.AUTHOR, foot, 1)
    html = html.replace("</head>", f"<style>{PN_CSS}{css}</style></head>", 1)
    return site.localize(html)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "wall.css").write_text((HERE / "wall.css").read_text(encoding="utf8"), encoding="utf8")
    for key in OPTIONS:
        (OUT / f"{key}.html").write_text(page(key), encoding="utf8")
