"""Three 2026 type pairings for the same layout. Each entry: Google Fonts query and the CSS appended to wall.css."""

VARIANTS = {
    "newsreader": {
        "name": "Newsreader",
        "pair": "Newsreader + Geist",
        "note": "The chosen pairing: a light optical-size serif for display, Geist for everything else.",
        "fonts": "family=Geist:wght@300;400;500&family=Newsreader:ital,opsz,wght@0,6..72,200..800;1,6..72,200..800",
        "css": "",
    },
    "instrument": {
        "name": "Instrument",
        "pair": "Instrument Serif + Geist",
        "note": "The sharp editorial look of 2025–26: a condensed high-contrast display serif over Vercel’s neutral sans.",
        "fonts": "family=Instrument+Serif:ital@0;1&family=Geist:wght@300..700",
        "css": """
/* Instrument Serif is condensed and has one weight, so display sizes go up a step and tracking loosens */
:root{--serif:"Instrument Serif",Georgia,serif;--sans:"Geist",system-ui,sans-serif;--display-weight:400;--text:17.5px;--lead-lh:1.2}
h1{font-size:clamp(44px,4.9vw,82px);letter-spacing:-.01em;line-height:1.02}
.sec-h{font-size:clamp(36px,4.1vw,60px);letter-spacing:-.005em}
.card .t,.rw .t{font-size:clamp(34px,3.9vw,60px);letter-spacing:-.005em}
.work .t,.pillar h3{font-size:clamp(29px,3vw,44px);letter-spacing:0}
.about .big,.lead p:first-child,.article>p:first-child,.standing .body>p:first-child{font-size:clamp(30px,3vw,44px);letter-spacing:0}
.body blockquote,.part h2,.article h2,.essay h3,.mail,.rate{letter-spacing:0}
.nums dd{letter-spacing:-.01em}
.pn{font-weight:400;letter-spacing:0}
.close h2{letter-spacing:-.01em}
@media (min-width:1001px){.close h2{font-size:13.6vw}}
@media (max-width:640px){h1{font-size:37px}}
""",
    },
    "fraunces": {
        "name": "Fraunces",
        "pair": "Fraunces + Hanken Grotesk",
        "note": "Warm and a little wonky: a soft old-style serif with optical sizes, set over a humanist grotesk.",
        "fonts": "family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..700,0..100,0..1;1,9..144,300..700,0..100,0..1&family=Hanken+Grotesk:ital,wght@0,300..600;1,300..600",
        "css": """
/* Fraunces sets wide, so display sizes come down a step; the soft and wonky axes are on for display only */
:root{--serif:"Fraunces",Georgia,serif;--sans:"Hanken Grotesk",system-ui,sans-serif;--display-weight:300}
h1,.sec-h,.close h2,.card .t,.rw .t,.work .t,.pillar h3,.essay h3,.part h2,.article h2,.about .big,.lead p:first-child,.article>p:first-child,.standing .body>p:first-child,.body blockquote,.mail,.nums dd,.rate,.pn{font-optical-sizing:auto;font-variation-settings:"SOFT" 70,"WONK" 1}
h1{font-size:clamp(37px,4vw,66px);letter-spacing:-.03em}
.sec-h{font-size:clamp(31px,3.4vw,50px);letter-spacing:-.025em}
.card .t,.rw .t{font-size:clamp(30px,3.3vw,50px);letter-spacing:-.025em}
.work .t,.pillar h3{font-size:clamp(25px,2.6vw,36px);letter-spacing:-.02em}
.about .big,.lead p:first-child,.article>p:first-child,.standing .body>p:first-child{font-size:clamp(26px,2.6vw,36px);letter-spacing:-.02em}
.close h2{letter-spacing:-.04em}
@media (min-width:1001px){.close h2{font-size:14.2vw}}
@media (max-width:640px){h1{font-size:32px}}
""",
    },
    "host": {
        "name": "Host",
        "pair": "Host Grotesk + Geist Mono",
        "note": "No serif at all: a light Swiss grotesk for everything, with a monospace for dates, labels and years.",
        "fonts": "family=Host+Grotesk:ital,wght@0,300..800;1,300..800&family=Geist+Mono:wght@400;500",
        "css": """
/* One grotesk for display and text, a monospace for the small labels */
:root{--serif:"Host Grotesk",system-ui,sans-serif;--sans:"Host Grotesk",system-ui,sans-serif;--mono:"Geist Mono",ui-monospace,SFMono-Regular,monospace;--display-weight:300;--text:17.5px;--lead-lh:1.22}
h1{font-size:clamp(38px,4.2vw,70px);letter-spacing:-.035em;line-height:1.02}
.sec-h,.card .t,.rw .t,.essay h3{letter-spacing:-.03em}
.work .t,.pillar h3,.part h2,.article h2,.about .big,.lead p:first-child,.article>p:first-child,.standing .body>p:first-child,.body blockquote{letter-spacing:-.025em}
.mail,.rate,.nums dd{letter-spacing:-.03em}
.pn{letter-spacing:-.04em}
.close h2{letter-spacing:-.045em}
.lbl,.facts dt,.d,.yr,.work .y,.sched span:last-child,.colophon,.post-head .d,.body blockquote footer{font-family:var(--mono)}
.lbl,.facts dt{font-size:12.5px;font-weight:400;letter-spacing:.05em}
.d,.yr,.work .y,.sched span:last-child{font-size:14.5px;letter-spacing:0}
.colophon{font-size:14px}
@media (min-width:1001px){.close h2{font-size:10.7vw}}
@media (max-width:640px){h1{font-size:33px}}
""",
    },
}
