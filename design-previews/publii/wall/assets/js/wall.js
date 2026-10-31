/* The Wall theme. Everything here is progressive: the pages read fine without it. In this order:
   1. email links assembled from parts, so the addresses are not in the source
   2. the phone sheet menu closes on Escape and on same-page links
   3. the footer's "last updated" date, from the page's own modification time
   4. the running head on articles, shown once the title has scrolled away
   5. page bodies: each h2 and what follows it becomes a two-column section; Publications
      rows become citations with a BibTeX toggle; grants, courses and quotes get their shapes
   6. straight quotes curl */
(function () {
  "use strict";

  /* 1 */
  function mailLinks() {
    document.querySelectorAll("a.mailto").forEach(function (a) {
      var e = a.dataset.u + "@" + a.dataset.d;
      a.href = "mailto:" + e;
      if (a.querySelector(".at")) a.textContent = e;
    });
  }

  /* 2 */
  function phoneMenu() {
    var m = document.getElementById("menu");
    if (!m) return;
    m.checked = false;
    window.addEventListener("pageshow", function () { m.checked = false; });
    document.querySelectorAll("nav.top ul a").forEach(function (a) { a.addEventListener("click", function () { m.checked = false; }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && m.checked) { m.checked = false; m.focus(); } });
  }

  /* 3 */
  function updatedDate() {
    var upd = document.querySelector("[data-updated]");
    if (!upd) return;
    var d = new Date(document.lastModified);
    if (!isNaN(d)) upd.textContent = "Last updated " + d.getDate() + " " + d.toLocaleString("en-GB", { month: "long" }) + " " + d.getFullYear();
  }

  /* 4 */
  function runningHead() {
    var h1 = document.querySelector(".post-head h1");
    if (!h1 || !("IntersectionObserver" in window)) return;
    new IntersectionObserver(function (es) { document.body.classList.toggle("past", !es[0].isIntersecting && es[0].boundingClientRect.top < 0); }).observe(h1);
  }

  /* 5 */
  function tidy(h) {
    h = h.replace(/<(p|div|h[1-6])\s[^>]*>/g, "<$1>").replace(/<\/?div>/g, "").replace(/<h[1-6]>\s*<\/h[1-6]>/g, "");
    h = h.replace(/<br\s*\/?>/g, " ").replace(/;\s*<\/a>/g, "</a>; ").replace(/\s+/g, " ").replace(/\s+<\/a>/g, "</a> ");
    h = h.replace(/(<\/a>|<\/em>)\s+([,.;:!?])/g, "$1$2").replace(/\s+([,;:!?])(?=\s)/g, "$1");
    return h.replace(/<p> /g, "<p>").replace(/ <\/p>/g, "</p>");
  }

  function citeRow(inner) {
    inner = inner.trim().replace(/;$/, "").trim();
    var text = inner.replace(/<[^>]+>/g, " ");
    var y = text.match(/\b(?:19|20)\d{2}\b/);
    var au = null, ti = null, ve = null, mm;
    inner = inner.replace(/<em>(<a [\s\S]*?<\/a>)([\s\S]*?)<\/em>/, "$1$2");
    var links = (inner.match(/<a /g) || []).length;
    var linked = inner.match(/^([\s\S]*?)(<a [^>]*>(?!\()[^<]*<\/a>)\s*([.,?!:]*)\s*([\s\S]*)$/);
    if (links === 1 && linked) {
      au = linked[1];
      ti = linked[2] + (".?!".indexOf(linked[2].charAt(linked[2].length - 5)) >= 0 ? "" : linked[3]);
      ve = linked[4];
    } else if (links === 0) {
      mm = inner.match(/^([\s\S]*?\(\d{4}[^)]*\)\.)\s*([\s\S]*?\.)\s*([\s\S]*)$/) || inner.match(/^([\s\S]*?),\s*(“[\s\S]*?”)\s*([\s\S]*)$/);
      if (mm) { au = mm[1]; ti = mm[2]; ve = mm[3]; }
    }
    if (ti) {
      ti = ti.trim().replace(/[\s.,:]+$/, "").replace(/(<\/a>)[.,:]+$/, "$1").replace(/,”/g, "”");
    }
    if (au) au = au.replace(/\s+-\s*$/, "").replace(/\s*\(\d{4}[^)]*\)\.?\s*$/, "");
    if (ve) {
      ve = ve.replace(/<em>((?:Preparing|Under Review|Resubmit|Available at)[^<]*)<\/em>/g, "$1");
      if (/^\s*\(\d{4}\)\.?\s*$/.test(ve)) ve = null;
    }
    if (ti === null && (mm = inner.match(/^(Vlees Magazine) \([\s\S]*?\)\.\s*([\s\S]*?)\s*<a [^>]*>/))) {
      var link = inner.match(/<a [^>]*>[\s\S]*?<\/a>/)[0];
      au = mm[1]; ti = mm[2] + " " + link;
    }
    var content;
    if (ti === null) {
      content = "<p>" + inner + "</p>";
    } else {
      content = "<p>" + [["au", au], ["ti", ti], ["ve", ve]].filter(function (p) { return p[1] && p[1].trim(); })
        .map(function (p) { return '<span class="' + p[0] + '">' + p[1].trim() + "</span>"; }).join("") + "</p>";
    }
    if (ti !== null) {
      var bib = bibtex(au, ti, ve, y ? y[0] : "", inner);
      content = content.replace("</p>", ' <a class="bib" href="#" data-bib>BibTeX</a></p><pre hidden>' + bib.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</pre>");
    }
    return '<div class="cite"><span class="yr">' + (y ? y[0] : "") + "</span>" + content + "</div>";
  }

  function strip(h) { var d = document.createElement("div"); d.innerHTML = h || ""; return d.textContent.trim(); }

  function bibtex(au, ti, ve, year, inner) {  // an approximate entry: enough to cite, easy to correct
    var authors = strip(au).replace(/,+$/, "").replace(/,?\s*(?:&|and)\s+/g, " and ").replace(/(\w\.),\s+(?=[A-Z][a-z])/g, "$1 and ");
    var title = strip(ti).replace(/^[“”"]|[“”"]$/g, "");
    var journal = strip((ve || "").match(/<em>[\s\S]*?<\/em>/g) ? (ve.match(/<em>([\s\S]*?)<\/em>/g) || []).map(function (e) { return e.replace(/<\/?em>/g, ""); }).join(" ") : "");
    var url = inner.match(/href="([^"]+)"/);
    var firstAuthor = authors ? authors.split(" and ")[0] : "Kaminski";
    var surname = (firstAuthor.indexOf(",") >= 0 ? firstAuthor.split(",")[0] : firstAuthor.split(/\s+/).pop()).toLowerCase().replace(/[^a-z]/g, "") || "kaminski";
    var key = surname + (year || "nd") + (title ? title.split(/\s+/)[0].toLowerCase().replace(/[^a-z]/g, "") : "");
    var fields = [["author", authors], ["title", title], ["journal", journal], ["year", year], ["url", url ? url[1] : ""], ["note", journal ? "" : strip(ve).replace(/\.$/, "")]];
    return "@" + (journal ? "article" : "misc") + "{" + key + ",\n" + fields.filter(function (f) { return f[1]; }).map(function (f) { return "  " + f[0] + " = {" + f[1] + "}"; }).join(",\n") + "\n}";
  }

  function citations(chunk) {
    return chunk.replace(/<p>([\s\S]*?)<\/p>/g, function (_, inner) {
      if (inner.indexOf("Moviegalaxies (Selection):") === 0) {
        var items = inner.split(":").slice(1).join(":").split(/;\s*|(?<=<\/a>\.)\s+(?=<a )/);
        return "<h3>Moviegalaxies (Selection)</h3>" + items.filter(function (i) { return i.trim(); }).map(citeRow).join("");
      }
      return citeRow(inner);
    });
  }

  function grants(chunk) {  // own grants first, then those where I am collaborator or project partner
    var own = "", others = "";
    chunk.replace(/<li>(\d{4})\s+([\s\S]*?)<\/li>/g, function (_, year, rest) {
      var amount = rest.match(/\s*\(([\d,]+ [A-Z]{3})\)/);
      var what = amount ? rest.replace(amount[0], "") : rest;
      var role = what.match(/^\s*<em>((?:Collaborator|Project-Partner)[^<]*)<\/em>[:.]?\s*/);
      if (role) what = what.slice(role[0].length) + '<span class="role">' + role[1].replace("Project-Partner", "Project partner").replace("/Co-Supervisor", " and co-supervisor") + "</span>";
      var row = '<li class="grant"><span class="yr">' + year + "</span><span>" + what.trim() + '</span><span class="amt">' + (amount ? amount[1] : "") + "</span></li>";
      if (role) others += row; else own += row;
    });
    if (!own && !others) return chunk;
    return "<ul>" + own + "</ul>" + (others ? "<h3>As collaborator or project partner</h3><ul>" + others + "</ul>" : "");
  }

  function awards(chunk) {
    var mm = chunk.match(/<p>([\s\S]*?)<\/p>/);
    if (!mm) return chunk;
    var text = mm[1].replace(/[. ]+$/, "").replace("London, UK Young", "London, UK; Young");
    return "<ul>" + text.split(/(?<!&amp);/).map(function (a) { return "<li>" + a.trim() + "</li>"; }).join("") + "</ul>";
  }

  function courses(chunk) {
    return chunk.replace(/<li>([\s\S]*?)<\/li>/g, function (_, inner) {
      inner = inner.replace(/<\/?span[^>]*>/g, "").trim();  // the editor leaves styled spans around some ratings
      var rate = inner.match(/\s*\(\s*([\d.]+)\s*\/\s*([\d.]+)\s*\)\s*$/);
      if (!rate) return '<li class="course"><span>' + inner + "</span></li>";
      return '<li class="course"><span>' + inner.slice(0, rate.index) + '</span><span class="rate">' + rate[1] + "<small> / " + rate[2] + "</small></span></li>";
    });
  }

  function quotes(chunk) {
    return chunk.replace(/<blockquote><p>([\s\S]*?)\s*[–—]\s*([^–—]*?)<\/p><\/blockquote>/g, "<blockquote><p>$1</p><footer>$2</footer></blockquote>");
  }

  function profileSentence(chunk) {  // the profile links as one sentence in the lead type, the links inside the prose
    var by = {};
    chunk.replace(/<a [^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/g, function (_, u, n) { by[n.replace(/<[^>]+>/g, "").trim()] = u; });
    var g = by["Google Scholar"], m = by["Semantic Scholar"], sg = by["Sage Policy Impact"], r = by["Rankless"];
    var a = function (u, t) { return '<a href="' + u + '">' + t + "</a>"; };
    if (g && m && sg && r) return '<p class="head-lead">My papers are indexed on ' + a(g, "Google Scholar") + " and " + a(m, "Semantic Scholar") + ", and their use in policy is tracked by " + a(sg, "Sage") + " and " + a(r, "Rankless") + ".</p>";
    var all = Object.keys(by).map(function (k) { return a(by[k], k); });
    return all.length ? '<p class="head-lead">Find my work on ' + all.join(", ") + ".</p>" : "";
  }

  var SHAPE = { "Grants and Collaborations": grants, "Awards and Honors (Selection)": awards, "Courses": courses, "Teaching Statement": quotes };

  function shapeBodies() {
    document.querySelectorAll(".raw").forEach(function (raw) {
      var h = tidy(raw.innerHTML);
      var cite = raw.hasAttribute("data-cite");
      var bits = h.split(/<h[2-4]>([\s\S]*?)<\/h[2-4]>/);
      var out = [];
      var lead = bits[0].trim();
      var profiles = "";
      if (lead) out.push('<section class="part lead"><div></div><div class="body">' + lead + "</div></section>");
      for (var i = 1; i < bits.length; i += 2) {
        var title = bits[i].replace(/<[^>]+>/g, "").trim();
        var chunk = bits[i + 1] || "";
        if (cite && title === "Links") { profiles = profileSentence(chunk); continue; }  // goes under the page title
        chunk = cite ? citations(chunk) : (SHAPE[title] ? SHAPE[title](chunk) : chunk);
        out.push('<section class="part"><h2>' + title + '</h2><div class="body">' + chunk.trim() + "</div></section>");
      }
      var wrap = document.createElement("div");
      wrap.className = "parts";
      wrap.innerHTML = out.join("");
      raw.replaceWith(wrap);
      if (profiles) {
        var head = document.querySelector(".head");
        if (head) head.insertAdjacentHTML("beforeend", profiles);
      }
    });
  }

  function bibToggle() {  // one listener, so it also serves the citations built above
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a[data-bib]");
      if (!a) return;
      e.preventDefault();
      var p = a.closest(".cite").querySelector("pre");
      p.hidden = !p.hidden;
      a.textContent = p.hidden ? "BibTeX" : "Hide";
    });
  }

  /* 6 */
  function curly(text) {
    text = text.replace(/(?<=\w)'/g, "’").replace(/(^|[\s(\[])'/g, "$1‘").replace(/'/g, "’");
    text = text.replace(/(^|[\s(\[])"/g, "$1“");
    return text.replace(/"/g, "”");
  }

  function curlAll(root) {
    if (!root) return;
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    var n;
    while ((n = walker.nextNode())) {
      if (n.parentNode.closest("script,style,code,pre")) continue;
      if (/['"]/.test(n.nodeValue)) n.nodeValue = curly(n.nodeValue);
    }
  }

  mailLinks();
  phoneMenu();
  updatedDate();
  runningHead();
  shapeBodies();
  bibToggle();
  curlAll(document.getElementById("main"));
})();
