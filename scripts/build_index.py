"""Regenerate index.html from briefings/briefing_YYYY_MM_DD.html files."""
import datetime, html, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
css = (root / "scripts" / "style.css").read_text()
rows = []
for f in sorted((root / "briefings").glob("briefing_*.html"), reverse=True):
    m = re.match(r"briefing_(\d{4})_(\d{2})_(\d{2})\.html$", f.name)
    if not m:
        continue
    d = datetime.date(*map(int, m.groups()))
    s = f.read_text(encoding="utf-8")
    k = re.search(r'class="key".*?<h2><a[^>]*>(.*?)</a></h2>', s, re.S)
    head = k.group(1) if k else "Daily briefing"
    rows.append(f'<article class="card"><div class="meta"><time datetime="{d}">{d:%A, %d %B %Y}</time></div>'
                f'<h3><a href="briefings/{f.name}">{head}</a></h3></article>')
latest = f'<p><a href="briefings/{sorted((root/"briefings").glob("briefing_*.html"))[-1].name}">Open the latest briefing</a></p>' if rows else ""
doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AgBioTech Briefings</title><style>{css}</style></head><body><div class="wrap">
<header><h1>Daily AgBioTech Briefings</h1><p>Plant Sciences, Biotechnology and Agriculture &middot; {len(rows)} briefings</p></header>
{latest}
<section>{''.join(rows)}</section>
<footer>Each card shows that day's key takeaway. Compiled automatically by Claude.</footer>
</div></body></html>"""
(root / "index.html").write_text(doc, encoding="utf-8")
print(f"index.html: {len(rows)} briefings")
