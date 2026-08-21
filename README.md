# Course website: GPH-GU 2182 Statistical Programming in R (Fall 2026)

Quarto website for the course. Rendered output goes to `docs/` so GitHub Pages
can serve it directly from the main branch.

## Workflow

```bash
quarto render     # rebuilds docs/
git add -A && git commit -m "Update site" && git push
```

## Publishing (one-time setup)

1. Push this folder to a GitHub repository.
2. In the repo: Settings → Pages → Source: "Deploy from a branch",
   Branch: `main`, Folder: `/docs`.
3. The site appears at `https://<user-or-org>.github.io/<repo>/`.

## Structure

- `_quarto.yml` — site config (navbar, sidebar, theme)
- `index.qmd` — home page
- `syllabus.qmd`, `schedule.qmd`, `project.qmd`, `ai-policy.qmd`
- `weeks/week-01.qmd` … `week-14.qmd` — one page per session; post slides and
  exercise links in the Materials section of each
