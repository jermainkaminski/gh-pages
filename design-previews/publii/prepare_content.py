#!/usr/bin/env python3
"""Prepares the Publii site for the Wall theme: About becomes a page, Writing and News pages are created,
Publications loses its press section to News and gains the silicon paper, typos are corrected, featured
images get their notes, and the menu is rewritten. Run once; a backup of the database sits beside the site."""
import json
import shutil
import sqlite3
import time
from pathlib import Path

SITE = Path.home() / "Documents/Publii/sites/jermain-c-kaminski/input"
DB = SITE / "db.sqlite"
NOW = int(time.time() * 1000)

TYPOS = {
    "Entrepreneuership": "Entrepreneurship", "bandwith": "bandwidth", "could together on": "could work together on",
    "sparrings partner": "sparring partner", "I enjoy to trigger": "I enjoy triggering", "in a the famous": "in the famous",
    "powerful and tools": "powerful tools", "18-39 year old who": "18–39-year-olds who", "Awwards": "Awwwards",
}
SILICON = "<p>Kaminski, J. (2026). Silicon sampling for product feedback in entrepreneurship. Working paper. The title was changed for peer review.</p>\n"
GITHUB = ('<p>GitHub Blog (2026). <a href="https://github.blog/news-insights/policy-news-and-insights/how-researchers-are-using-github-innovation-graph-data-to-reveal-the-digital-complexity-of-nations/" target="_blank" rel="noopener noreferrer">'
          'How researchers are using GitHub Innovation Graph data to reveal the “digital complexity” of nations</a>.</p>\n')
NOTES = {  # image id: (alt, note shown under the picture on phones)
    367: ("Numbered sailing dinghies on a dock on the Charles River, with the Boston skyline across the water", "<b>Charles River</b>MIT, Cambridge, Massachusetts"),
    394: ("Jermain Kaminski teaching a seated MBA class in a long timber-floored room", "<b>MBA class</b>Maastricht University"),
    306: ("A corridor at Tapijn with yellow, orange, red and blue study alcoves in timber frames", "<b>Tapijn campus</b>Maastricht University"),
    379: ("Portrait of Jermain Kaminski", "<b>Jermain Kaminski</b>Maastricht University"),
    404: ("Park bench scene from the 1997 film Good Will Hunting", "<b>Good Will Hunting</b>1997, the park bench scene"),
}


def main():
    db = sqlite3.connect(DB)
    c = db.cursor()

    # About: the featured "Welcome!" post becomes a page, with the full-length photograph as its picture
    c.execute("update posts set status='published,is-page', title='About', modified_at=? where id=12", (NOW,))
    shutil.copy(SITE.parent.parent.parent.parent / "GitHub/gh-pages/design-previews/wall/media/Jermain-standing.jpg", SITE / "media/posts/12/Jermain-standing.jpg")
    c.execute("insert into posts_images (post_id, url, title, caption, additional_data) values (12, 'Jermain-standing.jpg', '', ?, ?)",
              ("<b>School of Business and Economics</b>Maastricht University",
               json.dumps({"alt": "Jermain Kaminski standing full length in a bright university corridor, in a blue suit and pink bow tie, hands in pockets, beside a cobalt blue alcove",
                           "caption": "<b>School of Business and Economics</b>Maastricht University", "credits": ""})))
    c.execute("update posts set featured_image_id=? where id=12", (c.lastrowid,))

    # Posts: the essay is no longer hidden, the meeting no longer "featured"; the meeting's picture is the Tapijn hallway
    c.execute("update posts set status='published' where id in (9, 19)")
    core = json.loads(c.execute("select value from posts_additional_data where post_id=19 and key='_core'").fetchone()[0])
    core["metaRobots"] = "index, follow"
    c.execute("update posts_additional_data set value=? where post_id=19 and key='_core'", (json.dumps(core),))
    shutil.copy(SITE / "media/posts/16/UM-Tapijn-202011-022.jpg", SITE / "media/posts/9/UM-Tapijn-202011-022.jpg")
    c.execute("insert into posts_images (post_id, url, title, caption, additional_data) values (9, 'UM-Tapijn-202011-022.jpg', '', ?, ?)",
              ("<b>Tapijn campus</b>Maastricht University",
               json.dumps({"alt": "A corridor at Tapijn with yellow, orange, red and blue study alcoves in timber frames",
                           "caption": "<b>Tapijn campus</b>Maastricht University", "credits": ""})))
    c.execute("update posts set featured_image_id=? where id=9", (c.lastrowid,))

    # Notes under the other pictures
    for image_id, (alt, note) in NOTES.items():
        c.execute("update posts_images set caption=?, additional_data=? where id=?",
                  (note, json.dumps({"alt": alt, "caption": note, "credits": ""}), image_id))

    # Publications: press moves to its own page, the silicon paper joins the working papers
    text = c.execute("select text from posts where id=15").fetchone()[0]
    i = text.index('<h4 id="mcetoc_1j47ouonh1jh">Press Mentions</h4>')
    press = text[i:].split("</h4>", 1)[1]
    pubs = text[:i].replace("<h4>Working Papers</h4>\n", "<h4>Working Papers</h4>\n" + SILICON, 1)
    c.execute("update posts set text=?, modified_at=? where id=15", (pubs, NOW))
    news = "<h4>Press and media</h4>\n" + GITHUB + press

    # Typos
    for pid in (11, 15, 16, 18, 19):
        t = c.execute("select text from posts where id=?", (pid,)).fetchone()[0]
        for wrong, right in TYPOS.items():
            t = t.replace(wrong, right)
        c.execute("update posts set text=? where id=?", (t, pid))

    # New pages: Writing (id 24, template "writing") and In the news (id 25)
    for pid, title, slug, template, body in ((24, "Writing", "writing", "writing", ""), (25, "In the news", "news", "", news)):
        c.execute("insert into posts (id, title, authors, slug, text, featured_image_id, created_at, modified_at, status, template) values (?,?,?,?,?,?,?,?,?,?)",
                  (pid, title, "1", slug, body, 0, NOW, NOW, "published,is-page", template))
        c.execute("insert into posts_additional_data (post_id, key, value) values (?, '_core', ?)",
                  (pid, json.dumps({"metaTitle": "", "metaDesc": "", "metaRobots": "index, follow", "canonicalUrl": "", "editor": "tinymce"})))
    db.commit()
    db.close()

    pages = json.loads((SITE / "config/pages.config.json").read_text())
    for pid in (12, 24, 25):
        if not any(p["id"] == pid for p in pages):
            pages.append({"id": pid, "subpages": []})
    (SITE / "config/pages.config.json").write_text(json.dumps(pages, indent=4))

    items = [("About", 12), ("Research", 11), ("Publications", 15), ("Writing", 24), ("Teaching", 18), ("Students", 16), ("Speaking", 17), ("News", 25)]
    menu = [{"name": "Menu", "position": "mainMenu", "items": [
        {"id": NOW + n, "label": label, "title": "", "type": "page", "target": "_self", "rel": "", "link": pid, "cssClass": "", "isHidden": False, "items": []}
        for n, (label, pid) in enumerate(items)]}]
    (SITE / "config/menu.config.json").write_text(json.dumps(menu, indent=4))

    site = json.loads((SITE / "config/site.config.json").read_text())
    site["advanced"]["metaDescription"] = "Associate Professor of Entrepreneurship and Innovation at Maastricht University. Causal inference and machine learning for the decisions founders make."
    (SITE / "config/site.config.json").write_text(json.dumps(site, indent=4))

    # The portrait for the home page, as a theme option image
    (SITE / "media/website").mkdir(exist_ok=True)
    shutil.copy(SITE / "media/posts/12/Jermain-Kaminski-1-md-Kopie-3.jpg", SITE / "media/website/Jermain-Kaminski-1-md-Kopie-3.jpg")
    theme_cfg = {"config": {"postsPerPage": 20, "tagsPostsPerPage": 20, "authorsPostsPerPage": 20, "excerptLength": 40, "logo": ""},
                 "customConfig": {"heroImage": "media/website/Jermain-Kaminski-1-md-Kopie-3.jpg"}, "postConfig": {}, "pageConfig": {}}
    (SITE / "config/theme.wall.config.json").write_text(json.dumps(theme_cfg, indent=4))
    print("done")


if __name__ == "__main__":
    main()
