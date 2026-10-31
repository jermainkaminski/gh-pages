#!/usr/bin/env python3
"""Page helpers for the site preview. Sub-page text and links are read
from the live site's pages in this repo, so the wording stays Jermain's own."""
import html
import json
import re
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

from content import pillars_html

HERE = Path(__file__).parent
REPO = HERE.parent.parent

ARROW = ('<svg viewBox="0 0 12 12" width="11" height="11" aria-hidden="true">'
         '<path d="M2.5 9.5 9.5 2.5M4 2.5h5.5V8" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>')
NOTES = {  # the short note under each photograph on phones
    "home": "At the School of Business and Economics, Maastricht University.",
    "about": "At the School of Business and Economics, Maastricht University.",
    "research": "The Charles River at MIT, Cambridge, Massachusetts.",
    "teaching": "An MBA class at Maastricht University.",
    "students": "Tapijn campus, Maastricht University.",
    "speaking": "Jermain Kaminski.",
}
PAGES = {  # output name: (source folder, title, hero image, hero alt)
    "about": ("welcome", "About", None, ""),
    "research": ("research", "Research", "MITSailing-1.jpg", "Numbered sailing dinghies on a dock on the Charles River, with the Boston skyline across the water"),
    "publications": ("publications", "Publications", None, ""),
    "teaching": ("teaching", "Teaching", "MBA-LR-5.jpg", "Jermain Kaminski teaching a seated MBA class in a long timber-floored room"),
    "students": ("students", "Students", "UM-Tapijn-202011-022.jpg", "Maastricht University's Tapijn campus"),
    "speaking": ("speaking-and-workshops", "Speaking &amp; Advisory", "Jermain-Kaminski-1-md.jpg", "Portrait of Jermain Kaminski"),
}
ESSAY_SRC = "the-sistine-chapel-problem"
NAV = [("about", "About"), ("research", "Research"), ("publications", "Publications"),
       ("teaching", "Teaching"), ("students", "Students"), ("speaking", "Speaking"), ("news", "News")]
LOCAL = {"welcome": "about", "research": "research", "publications": "publications", "teaching": "teaching",
         "students": "students", "speaking-and-workshops": "speaking", ESSAY_SRC: "essay"}


def local_href(href):
    m = re.fullmatch(r"https://jermainkaminski\.com/([a-z-]+)/?", href)
    if m and m.group(1) in LOCAL:
        return LOCAL[m.group(1)] + ".html"
    if href == "causalscience.org":  # broken relative link on the live speaking page
        return "https://causalscience.org"
    return href


class Clean(HTMLParser):
    """Keeps only structure and links; drops Publii's classes, spans and inline styles."""
    KEEP = {"p", "ul", "ol", "li", "em", "strong", "blockquote", "br", "figure", "figcaption"}
    RENAME = {"i": "em", "b": "strong", "h1": "h2", "h2": "h2", "h3": "h2", "h4": "h2", "h5": "h2", "h6": "h2"}

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
            return
        a = dict(attrs)
        tag = self.RENAME.get(tag, tag)
        if tag == "a" and a.get("href"):
            cls = ' class="chip"' if "btn" in (a.get("class") or "") else ""
            self.out.append(f'<a{cls} href="{html.escape(local_href(html.unescape(a["href"])), quote=True)}">')
        elif tag == "img" and a.get("src"):
            name = a["src"].rsplit("/", 1)[-1]
            self.out.append(f'<img src="media/{name}" alt="{html.escape(a.get("alt") or "", quote=True)}" loading="lazy">')
        elif tag in self.KEEP or tag == "h2":
            self.out.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
            return
        tag = self.RENAME.get(tag, tag)
        if tag == "a" or tag in self.KEEP or tag == "h2":
            if tag != "br":
                self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)

    def handle_entityref(self, name):
        self.out.append(f"&{name};")

    def handle_charref(self, name):
        self.out.append(f"&#{name};")


TYPOS = {  # corrected here until the live pages are fixed in Publii
    "Entrepreneuership": "Entrepreneurship",
    "bandwith": "bandwidth",
    "could together on": "could work together on",
    "sparrings partner": "sparring partner",
    "I enjoy to trigger": "I enjoy triggering",
    "in a the famous": "in the famous",
    "powerful and tools": "powerful tools",
    "18-39 year old who": "18–39-year-olds who",
    "Awwards": "Awwwards",
}


GITHUB_POST = ('GitHub Blog (2026). <a href="https://github.blog/news-insights/policy-news-and-insights/how-researchers-are-using-github-innovation-graph-data-to-reveal-the-digital-complexity-of-nations/">'
               'How researchers are using GitHub Innovation Graph data to reveal the “digital complexity” of nations</a>.')
SILICON = "Kaminski, J. (2026). Silicon sampling for product feedback in entrepreneurship. Working paper. The title was changed for peer review."


def body_of(folder):
    s = (REPO / folder / "index.html").read_text(encoding="utf8")
    for wrong, right in TYPOS.items():
        s = s.replace(wrong, right)
    i = s.index('content__inner content__entry"')
    i = s.index(">", i) + 1
    ends = [j for j in (s.find("<footer", i), s.find("</article>", i)) if j > 0]
    c = Clean()
    c.feed(s[i:min(ends)])
    h = "".join(c.out)
    h = re.sub(r"\s*&nbsp;\s*", " ", h)
    h = re.sub(r'(<a[^>]*>)([^<]*)</a>\s*\1', r"\1\2", h)  # one link split in two by the editor
    for _ in range(3):
        h = re.sub(r"<(p|h2|li|em|strong|ul|a)(\s[^>]*)?>\s*</\1>", "", h)
    h = re.sub(r"<strong>([^<]*)</strong>(?=</h2>)", r"\1", h)
    h = re.sub(r"<h2><strong>(.*?)</strong></h2>", r"<h2>\1</h2>", h)
    h = re.sub(r"<h2>\s*(<figure>.*?</figure>)\s*</h2>", r"\1", h, flags=re.S)  # photo wrapped in a heading
    return h.strip()


def tidy(h):
    """Repairs spacing left by the editor: stray breaks, spaces before punctuation, doubled spaces."""
    h = re.sub(r"<br>", " ", h)
    h = re.sub(r";\s*</a>", "</a>; ", h)
    h = re.sub(r"\s+", " ", h)
    h = re.sub(r"\s+</a>", "</a> ", h)
    h = re.sub(r"(</a>|</em>)\s+([,.;:!?])", r"\1\2", h)
    h = re.sub(r"\s+([,;:!?])(?=\s)", r"\1", h)
    return h.replace("<p> ", "<p>").replace(" </p>", "</p>")


def cite_row(inner):
    """One publication: authors, title on its own line, venue. The year also goes in the margin."""
    inner = inner.strip().rstrip(";").strip()
    text = re.sub(r"<[^>]+>", " ", inner)
    y = re.search(r"\b(?:19|20)\d{2}\b", text)
    au = ti = ve = None
    inner = re.sub(r"<em>(<a .*?</a>)(.*?)</em>", r"\1\2", inner)
    linked = re.match(r"(.*?)(<a [^>]*>(?!\()[^<]*</a>)\s*([.,?!:]*)\s*(.*)$", inner)
    if inner.count("<a ") == 1 and linked:
        m = linked
        au, ti, ve = m.group(1), m.group(2) + ("" if m.group(2)[-5] in ".?!" else m.group(3)), m.group(4)
    elif "<a " not in inner:
        m = (re.match(r"(.*?\(\d{4}[^)]*\)\.)\s*(.*?\.)\s*(.*)$", inner)
             or re.match(r"(.*?),\s*(“.*?”)\s*(.*)$", inner))
        if m:
            au, ti, ve = m.groups()
    if ti:  # titles are not sentences
        ti = re.sub(r"[\s.,:]+$", "", ti.strip())
        ti = re.sub(r"(</a>)[.,:]+$", r"\1", ti).replace(",”", "”")
    if au:  # the year is in the margin
        au = re.sub(r"\s+-\s*$", "", au)
        au = re.sub(r"\s*\(\d{4}[^)]*\)\.?\s*$", "", au)
    if ve:  # italics are for journal names, not for a paper's status
        ve = re.sub(r"<em>((?:Preparing|Under Review|Resubmit|Available at)[^<]*)</em>", r"\1", ve)
        if re.fullmatch(r"\s*\(\d{4}\)\.?\s*", ve):
            ve = None
    if ti is None and (m := re.match(r"(Vlees Magazine) \(.*?\)\.\s*(.*?)\s*<a [^>]*>", inner)):
        link = re.search(r'<a [^>]*>.*?</a>', inner).group(0)
        au, ti = m.group(1), f"{m.group(2)} {link}"
    if ti is None:
        content = f"<p>{inner}</p>"
    else:
        content = "".join(f'<span class="{c}">{v.strip()}</span>' for c, v in (("au", au), ("ti", ti), ("ve", ve)) if v and v.strip())
        content = f"<p>{content}</p>"
    return f'<div class="cite"><span class="yr">{y.group(0) if y else ""}</span>{content}</div>'


def citations(chunk):
    def row(m):
        inner = m.group(1)
        if inner.startswith("Moviegalaxies (Selection):"):  # one long paragraph on the live site
            items = re.split(r";\s*|(?<=</a>\.)\s+(?=<a )", inner.split(":", 1)[1])
            return '<h3>Moviegalaxies (Selection)</h3>' + "".join(cite_row(i) for i in items if i.strip())
        return cite_row(inner)
    return re.sub(r"<p>(.*?)</p>", row, chunk, flags=re.S)


def grants(chunk):
    def row(m):
        amount = re.search(r"\s*\(([\d,]+ [A-Z]{3})\)", m.group(2))
        what = m.group(2).replace(amount.group(0), "") if amount else m.group(2)
        return (f'<li class="grant"><span class="yr">{m.group(1)}</span><span>{what.strip()}</span>'
                f'<span class="amt">{amount.group(1) if amount else ""}</span></li>')
    return re.sub(r"<li>(\d{4})\s+(.*?)</li>", row, chunk, flags=re.S)


def awards(chunk):
    text = re.search(r"<p>(.*?)</p>", chunk, flags=re.S).group(1).rstrip(". ")
    text = text.replace("London, UK Young", "London, UK; Young")  # separator missing on the live page
    return "<ul>" + "".join(f"<li>{a.strip()}</li>" for a in re.split(r"(?<!&amp);", text)) + "</ul>"


def courses(chunk):
    def row(m):
        rate = re.search(r"\s*\(\s*([\d.]+)\s*/\s*([\d.]+)\s*\)\s*$", m.group(1))
        if not rate:
            return f'<li class="course"><span>{m.group(1)}</span></li>'
        return (f'<li class="course"><span>{m.group(1)[:rate.start()]}</span>'
                f'<span class="rate">{rate.group(1)}<small> / {rate.group(2)}</small></span></li>')
    return re.sub(r"<li>(.*?)</li>", row, chunk, flags=re.S)


def quotes(chunk):
    return re.sub(r"<blockquote><p>(.*?)\s*[–—]\s*([^–—]*?)</p></blockquote>",
                  r'<blockquote><p>\1</p><footer>\2</footer></blockquote>', chunk, flags=re.S)


SHAPE = {"Grants and Collaborations": grants, "Awards and Honors (Selection)": awards, "Courses": courses,
         "Teaching Statement": quotes}


def parts(h, cite=False):
    bits = re.split(r"<h2>(.*?)</h2>", tidy(h), flags=re.S)
    out = []
    if bits[0].strip():
        out.append(f'<section class="part lead"><div></div><div class="body">{bits[0]}</div></section>')
    for title, chunk in zip(bits[1::2], bits[2::2]):
        title = title.strip()
        chunk = citations(chunk) if cite else SHAPE.get(title, str)(chunk)
        out.append(f'<section class="part"><h2>{title}</h2><div class="body">{chunk.strip()}</div></section>')
    return "\n".join(out)


def nav(current=None):
    items = "".join(
        f'<li><a href="{k}.html"{" aria-current=" + chr(34) + "page" + chr(34) if k == current else ""}>{v}</a></li>'
        for k, v in NAV)
    badge = ("" if current else  # hangs from the top-right corner; every page keeps the corner free, so the menu never moves
             '<a class="badge" href="https://poetsandquants.com/2024/05/18/2024-best-40-under-40-mba-professors-jermain-kaminski-maastricht-university-school-of-business-and-economics/">'
             '<img src="media/40under40logo.jpg" width="271" height="459" alt="Poets&amp;Quants Best 40 Under 40 Professors"></a>')
    # On phones the list becomes a full-screen sheet, opened by the checkbox behind the burger; no script needed
    return (f'<div class="pad"><nav class="top{"" if current else " home"}" aria-label="Main">'
            f'<input type="checkbox" id="menu" class="menu-t" aria-label="Menu" autocomplete="off"><a class="who" href="index.html">Jermain C. Kaminski</a>'
            f'<label for="menu" class="burger" aria-hidden="true"><svg viewBox="0 0 24 24" width="24" height="24">'
            f'<line x1="2" y1="5" x2="22" y2="5"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="19" x2="22" y2="19"/></svg></label>'
            f'<ul>{items}<li class="m-only"><a href="#contact">Get in touch</a></li>'
            f'<li class="m-only soc"><a href="https://www.linkedin.com/in/jermainkaminski/">LinkedIn</a><a href="https://bsky.app/profile/jermainkaminski.bsky.social">Bluesky</a></li></ul>'
            f'<a class="pill" href="#contact">Get in touch</a>{badge}</nav></div>')


def mail(user, domain, text=None):
    """An email link harvesters have to work for: the address is assembled by the script, and reads 'user at domain' without it."""
    shown = text or f'{user}<span class="at"> at </span>{domain}'
    return f'<a class="mailto" data-u="{user}" data-d="{domain}" href="#contact">{shown}</a>'


FOOT = """<footer class="close" id="contact">
  <div class="pad in">
    <h2>Let's <em>work together.</em></h2>
    <div class="routes">
      <div><p>Research collaboration:</p><div class="mail">""" + mail("j.kaminski", "maastrichtuniversity.nl") + """</div></div>
      <div><p>Speaking, workshops and advisory:</p><div class="mail">""" + mail("jermain.kaminski", "gmail.com") + """</div></div>
    </div>
    <div class="colophon">
      <span>Jermain C. Kaminski</span>
      <nav aria-label="Elsewhere"><a href="essay.html">Writing</a><a href="https://www.linkedin.com/in/jermainkaminski/">LinkedIn</a><a href="https://bsky.app/profile/jermainkaminski.bsky.social">Bluesky</a><a href="https://jermainkaminski.com/privacy/">Privacy</a></nav>
      <span class="upd">Last updated """ + date.today().strftime("%-d %B %Y") + """</span>
    </div>
  </div>
</footer>"""


DESCRIPTIONS = {
    None: "Associate Professor of Entrepreneurship and Innovation at Maastricht University. Causal inference and machine learning for the decisions founders make.",
    "about": "About Jermain C. Kaminski, Associate Professor of Entrepreneurship and Innovation at Maastricht University.",
    "research": "Jermain C. Kaminski's research: causality in strategic decision making, machine learning in entrepreneurship, and the economic complexity of software.",
    "publications": "Working papers, journal articles and conference papers by Jermain C. Kaminski.",
    "teaching": "Courses and teaching statement of Jermain C. Kaminski at Maastricht University.",
    "students": "PhD, master and honours students supervised by Jermain C. Kaminski.",
    "speaking": "Keynotes, executive workshops and advisory by Jermain C. Kaminski on causal thinking, AI and strategy, and advisor to Texterous.",
    "writing": "Essays and announcements by Jermain C. Kaminski on learning, AI, causality and entrepreneurship.",
    "news": "Press and media coverage of Jermain C. Kaminski's research and teaching.",
}
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23d0450c'/%3E"
        "%3Cpath d='M6 16h18M17 9l7 7-7 7' fill='none' stroke='%23fff' stroke-width='3'/%3E%3C/svg%3E")
OG_IMAGE = "https://jermainkaminski.com/media/posts/12/Jermain-Kaminski-1-md-Kopie-3.jpg"
IMAGE_ALT = {OG_IMAGE: "Jermain Kaminski in a bright university corridor at Maastricht University, in a blue blazer and pink bow tie"}


SITE = "https://jermainkaminski.com/"
PERSON = {  # structured data shared by every page: who the site is about, and where else he is
    "@type": "Person", "@id": SITE + "#person", "name": "Jermain C. Kaminski", "givenName": "Jermain", "familyName": "Kaminski",
    "jobTitle": "Associate Professor of Entrepreneurship and Innovation", "url": SITE, "image": OG_IMAGE,
    "description": "Associate Professor of Entrepreneurship and Innovation at Maastricht University School of Business and Economics. "
                   "Research on causal inference and machine learning for entrepreneurial and strategic decisions, and on the economic "
                   "complexity of software. Co-founder of the Causal Data Science Meeting and Moviegalaxies; advisor to Texterous.",
    "worksFor": {"@type": "Organization", "name": "Maastricht University School of Business and Economics", "url": "https://www.maastrichtuniversity.nl/about-um/faculties/school-business-and-economics"},
    "affiliation": [
        {"@type": "Organization", "name": "Maastricht University", "url": "https://www.maastrichtuniversity.nl/"},
        {"@type": "Organization", "name": "Causal Data Science Meeting", "url": "https://causalscience.org/"},
        {"@type": "Organization", "name": "Texterous", "url": "https://texterous.com/"},
    ],
    "hasOccupation": [
        {"@type": "Role", "roleName": "Associate Professor", "worksFor": {"@type": "Organization", "name": "Maastricht University"}},
        {"@type": "Role", "roleName": "Advisor", "worksFor": {"@type": "Organization", "name": "Texterous", "url": "https://texterous.com/"}},
    ],
    "alumniOf": [{"@type": "CollegeOrUniversity", "name": "RWTH Aachen University"}],
    "award": "Poets&Quants Best 40 Under 40 MBA Professors, 2024",
    "knowsAbout": ["causal inference", "causal machine learning", "machine learning", "entrepreneurship", "entrepreneurial finance",
                   "crowdfunding", "strategy", "innovation", "economic complexity", "open-source software", "large language models"],
    "sameAs": ["https://www.linkedin.com/in/jermainkaminski/", "https://bsky.app/profile/jermainkaminski.bsky.social",
               "https://scholar.google.com/citations?user=b-HX-AYAAAAJ", "https://www.semanticscholar.org/author/Jermain-Kaminski/39736726",
               "https://policyprofiles.sagepub.com/profile/6676/jermain-kaminski", "https://www.rankless.org/authors/jermain-kaminski",
               "https://www.maastrichtuniversity.nl/j.kaminski"],
}
WEBSITE = {"@type": "WebSite", "@id": SITE + "#website", "url": SITE, "name": "Jermain C. Kaminski", "inLanguage": "en",
           "publisher": {"@id": SITE + "#person"}}


def page(title, main, current=None, desc=None, image=OG_IMAGE, path=None, article=None):
    """One page. path is the page's folder on the live site; article is (date ISO, headline) for a post."""
    desc = html.escape(desc or DESCRIPTIONS.get(current) or DESCRIPTIONS[None], quote=True)
    t = html.escape(title, quote=True)
    if path is None:
        path = "" if current is None else PAGES[current][0] + "/" if current in PAGES else current + "/"
    url = SITE + path
    kind = "article" if article else ("profile" if current is None else "website")
    graph = [PERSON, WEBSITE, {"@type": "WebPage", "@id": url, "url": url, "name": html.unescape(title), "description": html.unescape(desc),
                               "isPartOf": {"@id": SITE + "#website"}, "about": {"@id": SITE + "#person"}, "inLanguage": "en",
                               "primaryImageOfPage": image}]
    if current is None:
        graph[2]["@type"] = "ProfilePage"
        graph[2]["mainEntity"] = {"@id": SITE + "#person"}
    extra = ""
    if article:
        published, headline = article
        graph.append({"@type": "BlogPosting", "@id": url + "#post", "headline": headline, "url": url, "datePublished": published,
                      "dateModified": published, "image": image, "description": html.unescape(desc), "inLanguage": "en",
                      "author": {"@id": SITE + "#person"}, "publisher": {"@id": SITE + "#person"}, "mainEntityOfPage": {"@id": url}})
        extra = f'\n<meta property="article:published_time" content="{published}">\n<meta property="article:author" content="{SITE}">'
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Jermain C. Kaminski">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="{kind}">
<meta property="og:site_name" content="Jermain C. Kaminski">
<meta property="og:locale" content="en_US">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{image}">
<meta property="og:image:alt" content="{html.escape(IMAGE_ALT.get(image, 'Jermain C. Kaminski'), quote=True)}">{extra}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{image}">
<script type="application/ld+json">{ld}</script>
<link rel="icon" href="{ICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS}&display=swap">
<link rel="stylesheet" href="wall.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{nav(current)}
<main id="main">
{main}
</main>
{FOOT}
<script>
// The sheet menu works without this; it only closes the sheet on a same-page link and on Escape.
document.querySelectorAll("a.mailto").forEach(function(a){{var e=a.dataset.u+"@"+a.dataset.d;a.href="mailto:"+e;if(a.querySelector(".at"))a.textContent=e}});
(function(){{var m=document.getElementById("menu");if(!m)return;
m.checked=false;window.addEventListener("pageshow",function(){{m.checked=false}});
document.querySelectorAll("nav.top ul a").forEach(function(a){{a.addEventListener("click",function(){{m.checked=false}})}});
document.addEventListener("keydown",function(e){{if(e.key==="Escape"&&m.checked){{m.checked=false;m.focus()}}}})}})();
</script>
</body>
</html>
"""


def press_html():
    """The press mentions kept on the live Publications page, newest addition first."""
    chunk = body_of(PAGES["publications"][0]).split("<h2>Press Mentions</h2>", 1)[1]
    return "<p>" + GITHUB_POST + "</p>" + chunk


def news_page():
    main = (f'<div class="pad head"><h1>In the news</h1></div>'
            f'<div class="pad page">{parts("<h2>Press and media</h2>" + press_html(), cite=True)}</div>')
    return page("In the news: Jermain C. Kaminski", main, "news")


def subpage(key):
    folder, title, img, alt = PAGES[key]
    h = body_of(folder)
    chips = ""
    if key == "publications":  # the profile links sit under the title rather than as a section
        m = re.match(r"<h2>Links</h2>(.*?)(?=<h2>)", h, flags=re.S)
        links = re.findall(r'<a class="chip" href="([^"]*)"[^>]*>(.*?)</a>', m.group(1))  # one quiet line of profiles
        chips = ('<p class="prof-line"><span class="lbl">Profiles</span>'
                 + "".join(f'<a href="{u}">{n}{ARROW}</a>' for u, n in links) + "</p>")
        h = h[m.end():]
        h = h.replace("<h2>Working Papers</h2>", "<h2>Working Papers</h2><p>" + SILICON + "</p>", 1)
        h = h.split("<h2>Press Mentions</h2>", 1)[0]  # press has its own page, see news_page
    if key == "research":  # the pillars lead the research page
        h = f"<h2>Three pillars of current research</h2>{pillars_html()}" + h
    band = f'<div class="pad"><figure class="band"><img src="media/{img}" alt="{alt}"><figcaption class="note">{NOTES[key]}</figcaption></figure></div>' if img else ""
    if key == "about":  # the full-length photograph, shown whole beside the page text
        main = (f'<div class="pad head"><h1>{title}</h1></div><div class="pad page standing">'
                f'<figure><img src="media/Jermain-standing.jpg" width="3170" height="3560" alt="Jermain Kaminski standing full length in a bright university corridor, in a blue suit and pink bow tie, hands in pockets, beside a cobalt blue alcove"><figcaption class="note">{NOTES["about"]}</figcaption></figure>'
                f'<div class="body">{tidy(h)}</div></div>')
        return page("About: Jermain C. Kaminski", main, key)
    main = (f'<div class="pad head"><h1>{title}</h1>{chips}</div>{band}'
            f'<div class="pad page">{parts(h, cite=key == "publications")}</div>')
    plain = html.unescape(title)
    return page(f"{plain}: Jermain C. Kaminski", main, key)


def home_parts():
    rest = (HERE / "home_sections.html").read_text(encoding="utf8")
    rest = re.sub(r'https://jermainkaminski\.com/([a-z-]+)/', lambda m: local_href(m.group(0)), rest)
    rest = rest.replace('<section class="sec pad" id="work">',
                        '<section class="sec pad" id="pillars"><h2 class="sec-h">Three pillars of current research</h2>'
                        + pillars_html() + '</section>\n<section class="sec pad" id="work" style="padding-top:0">', 1)
    rest = rest.replace('class="seeall"', 'class="more"')
    rest = rest.replace(' style="margin-top:12px"', "")
    rest = rest.replace('<a href="research.html" style="text-underline-offset:4px">Research, grants and service</a>',
                        '<a class="more" style="margin:0" href="about.html">More about me</a>')
    rest = rest.replace('<a href="essay.html" style="text-underline-offset:4px">Read the essay</a>',
                        '<a class="more" style="margin:0" href="essay.html">Read the essay</a>')
    rest = rest.replace('</dl>\n      </div>\n    </div>\n  </section>',
                        '</dl>\n        <a class="more" href="teaching.html">Courses and teaching statement</a>\n      </div>\n    </div>\n  </section>')
    hero = """<div class="pad">
      <div class="stage" id="top">
        <div class="say">
          <h1>Causal inference and machine learning for <em>the decisions founders actually make.</em></h1>
          <dl class="facts">
            <div><dt>Based</dt><dd>Maastricht University, School of Business and Economics</dd></div>
            <div><dt>Focus</dt><dd>Entrepreneurship, strategy, causal machine learning</dd></div>
            <div><dt>Co-founded</dt><dd><a href="https://causalscience.org">Causal Data Science Meeting</a>, <a href="https://moviegalaxies.gf52t95h4b.workers.dev">MovieGalaxies</a></dd></div>
            <div><dt>Advisor</dt><dd><a href="https://texterous.com">Texterous</a>, on AI that people actually use</dd></div>
          </dl>
        </div>
        <figure class="portrait"><img src="media/Jermain-Kaminski-1-md-Kopie-3.jpg" width="2000" height="1333" fetchpriority="high" alt="Jermain Kaminski smiling in a bright university corridor, in a blue blazer and pink bow tie"><figcaption class="note">""" + NOTES["home"] + """</figcaption></figure>
      </div>
    </div>
"""
    return hero, rest


FONTS = "family=Geist:wght@300;400;500&family=Newsreader:ital,opsz,wght@0,6..72,200..800;1,6..72,200..800"
