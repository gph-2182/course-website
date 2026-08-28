#!/usr/bin/env python3
"""Release manager: gates unreleased weekly materials at render time.

Runs as the Quarto pre-render hook (tools/prepare-release.sh). File
modifications only happen inside GitHub Actions (fresh checkout), never on a
local machine, so instructor working copies are always left untouched.
Locked weeks get a placeholder week page; their slides and in-class sources
are removed from the checkout before rendering.

Override: RELEASE_ALL=true renders everything (local preview default).
"""
import json
import os
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEDULE_PATH = os.path.join(BASE_DIR, "data", "schedule_release.json")

PLACEHOLDER = """---
title: "Week {week}: {topic}"
subtitle: "{class_pretty} · 2:00–4:40 PM · Bobst LL138"
---

::: {{.callout-note}}
### \U0001f512 Not yet released

Materials for this week (slides, in-class exercise, and weekly exercise)
unlock automatically on **{release_pretty} at 8:00 AM ET**.
:::

## Before class

- **Read:** {readings}
"""


def pretty_date(dt):
    return f"{dt.strftime('%b')} {dt.day}, {dt.year}"


def main():
    if not os.path.exists(SCHEDULE_PATH):
        print(f"Schedule file not found at {SCHEDULE_PATH}")
        return

    with open(SCHEDULE_PATH, "r", encoding="utf-8") as f:
        schedule = json.load(f)

    release_all = os.environ.get("RELEASE_ALL", "false").lower() in ("true", "1", "yes")
    in_ci = os.environ.get("GITHUB_ACTIONS", "").lower() == "true"

    now = datetime.now(timezone.utc)
    print(f"[Release Manager] Current time (UTC): {now.isoformat()}")
    print(f"[Release Manager] RELEASE_ALL override: {release_all}")
    print(f"[Release Manager] Running in CI: {in_ci}")

    released_weeks = []
    locked_weeks = []

    for item in schedule:
        w_num = item["week"]
        rel_dt = datetime.fromisoformat(item["release_date"])

        if release_all or now >= rel_dt:
            released_weeks.append(w_num)
        else:
            locked_weeks.append((w_num, item))

    print(f"[Release Manager] Released Weeks: {released_weeks}")
    print(f"[Release Manager] Locked Weeks: {[w for w, _ in locked_weeks]}")

    if not in_ci or release_all:
        print("[Release Manager] Not gating files (local run or RELEASE_ALL).")
        return

    for w_num, item in locked_weeks:
        ww = f"{w_num:02d}"
        class_dt = datetime.fromisoformat(item["class_date"])
        rel_dt = datetime.fromisoformat(item["release_date"])

        week_page = os.path.join(BASE_DIR, "weeks", f"week-{ww}.qmd")
        if os.path.exists(week_page):
            with open(week_page, "w", encoding="utf-8") as f:
                f.write(PLACEHOLDER.format(
                    week=w_num,
                    topic=item["topic"],
                    readings=item["readings"],
                    class_pretty=pretty_date(class_dt),
                    release_pretty=f"Sunday, {pretty_date(rel_dt)}",
                ))
            print(f"[Release Manager] Locked page written: weeks/week-{ww}.qmd")

        for gated in (
            os.path.join(BASE_DIR, "weeks", "slides", f"week-{ww}-slides.qmd"),
            os.path.join(BASE_DIR, "weeks", "inclass", f"week-{ww}-inclass.qmd"),
        ):
            if os.path.exists(gated):
                os.remove(gated)
                print(f"[Release Manager] Removed unreleased source: {os.path.relpath(gated, BASE_DIR)}")


if __name__ == "__main__":
    main()
