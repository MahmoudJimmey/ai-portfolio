# Story layout for job-specific pages (written by the job bot into pages/<slug>.json with "layout": "story").
# build.py calls page_story(cfg, PROJECTS, EMAIL, LINKEDIN, GITHUB).
import html


def t2(x):
    """HTML-escape visible copy and drop em and en dashes."""
    return html.escape(str(x).replace("—", ", ").replace("–", "-"), quote=True)


def page_story(cfg, PROJECTS, EMAIL, LINKEDIN, GITHUB):
    b = cfg["base"]
    acc = cfg.get("accent", "#1b7a52")
    story = "".join(
        '<li data-r><p class="yr">%s</p><div><h3>%s</h3><p>%s</p><p class="learn"><span>Learned:</span> %s</p></div></li>'
        % (t2(y), t2(h), t2(tx), t2(le))
        for y, h, tx, le in cfg["story"])
    nums = "".join('<div class="num" data-r><b>%s</b><span>%s</span></div>' % (t2(v), t2(l)) for v, l in cfg.get("stats", []))
    cells = []
    for i, (k, why) in enumerate(cfg["cases"][:3]):
        p = PROJECTS[k]
        img = "auto_1" if k == "autologist" else next((x for x in p["slides"] if not x.startswith("video:")), "scoop_1")
        link = ' <a class="tl" href="%s">Source code</a>' % p["link"] if p.get("link") else ""
        cls = ["big", "a", "b"][i]
        cells.append(
            '<article class="pc %s" data-r><div class="im"><img src="%simg/%s.jpg" width="1080" height="1350" alt="%s" loading="lazy"></div>'
            '<div class="tx"><h3>%s</h3><p class="kd">%s</p><p>%s%s</p><p class="why">%s</p><p class="tools">Built with %s</p></div></article>'
            % (cls, b, img, t2(p["alt"]), t2(p["name"]), t2(p["kind"]), t2(p["text"]), link, t2(why), t2(p["tools"])))
    fit = []
    for r, e, tag in cfg["fit"]:
        gap = str(tag).lower().startswith("partial")
        fit.append('<div class="fc%s" data-r><span class="tag">%s</span><h3>%s</h3><p>%s</p></div>'
                   % (" gap" if gap else "", "Partial match" if gap else "Match", t2(r), t2(e)))
    why = "".join("<p>%s</p>" % t2(x) for x in cfg["why"])
    hero_img = cfg.get("hero_img", "scoop_1")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t2(cfg["title"])}</title><meta name="description" content="{t2(cfg["desc"])}">
<meta property="og:title" content="{t2(cfg["title"])}"><meta property="og:description" content="{t2(cfg["desc"])}"><meta property="og:image" content="https://mahmoudjimmey.github.io/ai-portfolio/img/portrait.jpg">
<meta name="color-scheme" content="light dark"><script>document.documentElement.classList.add('js')</script>
<link rel="stylesheet" href="{b}story.css"><style>:root{{--accent:{acc}}}</style></head>
<body>
<header class="nav"><div class="wrap"><a class="wm" href="#top">Mahmoud Gamal</a><nav><a href="#story">Story</a><a href="#proof">Proof</a><a href="#fit">Fit</a><a href="#contact">Contact</a></nav><a class="btn sm" href="mailto:{EMAIL}">Email me</a></div></header>
<main id="top">
<section class="hero"><div class="wrap">
 <div><h1>{t2(cfg["headline"])}</h1><p class="sub">{t2(cfg["sub"])}</p>
 <div class="cta"><a class="btn" href="mailto:{EMAIL}?subject=Hello%20Mahmoud">Email me</a><a class="btn ghost" href="#proof">See the proof</a></div>
 <p class="for">{t2(cfg["for_line"])}</p></div>
 <div class="vis"><div class="card"><img src="{b}img/{hero_img}.jpg" width="1080" height="1350" alt="A carousel made by my AI newsroom for Address Scoop"></div>
 <div class="me"><img src="{b}img/portrait.jpg" width="112" height="112" alt="Mahmoud Gamal"><p><b>Mahmoud Gamal</b>Cairo, Egypt</p></div></div>
</div></section>
<section id="story" class="sec story"><div class="wrap"><h2 data-r>{t2(cfg["story_title"])}</h2><p class="lead" data-r>{t2(cfg["story_lead"])}</p><ol>{story}</ol></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><h2 data-r>{t2(cfg.get("stats_title", "Numbers I can back up"))}</h2><div class="nums">{nums}</div></div></section>
<section id="proof" class="sec"><div class="wrap"><h2 data-r>{t2(cfg["proof_title"])}</h2><p class="lead" data-r>{t2(cfg["proof_lead"])}</p><div class="bento">{"".join(cells)}</div></div></section>
<section id="fit" class="sec fit"><div class="wrap"><h2 data-r>{t2(cfg["fit_title"])}</h2><p class="lead" data-r>{t2(cfg["fit_intro"])}</p><div class="grid">{"".join(fit)}</div></div></section>
<section class="sec why-sec"><div class="wrap"><h2 data-r>{t2(cfg["why_title"])}</h2><div class="txt" data-r>{why}</div>
 <div class="sig" data-r><img src="{b}img/portrait.jpg" width="104" height="104" alt=""><p><b>Mahmoud Gamal</b>{t2(cfg["role"])}</p></div></div></section>
<section id="contact" class="sec contact"><div class="wrap"><div class="box" data-r><h2>{t2(cfg["contact_title"])}</h2>
 <a class="btn" href="mailto:{EMAIL}?subject=Hello%20Mahmoud">Email me</a>
 <dl><div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div><div><dt>LinkedIn</dt><dd><a href="{LINKEDIN}">mahmoud-gamal-eldeen</a></dd></div><div><dt>Based in</dt><dd>El Sherouk, Cairo</dd></div></dl></div></div></section>
</main>
<footer><div class="wrap"><p>Every image on this page is real output from my own systems. Client data and credentials are not shown.</p><p><a class="tl" href="{LINKEDIN}">LinkedIn</a> <a class="tl" href="{GITHUB}">GitHub</a></p></div></footer>
<script>(function(){{var els=document.querySelectorAll('[data-r]');var li=document.querySelectorAll('.story li');
if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches){{els.forEach(function(e){{e.classList.add('in')}});return}}
var io=new IntersectionObserver(function(es){{es.forEach(function(x){{if(x.isIntersecting){{x.target.classList.add('in');io.unobserve(x.target)}}}})}},{{threshold:.18}});els.forEach(function(e){{io.observe(e)}})}})();</script>
</body></html>"""
