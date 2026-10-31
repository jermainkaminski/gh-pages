"""Content shared by the site generator: the research pillars, news and the three ways to work together. Selected work, ratings and events are in home_sections.html."""

PILLARS = [
    ("Causality in Strategic Decision Making",
     "How managers can reason about cause and effect before they act. Causal diagrams make a strategy’s theory of value explicit; causal discovery and structural causal models put it to the test.", [
        ("Mapping theories of value", None, "Preparing for submission"),
        ("Causal discovery in strategic management research", "https://research.cbs.dk/en/publications/causal-discovery-in-strategic-management-research", "DRUID23"),
        ("Structural causal models in strategy", "https://journals.aom.org/doi/abs/10.5465/AMPROC.2023.12543abstract", "AoM Proceedings, 2023"),
    ]),
    ("Machine Learning and Simulacra in Entrepreneurship",
     "What machine learning, and now language models, can tell founders. From multimodal prediction of venture outcomes to silicon samples that simulate customer feedback before a product exists.", [
        ("Silicon sampling for product feedback in entrepreneurship", None, "Working paper, 2026"),
        ("Predicting outcomes in crowdfunding", "https://link.springer.com/content/pdf/10.1007/s11187-019-00218-w.pdf", "Small Business Economics, 2020"),
        ("Learning to frame", None, "Resubmit"),
    ]),
    ("Economic Complexity of Software",
     "Software as a lens on what economies know how to do. With Juhász, Wachs and Hidalgo, measuring the complexity of the code that countries produce and how it relates to their development.", [
        ("The software complexity of nations", "https://doi.org/10.1016/j.respol.2026.105422", "Research Policy, 2026"),
        ("Creative complexity", None, "Under review"),
        ("How researchers are using GitHub Innovation Graph data to reveal the “digital complexity” of nations", "https://github.blog/news-insights/policy-news-and-insights/how-researchers-are-using-github-innovation-graph-data-to-reveal-the-digital-complexity-of-nations/", "GitHub Blog, 2026"),
    ]),
]


def pillars_html():
    def paper(t, u, v):
        name = f'<a href="{u}">{t}</a>' if u else f"<span>{t}</span>"
        return f'<li>{name}<small>{v}</small></li>'
    return '<ol class="pillars">' + "".join(
        f'<li class="pillar"><span class="pn">{i}</span><h3>{t}</h3><p>{d}</p><ul>{"".join(paper(*p) for p in ps)}</ul></li>'
        for i, (t, d, ps) in enumerate(PILLARS, 1)) + "</ol>"


NEWS = [  # the three pieces of coverage shown on the home page; the News page has them all
    ("GitHub Blog", "How researchers are using GitHub Innovation Graph data to reveal the “digital complexity” of nations", "https://github.blog/news-insights/policy-news-and-insights/how-researchers-are-using-github-innovation-graph-data-to-reveal-the-digital-complexity-of-nations/", "2026"),
    ("Poets&amp;Quants", "Best 40 Under 40 MBA Professors", "https://poetsandquants.com/2024/05/18/2024-best-40-under-40-mba-professors-jermain-kaminski-maastricht-university-school-of-business-and-economics/", "2024"),
    ("Einstein Telescope", "The entrepreneurial side of fundamental research", "https://www.einsteintelescope-emr.eu/en/2024/07/04/the-entrepreneurial-side-of-fundamental-research/", "2024"),
]
COLLAB = [  # work with me: three doors, all open
    ("Research collaboration",
     "Causal inference, machine learning, and text and image data on entrepreneurship, strategy and innovation. I’m open to co-authoring, to joint data projects, and to companies and public bodies with a question that deserves a proper answer.",
     "Write to me", "#contact"),
    ("Speaking, workshops and advisory",
     "Keynotes and executive workshops on causal thinking and AI in strategy, and advisory for teams that need to know what their data can and cannot tell them.",
     "Speaking and advisory", "speaking.html"),
    ("Students",
     "I supervise PhD, master’s and honours students at Maastricht, and I’m always glad to hear from prospective PhD candidates with a causal or machine-learning question in mind.",
     "Working with students", "students.html"),
]


def news_html():
    return '<div class="sched news">' + "".join(
        f'<a href="{u}"><span class="o">{o}</span><span class="t">{t}</span><span>{y}</span></a>' for o, t, u, y in NEWS) + "</div>"


def collab_html():
    return '<div class="collab">' + "".join(
        f'<div><h3>{t}</h3><p>{d}</p><a class="more{" mailto" if u == "#contact" else ""}" href="{u}"'
        f'{" data-u=" + chr(34) + "j.kaminski" + chr(34) + " data-d=" + chr(34) + "maastrichtuniversity.nl" + chr(34) if u == "#contact" else ""}>{l}</a></div>'
        for t, d, l, u in COLLAB) + "</div>"
