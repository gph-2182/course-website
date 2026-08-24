#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEDULE_PATH = os.path.join(BASE_DIR, "data", "schedule_release.json")

def main():
    if not os.path.exists(SCHEDULE_PATH):
        print(f"Schedule file not found at {SCHEDULE_PATH}")
        return

    with open(SCHEDULE_PATH, "r", encoding="utf-8") as f:
        schedule = json.load(f)

    # Check if instructor override is active
    release_all = os.environ.get("RELEASE_ALL", "false").lower() in ("true", "1", "yes")
    
    # Current time in UTC
    now = datetime.now(timezone.utc)
    print(f"[Release Manager] Current time (UTC): {now.isoformat()}")
    print(f"[Release Manager] RELEASE_ALL override: {release_all}")

    released_weeks = []
    locked_weeks = []

    for item in schedule:
        w_num = item["week"]
        rel_str = item["release_date"]
        rel_dt = datetime.fromisoformat(rel_str)
        
        is_released = release_all or (now >= rel_dt)
        if is_released:
            released_weeks.append(w_num)
        else:
            locked_weeks.append(w_num)

    print(f"[Release Manager] Released Weeks: {released_weeks}")
    print(f"[Release Manager] Locked Weeks: {locked_weeks}")

if __name__ == "__main__":
    main()
