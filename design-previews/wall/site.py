#!/usr/bin/env python3
"""Builds the site preview into site/: home, sub-pages, writing page and posts."""
import re
import subprocess
from pathlib import Path

import build as b
from content import collab_html, news_html

PULL = '<p class="pull">Experience cannot be summarized or transferred; it has to be discovered through years of attention, presence, and engagement.</p>\n'

HERE = Path(__file__).parent
OUT = HERE / "site"

POSTS = [
    {"file": "cdsm-2026.html", "vt": "post-cdsm", "og": "https://jermainkaminski.com/media/posts/9/cdsm-2026-header.jpg", "src": "causal-data-science-meeting-2026", "title": "Causal Data Science Meeting 2026",
     "date": "16 October 2026", "iso": "2026-10-16", "kicker": "Announcement", "read": "3 min", "img": "UM-Tapijn-202011-022.jpg", "w": 7952, "h": 5304,
     "alt": "A corridor at Tapijn with yellow, orange, red and blue study alcoves in timber frames", "note": "<b>Tapijn campus</b>Maastricht University",
     "blurb": "Online on 4–5 November: two days of talks and discussion on causal data science, machine learning and AI. Attendance is free, and more than 1,600 participants have already registered.",
     "desc": "Causal Data Science Meeting 2026, online on 4–5 November: two free days of talks on causal data science, machine learning and AI."},
    {"file": "essay.html", "vt": "post-essay", "og": "https://jermainkaminski.com/media/posts/19/Will20Hunting.jpg.webp", "src": "the-sistine-chapel-problem", "title": "The Sistine Chapel Problem",
     "date": "8 September 2025", "iso": "2025-09-08", "kicker": "Essay", "read": "9 min", "img": "Will20Hunting.jpg.webp", "w": 1280, "h": 720,
     "alt": "Park bench scene from the 1997 film Good Will Hunting", "note": "<b>Good Will Hunting</b>1997, the park bench scene",
     "blurb": "When language models can write a seemingly beautiful essay in seconds, what is the most important thing about learning? The answer can be found in a park bench conversation from a 1997 movie.",
     "desc": "When language models write a beautiful essay in seconds, what still matters about learning? An answer from a park bench in Good Will Hunting."},
]
b.LOCAL["causal-data-science-meeting-2026"] = "cdsm-2026"
b.NAV.insert(3, ("writing", "Writing"))
b.FOOT = b.FOOT.replace('<a href="essay.html">Writing</a>', '<a href="writing.html">Writing</a>')


def img(p, lazy=True):
    return (f'<img src="media/{p["img"]}" width="{p["w"]}" height="{p["h"]}" alt="{p["alt"]}"'
            f' style="view-transition-name:{p["vt"]}"{" loading=" + chr(34) + "lazy" + chr(34) if lazy else ""}>')


def head(title="Latest writing"):
    return f'<div class="bh"><h2 class="sec-h">{title}</h2><a class="more" href="writing.html">All writing</a></div>'


def cards():
    items = "".join(f'<a class="card" href="{p["file"]}"><span class="pic">{img(p)}</span><span class="t">{p["title"]}</span>'
                    f'<span class="d">{p["date"]}</span><span class="s">{p["blurb"]}</span></a>' for p in POSTS)
    return f'<div class="cards">{items}</div>'


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
    named["work"] = named["work"].replace(' style="padding-top:0"', "")
    return hero, named


def rest_of(named, *keys):
    return "\n".join(named[k] for k in keys)


REST = ("pillars", "work", "river", "about", "teaching", "collab", "news", "events")


def home_page(hero, s):
    s = dict(s)
    s["collab"] = f'<section class="sec pad" id="collab"><h2 class="sec-h">Work with me</h2>{collab_html()}</section>'
    s["news"] = (f'<section class="sec pad" id="news"><div class="bh"><h2 class="sec-h">In the news</h2>'
                 f'<a class="more" href="news.html">All coverage</a></div>{news_html()}</section>')
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
    s = s.replace('src="media/', 'src="../media/').replace('<a href="https://jermainkaminski.com/causal-data-science-meeting-2026/"', '<a href="cdsm-2026.html"')
    return typeset(s)


def prev_next(p):
    """Newest first in POSTS: next is the newer piece, previous the older."""
    i = POSTS.index(p)
    older = POSTS[i + 1] if i + 1 < len(POSTS) else None
    newer = POSTS[i - 1] if i > 0 else None
    links = ""
    if older:
        links += f'<a class="prev" href="{older["file"]}"><span class="lbl">← Previous</span><span class="t">{older["title"]}</span></a>'
    if newer:
        links += f'<a class="next" href="{newer["file"]}"><span class="lbl">Next →</span><span class="t">{newer["title"]}</span></a>'
    return f'<nav class="pn" aria-label="More writing">{links}</nav>' if links else ""


def post_page(p):
    h = b.tidy(b.body_of(p["src"]))
    h = re.sub(r'(<a href="[^"]*youtube[^"]*">)(<strong>.*?</strong>)(.*?)</a>', r'<p class="play">\1\2</a><br>\3</p>', h)
    if p["kicker"] == "Essay":  # one sentence pulled into the margin
        h = h.replace("<p>Ironically,", PULL + "<p>Ironically,", 1)
    main = (f'<div class="runhead" aria-hidden="true"><a class="who" href="index.html">Jermain C. Kaminski</a><span class="t">{p["title"]}</span></div>'
            f'<div class="pad head post-head"><span class="d">{p["date"]}</span><h1>{p["title"]}</h1></div>'
            f'<div class="pad"><figure class="band post">{img(p, False)}<figcaption class="note">{p["note"]}</figcaption></figure></div>'
            f'<div class="pad page{" is-essay" if p["kicker"] == "Essay" else ""}"><article class="body article">{h}{prev_next(p)}</article></div>')
    return b.page(f'{p["title"]}: Jermain C. Kaminski', main, "writing", p["desc"], p["og"], path=p["src"] + "/", article=(p["iso"], p["title"]))


def writing_page():
    cards = "".join(f'<a class="mag" href="{p["file"]}"><span class="pic">{img(p)}</span><span class="kick">{p["kicker"]} · {p["read"]} read</span>'
                    f'<span class="t">{p["title"]}</span><span class="s">{p["blurb"]}</span><span class="meta">{p["date"]}</span></a>' for p in POSTS)
    main = f'<div class="pad head"><h1>Writing</h1></div><div class="pad page"><div class="maggrid">{cards}</div></div>'
    return b.page("Writing: Jermain C. Kaminski", main, "writing", author=True)


def build(out):
    """Writes every page into out/."""
    out.mkdir(exist_ok=True)
    (out / "wall.css").write_text((HERE / "wall.css").read_text(encoding="utf8"), encoding="utf8")
    hero, named = sections()
    pages = {"index.html": b.page("Jermain C. Kaminski, Associate Professor, Maastricht University", home_page(hero, named))}
    pages.update({f"{key}.html": b.subpage(key) for key in b.PAGES})
    pages.update({p["file"]: post_page(p) for p in POSTS})
    pages["writing.html"] = writing_page()
    pages["news.html"] = b.news_page()
    for file, page in pages.items():
        (out / file).write_text(localize(page), encoding="utf8")


if __name__ == "__main__":
    build(OUT)
