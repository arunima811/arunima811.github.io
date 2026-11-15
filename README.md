# arunima-site

Personal site: two tabs, `work` (default, `/`) and `!work` (`/notwork/`). Static [Astro](https://astro.build) site, no client JavaScript.

## Run

```sh
npm ci --ignore-scripts   # .npmrc also sets ignore-scripts
npm run dev               # http://localhost:4321 (drafts visible)
npm run build             # production build in dist/ (drafts skipped)
```

## Edit content

| What | Where |
| --- | --- |
| Intros, links, timeline, side projects, recognition | `src/data/profile.ts` |
| Projects (list + detail page) | `src/content/projects/*.md` |
| Posts written in markdown | `src/content/posts/*.md` |
| Posts written as notebooks | `notebooks/*.ipynb` |
| Photos (work / !work), résumé | `public/me.jpg`, `public/me-life.jpg`, `public/resume.pdf` (the link appears only when the file exists) |

Post front matter:

```yaml
---
title: Why our joins got 8x faster
date: 2026-11-20
tab: work            # work | notwork — which tab lists it
summary: One line for lists and link previews.
draft: true          # optional: shows on localhost only
external: https://…  # optional: list it, but link out instead of rendering here
---
```

Notebooks: the first cell must be a **raw** cell holding that same front matter. The file name becomes the URL (`notebooks/spj-joins.ipynb` → `/posts/spj-joins/`). Cell tags `remove-input`, `remove-output`, `remove-cell` hide parts. Outputs are rendered as saved, so run the notebook before committing.

## Contribution graph

`npm run contributions` reads the public contribution calendars of both GitHub accounts (exactly what a logged-out visitor sees, including anonymous private counts) and merges them into `src/data/contributions.json`; the site draws the last 53 weeks. No token is needed. The deploy workflow re-runs it weekly; if GitHub's page markup changes, the script fails without writing, and the deploy keeps the committed snapshot and shows a warning.

## Deploy

`.github/workflows/deploy.yml` builds and publishes to GitHub Pages on every push to `main` and weekly (to refresh the graph). In the repo settings, set Pages → Source to "GitHub Actions".
