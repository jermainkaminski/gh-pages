#!/usr/bin/env python3
"""Builds the site preview into site/: home, sub-pages, writing page and posts."""
import re
import shutil
import subprocess
from pathlib import Path

import build as b
from content import PHOTO
from fonts import VARIANTS

HERE = Path(__file__).parent
OUT = HERE / "site"

POSTS = [
    {"file": "cdsm-2026.html", "vt": "post-cdsm", "og": "https://jermainkaminski.com/media/posts/9/cdsm-2026-header.jpg", "src": "causal-data-science-meeting-2026", "title": "Causal Data Science Meeting 2026",
     "date": "16 October 2026", "img": "cdsm-2026-header.jpg", "w": 2560, "h": 1707,
     "alt": "Causal Data Science Meeting, November 4–5, 2026, online", "note": "Causal Data Science Meeting 2026, online on 4–5 November.",
     "blurb": "Online on 4–5 November: two days of talks and discussion on causal data science, machine learning and AI. Attendance is free, and more than 650 participants have already registered."},
    {"file": "essay.html", "vt": "post-essay", "og": "https://jermainkaminski.com/media/posts/19/Will20Hunting.jpg.webp", "src": "the-sistine-chapel-problem", "title": "The Sistine Chapel Problem",
     "date": "8 September 2025", "img": "Will20Hunting.jpg.webp", "w": 1280, "h": 720,
     "alt": "Park bench scene from the 1997 film Good Will Hunting", "note": "Good Will Hunting (1997): the park bench scene.",
     "blurb": "When language models can write a seemingly beautiful essay in seconds, what is the most important thing about learning? The answer can be found in a park bench conversation from a 1997 movie."},
]
b.LOCAL["causal-data-science-meeting-2026"] = "cdsm-2026"
b.NAV.insert(3, ("writing", "Writing"))
b.FOOT = b.FOOT.replace('<a href="essay.html">Writing</a>', '<a href="writing.html">Writing</a>')


def img(p, lazy=True):
    return (f'<img src="media/{p["img"]}" width="{p["w"]}" height="{p["h"]}" alt="{p["alt"]}"'
            f' style="view-transition-name:{p["vt"]}"{" loading=" + chr(34) + "lazy" + chr(34) if lazy else ""}>')


def head(title="Latest writing"):
    return f'<div class="bh"><h2 class="sec-h">{title}</h2><a class="more" href="writing.html">All writing</a></div>'


def cards(cls=""):
    items = "".join(f'<a class="card" href="{p["file"]}"><span class="pic">{img(p)}</span><span class="note">{p["note"]}</span><span class="d">{p["date"]}</span>'
                    f'<span class="t">{p["title"]}</span><span class="s">{p["blurb"]}</span></a>' for p in POSTS)
    return f'<div class="cards {cls}">{items}</div>'


def rows():
    return '<div class="rows">' + "".join(
        f'<a class="rw" href="{p["file"]}"><span class="d">{p["date"]}</span><span class="t">{p["title"]}</span>'
        f'<span class="s">{p["blurb"]}</span><span class="pic">{img(p)}</span></a>' for p in POSTS) + "</div>"


def sections():
    hero, rest = b.home_parts()
    bits = re.split(r'(?=<section |<div class="pad">\s*<figure class="river")', rest)
    named = {}
    for bit in bits:
        m = re.search(r'id="(\w+)"', bit[:80])
        if m:
            named[m.group(1)] = bit
        elif "river" in bit[:80]:
            named["river"] = bit
    named["pillars"] = named["pillars"].replace('class="sec pad"', 'class="sec pad"', 1)
    named["work"] = named["work"].replace(' style="padding-top:0"', "")
    return hero, named


def rest_of(named, *keys):
    return "\n".join(named[k] for k in keys)


REST = ("pillars", "work", "river", "about", "teaching", "events")


def home_page(hero, s):
    return hero + f'<section class="sec pad blog">{head()}{cards()}</section>' + rest_of(s, *REST)


def curly(text):
    """Typographer's quotes in a run of text."""
    text = re.sub(r"(?<=\w)'", "’", text)
    text = re.sub(r"(^|[\s(\[])'", r"\1‘", text).replace("'", "’")
    text = re.sub(r'(^|[\s(\[])"', r"\1“", text)
    return text.replace('"', "”")


def typeset(page):
    head, body = page.split("<body>", 1)
    body, script = body.split("<script>", 1)  # the script keeps its straight quotes
    return head + "<body>" + "".join(bit if bit.startswith("<") else curly(bit) for bit in re.split(r"(<[^>]+>)", body)) + "<script>" + script


def size_of(name):
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(HERE / "media" / name)], capture_output=True, text=True).stdout
    return re.findall(r"pixel\w+: (\d+)", out)


def localize(s):
    def sized(m):
        w, h = size_of(m.group(1))
        return f'<img src="media/{m.group(1)}" width="{w}" height="{h}"'
    s = re.sub(r'<img src="media/([^"]+)"(?! width)', sized, s)
    s = s.replace('src="media/', 'src="../media/').replace("https://jermainkaminski.com/causal-data-science-meeting-2026/", "cdsm-2026.html")
    return typeset(s)


def post_page(p):
    h = b.tidy(b.body_of(p["src"]))
    h = re.sub(r'(<a href="[^"]*youtube[^"]*">)(<strong>.*?</strong>)(.*?)</a>', r'<p class="play">\1\2</a><br>\3</p>', h)
    main = (f'<div class="pad head post-head"><span class="d">{p["date"]}</span><h1>{p["title"]}</h1></div>'
            f'<div class="pad"><figure class="band post">{img(p, False)}<figcaption class="note">{p["note"]}</figcaption></figure></div>'
            f'<div class="pad page"><article class="body article">{h}</article></div>')
    return b.page(f'{p["title"]}: Jermain C. Kaminski', main, "writing", p["blurb"], p["og"])


def writing_page():
    main = f'<div class="pad head"><h1>Writing</h1></div><div class="pad page post-list">{rows()}</div>'
    return b.page("Writing: Jermain C. Kaminski", main, "writing")


def switcher(variant, file):
    """Preview only: a small fixed bar for moving between the type versions of the same page."""
    links = "".join(f'<a href="../site-{k}/{file}"{" aria-current=" + chr(34) + "true" + chr(34) if k == variant else ""}>{v["name"]}</a>'
                    for k, v in VARIANTS.items())
    return f'<nav class="pv" aria-label="Type versions"><span>Type</span>{links}</nav></body>'


def build(out, variant=None):
    """Writes every page into out/. With a variant, its fonts and CSS replace the Newsreader pairing."""
    v = VARIANTS[variant or "newsreader"]
    b.FONTS = v["fonts"]
    out.mkdir(exist_ok=True)
    (out / "wall.css").write_text((HERE / "wall.css").read_text(encoding="utf8") + v["css"] + (PV_CSS if variant else ""), encoding="utf8")
    hero, named = sections()
    pages = {"index.html": b.page("Jermain C. Kaminski, Associate Professor of Entrepreneurship and Innovation", home_page(hero, named))}
    pages.update({f"{key}.html": b.subpage(key) for key in b.PAGES})
    pages.update({p["file"]: post_page(p) for p in POSTS})
    pages["writing.html"] = writing_page()
    for file, page in pages.items():
        page = localize(page)
        if variant:
            page = page.replace("</body>", switcher(variant, file), 1)
        (out / file).write_text(page, encoding="utf8")


PV_CSS = """
/* preview switcher, not part of the design */
.pv{position:fixed;right:16px;bottom:16px;z-index:50;display:flex;gap:2px;background:var(--ink);color:#fff;font:500 12px/1 var(--sans);letter-spacing:.02em;padding:4px;box-shadow:0 2px 12px rgba(20,28,48,.25)}
.pv span,.pv a{padding:7px 9px;text-decoration:none;color:#fff}
.pv span{opacity:.6}
.pv a:hover{background:rgba(255,255,255,.14);color:#fff}
.pv a[aria-current]{background:#fff;color:var(--ink)}
@media print{.pv{display:none}}
"""


if __name__ == "__main__":
    import sys
    build(OUT)
    if "--variants" in sys.argv:  # the other type pairings, for comparison only
        for k in VARIANTS:
            build(HERE / f"site-{k}", k)
