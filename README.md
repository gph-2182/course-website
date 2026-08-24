# Course Website: GPH-GU 2182 Statistical Programming in R (Fall 2026)

Quarto website for the course, hosted on GitHub Pages at **`https://gph-2182.github.io/`**.

---

## 🚀 Automated Sunday Release System (Method 1)

Course materials (slides, in-class exercises, and weekly assignments) are automated via **GitHub Actions** to unlock every **Sunday morning at 8:00 AM EDT** before Wednesday's class:

- **Schedule Data:** Configured in `data/schedule_release.json`.
- **Pre-Render Hook:** `tools/prepare-release.sh` checks the calendar and gates future weeks.
- **Automated Workflow:** `.github/workflows/weekly-release.yml` triggers every Sunday at 12:00 UTC (8:00 AM EDT) to re-render and deploy to GitHub Pages (`gh-pages` branch).

### Instructor Local Override
When developing on your laptop, preview all 14 weeks in full anytime:
```bash
RELEASE_ALL=true quarto preview
```

---

## 🛠️ GitHub Repository & Pages Setup

1. **Rename the repo on GitHub (to get the clean root URL):**
   - Go to repo **Settings** $\rightarrow$ **Repository name** $\rightarrow$ change `course-website` to **`gph-2182.github.io`**.
2. **Update local remote & push:**
   ```bash
   git remote set-url origin https://github.com/gph-2182/gph-2182.github.io.git
   git add -A
   git commit -m "Configure automated Sunday releases and root domain"
   git push origin main
   ```
3. **Configure GitHub Pages (One-Time):**
   - Settings $\rightarrow$ **Pages** $\rightarrow$ Source: `Deploy from a branch` $\rightarrow$ Branch: `gh-pages` / `/ (root)`.

The site is served cleanly at: **`https://gph-2182.github.io/`**
