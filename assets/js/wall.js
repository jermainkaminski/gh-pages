/* The Wall theme. Everything here is progressive: the pages read fine without it.
   Page bodies come out of the Publii editor as plain headings and paragraphs; shapeBodies()
   turns them into two-column sections and gives Publications, grants, courses and quotes their form. */
(() => {
  "use strict";

  const tag = (name, cls, html) => `<${name} class="${cls}">${html}</${name}>`;
  const stripTags = (html) => html.replace(/<[^>]+>/g, "");
  const plainText = (html) => {
    const div = document.createElement("div");
    div.innerHTML = html || "";
    return div.textContent.trim();
  };

  /* The addresses are assembled here, so they are not in the source. */
  function mailLinks() {
    document.querySelectorAll("a.mailto").forEach((a) => {
      const address = `${a.dataset.u}@${a.dataset.d}`;
      a.href = `mailto:${address}`;
      if (a.querySelector(".at")) a.textContent = address;
    });
  }

  /* The full-screen menu is a checkbox; this closes it on Escape, on links and on coming back. */
  function menuSheet() {
    const toggle = document.getElementById("menu");
    if (!toggle) return;
    const close = () => { toggle.checked = false; };
    close();
    window.addEventListener("pageshow", close);
    document.querySelectorAll("nav.top ul a").forEach((a) => a.addEventListener("click", close));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && toggle.checked) { close(); toggle.focus(); }
    });
  }

  function updatedDate() {
    const el = document.querySelector("[data-updated]");
    const date = new Date(document.lastModified);
    if (!el || isNaN(date)) return;
    el.textContent = `Last updated ${date.getDate()} ${date.toLocaleString("en-GB", { month: "long" })} ${date.getFullYear()}`;
  }

  /* On articles, the running head appears once the title has scrolled away. */
  function runningHead() {
    const title = document.querySelector(".post-head h1");
    if (!title) return;
    new IntersectionObserver(([e]) => {
      document.body.classList.toggle("past", !e.isIntersecting && e.boundingClientRect.top < 0);
    }).observe(title);
  }

  /* Removes what the editor leaves behind: attributes, wrappers, empty headings, stray spaces. */
  function tidy(html) {
    return html
      .replace(/<(p|div|h[1-6])\s[^>]*>/g, "<$1>").replace(/<\/?div>/g, "").replace(/<h[1-6]>\s*<\/h[1-6]>/g, "")
      .replace(/<br\s*\/?>/g, " ").replace(/;\s*<\/a>/g, "</a>; ").replace(/\s+/g, " ").replace(/\s+<\/a>/g, "</a> ")
      .replace(/(<\/a>|<\/em>)\s+([,.;:!?])/g, "$1$2").replace(/\s+([,;:!?])(?=\s)/g, "$1")
      .replace(/<p> /g, "<p>").replace(/ <\/p>/g, "</p>");
  }

  /* Splits one reference into authors, title and venue; the title stays null when it cannot tell. */
  function citationParts(html) {
    let authors = null, title = null, venue = null;
    const linkCount = (html.match(/<a /g) || []).length;
    const linked = html.match(/^([\s\S]*?)(<a [^>]*>(?!\()[^<]*<\/a>)\s*([.,?!:]*)\s*([\s\S]*)$/);
    if (linkCount === 1 && linked) {
      const endsSentence = ".?!".includes(linked[2].charAt(linked[2].length - 5));  // the character before </a>
      [authors, title, venue] = [linked[1], linked[2] + (endsSentence ? "" : linked[3]), linked[4]];
    } else if (linkCount === 0) {
      const m = html.match(/^([\s\S]*?\(\d{4}[^)]*\)\.)\s*([\s\S]*?\.)\s*([\s\S]*)$/) || html.match(/^([\s\S]*?),\s*(“[\s\S]*?”)\s*([\s\S]*)$/);
      if (m) [authors, title, venue] = m.slice(1);
    }
    if (title) title = title.trim().replace(/[\s.,:]+$/, "").replace(/(<\/a>)[.,:]+$/, "$1").replace(/,”/g, "”");
    if (authors) authors = authors.replace(/\s+-\s*$/, "").replace(/\s*\(\d{4}[^)]*\)\.?\s*$/, "");
    if (venue) {
      venue = venue.replace(/<em>((?:Preparing|Under Review|Resubmit|Available at)[^<]*)<\/em>/g, "$1");
      if (/^\s*\(\d{4}\)\.?\s*$/.test(venue)) venue = null;
    }
    const vlees = title === null && html.match(/^(Vlees Magazine) \([\s\S]*?\)\.\s*([\s\S]*?)\s*<a [^>]*>/);
    if (vlees) [authors, title] = [vlees[1], `${vlees[2]} ${html.match(/<a [^>]*>[\s\S]*?<\/a>/)[0]}`];
    return { authors, title, venue };
  }

  /* Curated records from citations.js; a row without one simply has no BibTeX link. */
  function citationRecord(...candidates) {
    const records = window.WALL_CITATIONS || {};
    const key = (html) => plainText(html).toLowerCase().replace(/[^a-z0-9]/g, "").slice(0, 48);
    return candidates.map((html) => records[key(html)]).find(Boolean);
  }

  function citeRow(reference) {
    const trimmed = reference.trim().replace(/;$/, "").trim();
    const found = trimmed.replace(/<[^>]+>/g, " ").match(/\b(?:19|20)\d{2}\b/);
    const year = found ? found[0] : "";
    const html = trimmed.replace(/<em>(<a [\s\S]*?<\/a>)([\s\S]*?)<\/em>/, "$1$2");
    const parts = citationParts(html);
    const record = citationRecord(parts.title, html);
    const toggle = record ? ' <button class="bib" type="button" aria-expanded="false" data-bib>BibTeX</button>' : "";
    const entry = record ? `<pre hidden>${record.replace(/&/g, "&amp;").replace(/</g, "&lt;")}</pre>` : "";
    const spans = [["au", parts.authors], ["ti", parts.title], ["ve", parts.venue]]
      .filter(([, text]) => text && text.trim())
      .map(([cls, text]) => tag("span", cls, text.trim()))
      .join("");
    const content = `<p>${parts.title === null ? html : spans}${toggle}</p>${entry}`;
    return tag("div", "cite", tag("span", "yr", year) + content);
  }

  function citations(chunk) {
    return chunk.replace(/<p>([\s\S]*?)<\/p>/g, (_, inner) => {
      if (!inner.startsWith("Moviegalaxies (Selection):")) return citeRow(inner);
      const items = inner.split(":").slice(1).join(":").split(/;\s*|(?<=<\/a>\.)\s+(?=<a )/);
      return `<h3>Moviegalaxies (Selection)</h3>${items.filter((item) => item.trim()).map(citeRow).join("")}`;
    });
  }

  /* Own grants first, then those as collaborator or project partner. */
  function grants(chunk) {
    let own = "", shared = "";
    for (const [, year, rest] of chunk.matchAll(/<li>(\d{4})\s+([\s\S]*?)<\/li>/g)) {
      const amount = rest.match(/\s*\(([\d,]+ [A-Z]{3})\)/);
      let what = amount ? rest.replace(amount[0], "") : rest;
      const role = what.match(/^\s*<em>((?:Collaborator|Project-Partner)[^<]*)<\/em>[:.]?\s*/);
      if (role) what = what.slice(role[0].length) + tag("span", "role", role[1].replace("Project-Partner", "Project partner").replace("/Co-Supervisor", " and co-supervisor"));
      const row = tag("li", "grant", tag("span", "yr", year) + `<span>${what.trim()}</span>` + tag("span", "amt", amount ? amount[1] : ""));
      if (role) shared += row; else own += row;
    }
    if (!own && !shared) return chunk;
    return `<ul>${own}</ul>${shared ? `<h3>As collaborator or project partner</h3><ul>${shared}</ul>` : ""}`;
  }

  function awards(chunk) {
    const paragraph = chunk.match(/<p>([\s\S]*?)<\/p>/);
    if (!paragraph) return chunk;
    const text = paragraph[1].replace(/[. ]+$/, "").replace("London, UK Young", "London, UK; Young");
    return `<ul>${text.split(/(?<!&amp);/).map((award) => `<li>${award.trim()}</li>`).join("")}</ul>`;
  }

  function courses(chunk) {
    return chunk.replace(/<li>([\s\S]*?)<\/li>/g, (_, item) => {
      const inner = item.replace(/<\/?span[^>]*>/g, "").trim();  // the editor leaves styled spans around some ratings
      const rating = inner.match(/\s*\(\s*([\d.]+)\s*\/\s*([\d.]+)\s*\)\s*$/);
      if (!rating) return tag("li", "course", `<span>${inner}</span>`);
      return tag("li", "course", `<span>${inner.slice(0, rating.index)}</span>` + tag("span", "rate", `${rating[1]}<small> / ${rating[2]}</small>`));
    });
  }

  function quotes(chunk) {
    return chunk.replace(/<blockquote><p>([\s\S]*?)\s*[–—]\s*([^–—]*?)<\/p><\/blockquote>/g, "<blockquote><p>$1</p><footer>$2</footer></blockquote>");
  }

  /* The profile links of Publications, as one sentence under the page title. */
  function profileSentence(chunk) {
    const urls = {};
    for (const [, url, name] of chunk.matchAll(/<a [^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/g)) urls[stripTags(name).trim()] = url;
    const link = (url, text) => `<a href="${url}">${text}</a>`;
    const lead = (text) => `<p class="head-lead">${text}.</p>`;
    const { "Google Scholar": google, "Semantic Scholar": semantic, "Sage Policy Impact": sage, Rankless: rankless } = urls;
    if (google && semantic && sage && rankless) return lead(`My papers are indexed on ${link(google, "Google Scholar")} and ${link(semantic, "Semantic Scholar")}, and their use in policy is tracked by ${link(sage, "Sage Policy Impact")} and ${link(rankless, "Rankless")}`);
    const all = Object.entries(urls).map(([name, url]) => link(url, name));
    return all.length ? lead(`Find my work on ${all.join(", ")}`) : "";
  }

  const SHAPES = { "Grants and Collaborations": grants, "Awards and Honors (Selection)": awards, "Courses": courses, "Teaching Statement": quotes };

  /* Each heading and what follows it becomes a section. */
  function shapeBodies() {
    document.querySelectorAll(".raw").forEach((raw) => {
      const isCitationPage = raw.hasAttribute("data-cite");
      const [before, ...rest] = tidy(raw.innerHTML).split(/<h[2-4]>([\s\S]*?)<\/h[2-4]>/);
      const sections = before.trim() ? [`<section class="part lead"><div></div><div class="body">${before.trim()}</div></section>`] : [];
      let profiles = "";
      for (let i = 0; i < rest.length; i += 2) {
        const title = stripTags(rest[i]).trim();
        const chunk = rest[i + 1] || "";
        if (isCitationPage && title === "Links") { profiles = profileSentence(chunk); continue; }
        const shape = isCitationPage ? citations : SHAPES[title];
        sections.push(`<section class="part"><h2>${title}</h2><div class="body">${(shape ? shape(chunk) : chunk).trim()}</div></section>`);
      }
      const parts = document.createElement("div");
      parts.className = "parts";
      parts.innerHTML = sections.join("");
      raw.replaceWith(parts);
      if (profiles) document.querySelector(".head").insertAdjacentHTML("beforeend", profiles);
    });
  }

  /* One listener, so it also serves the citations built above. */
  function bibToggle() {
    document.addEventListener("click", (e) => {
      const button = e.target.closest("button[data-bib]");
      if (!button) return;
      const entry = button.closest(".cite").querySelector("pre");
      entry.hidden = !entry.hidden;
      button.setAttribute("aria-expanded", String(!entry.hidden));
      button.textContent = entry.hidden ? "BibTeX" : "Hide";
    });
  }

  function curlQuotes(root) {
    const curl = (text) => text
      .replace(/(?<=\w)'/g, "’").replace(/(^|[\s(\[])'/g, "$1‘").replace(/'/g, "’")
      .replace(/(^|[\s(\[])"/g, "$1“").replace(/"/g, "”");
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (/['"]/.test(node.nodeValue) && !node.parentNode.closest("script,style,code,pre")) node.nodeValue = curl(node.nodeValue);
    }
  }

  /* The share button under articles: the phone's own sheet on touch devices, a short menu elsewhere. */
  function shareButton() {
    const box = document.querySelector(".share");
    if (!box) return;
    const canonical = document.querySelector('link[rel="canonical"]');
    const url = canonical ? canonical.href : location.href.split("#")[0];
    const title = document.querySelector("h1").textContent.trim();
    const e = encodeURIComponent;
    const targets = {
      linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${e(url)}`,
      bluesky: `https://bsky.app/intent/compose?text=${e(`${title} ${url}`)}`,
      mail: `mailto:?subject=${e(title)}&body=${e(url)}`
    };
    box.querySelectorAll("a[data-share]").forEach((a) => { a.href = targets[a.dataset.share]; });
    box.hidden = false;
    box.querySelector("summary").addEventListener("click", (ev) => {
      if (!navigator.share || !matchMedia("(pointer:coarse)").matches) return;
      ev.preventDefault();
      navigator.share({ title, url }).catch(() => {});
    });
    const copy = box.querySelector("[data-share=copy]");
    if (navigator.clipboard) {
      copy.addEventListener("click", () => {
        navigator.clipboard.writeText(url).then(() => {
          copy.textContent = "Copied";
          setTimeout(() => { copy.textContent = "Copy link"; box.open = false; }, 1200);
        });
      });
    } else {
      copy.remove();
    }
    document.addEventListener("click", (ev) => { if (!box.contains(ev.target)) box.open = false; });
    document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") box.open = false; });
  }

  mailLinks();
  menuSheet();
  updatedDate();
  runningHead();
  shapeBodies();
  bibToggle();
  curlQuotes(document.getElementById("main"));
  shareButton();
})();
