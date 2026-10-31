#!/usr/bin/env python3
"""Adds the interpretability post (first published on LinkedIn) to the Publii site as post 26."""
import json
import sqlite3
import time
from pathlib import Path

SITE = Path.home() / "Documents/Publii/sites/jermain-c-kaminski/input"
NOW = int(time.time() * 1000)
LINKEDIN = "https://www.linkedin.com/in/jermainkaminski/recent-activity/all/"

TEXT = """<p>In machine learning, the honest answer to “why did the model do that?” remains “we can’t really tell”. That may be changing, and below is an interesting read. I think it’s intriguing for anyone who works on causality.</p>
<p>In management research, but also in industrial practice, I often see explainability tools treated as if they answered the “why?”. Shapley values, LIME, permutation importance, partial dependence plots, attention maps. All of them point at the inputs that mattered for an output, but none of them tell you what happens if you intervene: on a part inside the model, or on the world the data came from.</p>
<p>While explainability changes the inputs (the variables) and watches the output, interpretability changes a part inside the model (the function itself) and watches the output. The trouble with neural networks is that a concept like “car” has been spread across many neurons, and each neuron served many concepts, so switching one off told you little.</p>
<p><a href="https://already-clean.goodfire.com/" target="_blank" rel="noopener noreferrer">A new essay</a>, <a href="https://www.nytimes.com/2026/10/27/science/ai-problem-interpretability.html" target="_blank" rel="noopener noreferrer">covered in the New York Times this week</a>, argues it might be less messy than we thought. The results are preliminary and contested, but in large models, most neurons seem to have one main job. If the claims hold even in part, switching a neuron off then becomes an intervention on something you can name. For causal inference that’s interesting, because normally we observe data and have to guess at the structure behind it (causal discovery).</p>
<p>Now, does theory still matter, then? Likely more than before. Machines can propose hypotheses and test them faster than we can read them. What they can’t tell us is which of the many theories that fit the data is the one we need, because that depends on what we want to test. It’s new territory, again moving the bottleneck from computing answers to choosing the right questions, and nobody has a benchmark for that yet.</p>
<p><em>First published <a href="%s" target="_blank" rel="noopener noreferrer">on LinkedIn</a>.</em></p>
""" % LINKEDIN

db = sqlite3.connect(SITE / "db.sqlite")
c = db.cursor()
c.execute("insert into posts (id, title, authors, slug, text, featured_image_id, created_at, modified_at, status, template) values (?,?,?,?,?,?,?,?,?,?)",
          (26, "Why did the model do that?", "1", "why-did-the-model-do-that", TEXT, 0, NOW, NOW, "published", ""))
c.execute("insert into posts_additional_data (post_id, key, value) values (26, '_core', ?)",
          (json.dumps({"metaTitle": "", "metaDesc": "Explainability tools point at the inputs that mattered; interpretability intervenes inside the model. If most neurons have one job, switching one off becomes an intervention you can name.",
                       "metaRobots": "index, follow", "canonicalUrl": "", "editor": "tinymce"}),))
db.commit()
db.close()

cfg_path = SITE / "config/theme.wall.config.json"
cfg = json.loads(cfg_path.read_text())
cfg["customConfig"]["writingPosts"] = "26,9,19"
cfg_path.write_text(json.dumps(cfg, indent=4))
print("post 26 added")
