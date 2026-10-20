"""One-off: convert legacy briefing HTML pages into data/briefing_YYYY_MM_DD.json."""
import json, pathlib, re, sys
from html import unescape

root = pathlib.Path(__file__).resolve().parent.parent

def inner(s):
    return s.strip()

for f in sorted((root / "briefings").glob("briefing_*.html")):
    s = f.read_text(encoding="utf-8")
    date = re.search(r"briefing_(\d{4})_(\d{2})_(\d{2})", f.name).groups()
    key = re.search(r'<aside class="key">(.*?)</aside>', s, re.S).group(1)
    lead_a = re.search(r'<h2><a href="([^"]+)"[^>]*>(.*?)</a></h2>', key, re.S)
    lead_p = re.search(r"</h2>\s*<p>(.*?)</p>", key, re.S)
    notes = []
    for li in re.findall(r"<li>(.*?)</li>", key, re.S):
        m = re.match(r"<b>(.*?):?</b>:?\s*(.*)", li, re.S)
        notes.append({"label": m.group(1).rstrip(":"), "text": m.group(2).strip()} if m else {"label": "", "text": li})
    sections = {}
    for k, body in re.findall(r'<section role="tabpanel" id="p-(\w+)"[^>]*>(.*?)</section>', s, re.S):
        items = []
        for art in re.findall(r'<article class="card">(.*?)</article>', body, re.S):
            d = re.search(r'<time datetime="([^"]+)"', art).group(1)
            src = re.search(r'<span class="src">(.*?)</span>', art, re.S).group(1)
            a = re.search(r'<h3><a href="([^"]+)"[^>]*>(.*?)</a></h3>', art, re.S)
            p = re.search(r"</h3>\s*<p>(.*?)</p>", art, re.S).group(1)
            items.append({"date": d, "source": src, "url": unescape(a.group(1)), "title": a.group(2), "summary": p})
        sections[k] = items
    footer = re.search(r"<footer>(.*?)</footer>", s, re.S).group(1)
    data = {
        "date": "-".join(date),
        "lead": {"title": lead_a.group(2), "url": unescape(lead_a.group(1)), "summary": lead_p.group(1), "notes": notes},
        "sections": sections,
        "methods": footer.replace(" Compiled automatically by Claude.", ""),
    }
    out = root / "data" / f.name.replace(".html", ".json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(out.name, {k: len(v) for k, v in sections.items()}, len(notes))
