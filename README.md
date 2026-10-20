# The AgBioTech Briefing

Daily interactive briefings on plant sciences, biotechnology and agriculture, compiled by a scheduled Claude routine.
Live site: https://abhirichster.github.io/agbiotech-briefings/

## Layout

- `data/briefing_YYYY_MM_DD.json`: the content of each issue (source of truth).
- `briefings/briefing_YYYY_MM_DD.html`: rendered, self-contained daily pages (do not edit by hand).
- `index.html`: archive page, rendered from the same data.
- `scripts/render.py`: renders every issue plus the index. Run `python3 scripts/render.py`.

## Data format

```json
{
  "date": "2026-10-20",
  "lead": {"title": "...", "url": "...", "summary": "...",
           "notes": [{"label": "Plant science", "text": "..."}]},
  "sections": {
    "plant":   [{"date": "2026-10-20", "source": "Nature Plants", "url": "...", "title": "...", "summary": "..."}],
    "biotech": [],
    "ag":      []
  },
  "methods": "Coverage window and verification notes."
}
```

Text fields may contain inline HTML (`<i>` for species and gene names, entities such as `&amp;`). Use 10 items per section, three `notes`, and no em or en dashes in summaries.
