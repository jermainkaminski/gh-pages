"""Content shared by the site generator: selected work, ratings, events and the research pillars."""

PHOTO = '<img src="media/Jermain-Kaminski-1-md-Kopie-3.jpg" width="2000" height="1333" alt="Jermain Kaminski smiling in a bright university corridor, in a blue blazer and pink bow tie">'

WORK = [
    ("The software complexity of nations", "2026", "Research Policy", "With Juhász, Wachs and Hidalgo. Economic complexity, measured through the software countries produce.", "https://doi.org/10.1016/j.respol.2026.105422"),
    ("Launching for success", "2021", "Journal of Business Venturing", "How psychological distance and mental simulation shape crowdfunding decisions.", "https://www.sciencedirect.com/science/article/abs/pii/S0883902618308619"),
    ("Predicting outcomes in crowdfunding", "2020", "Small Business Economics", "An early multimodal classifier for venture outcomes, reading text, images and language.", "https://link.springer.com/content/pdf/10.1007/s11187-019-00218-w.pdf"),
    ("What 40 years of research reveals", "2018", "Harvard Business Review", "The difference between disruptive and radical innovation, drawn from topic models.", "https://hbr.org/2018/04/what-40-years-of-research-reveals-about-the-difference-between-disruptive-and-radical-innovation"),
    ("Causal Data Science Meeting", "2020–", "Co-founded with Paul Hünermund", "Keynotes have included Guido Imbens, Susan Athey and Judea Pearl.", "https://causalscience.org"),
    ("Moviegalaxies", "2012–", "Harvard Dataverse", "Social networks in movies, open data. An Awwwards Honorable Mention along the way.", "https://doi.org/10.7910/DVN/T4HBA3"),
]
RATINGS = [
    ("Commercializing Science and Technology", "Bachelor", "9.6", "10"),
    ("Technology Entrepreneurship", "Bachelor", "9.4", "10"),
    ("Digital Entrepreneurship", "Master", "9.2", "10"),
    ("Entrepreneurship and New Business Development", "MBA", "5.0", "5"),
]
EVENTS = [
    ("Causal Data Science Meeting 2026", "Online, 4–5 Nov", "https://causalscience.org"),
    ("NATO STO Symposium on Autonomy, Space, and AI", "Brussels", "https://www-eur.cvent.com/c/calendar/8b04e847-c70e-4051-9367-ac0c991ebffe"),
    ("Academy of Management 2026", "Philadelphia", "https://events.aom.org/events/aom-2026/session/qoG_QwylktF7p7uQxZdfj"),
    ("Research in Behavioral Finance Conference", "Amsterdam", "https://www.rbfc.eu"),
    ("Innovation &amp; Entrepreneurship Seminar", "Max Planck", "https://www.ip.mpg.de/en/the-institute/all-events/innovation-entrepreneurship-seminar-how-causal-graphs-can-improve-strategic-decision-making.html"),
    ("Frontiers of Causal Inference and ML", "IMT Lucca", "https://cimlconference.imtlucca.it"),
]
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
     "Write to me", "mailto:j.kaminski@maastrichtuniversity.nl"),
    ("Speaking, workshops and advisory",
     "Keynotes and executive workshops on causal thinking and AI in strategy, and advisory for teams that need to know what their data can and cannot tell them.",
     "Speaking and advisory", "speaking.html"),
    ("Students",
     "I supervise PhD, master’s and honours students at Maastricht, and I’m always glad to hear from prospective PhD candidates with a causal or machine-learning question in mind.",
     "Working with students", "students.html"),
]


def news_html():
    return '<div class="sched news">' + "".join(
        f'<a href="{u}"><span><span class="o">{o}</span>{t}</span><span>{y}</span></a>' for o, t, u, y in NEWS) + "</div>"


def collab_html():
    return '<div class="collab">' + "".join(
        f'<div><h3>{t}</h3><p>{d}</p><a class="more" href="{u}">{l}</a></div>' for t, d, l, u in COLLAB) + "</div>"


BIO ="My work brings together causal inference, language and vision to study how text, images and behaviour change financing and innovation outcomes."
ROLE = "Associate Professor of Entrepreneurship and Innovation, Maastricht University"
