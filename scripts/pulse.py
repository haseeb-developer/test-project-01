#!/usr/bin/env python3
"""Feeds assets/activity.svg with the last 60 days of public GitHub events. PULSE_MOCK=1 for an offline test."""
import datetime as dt, json, os, sys, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import build
login = build.CONFIG["login"]
if os.environ.get("PULSE_MOCK"): ev = [{"created_at": dt.datetime.now(dt.timezone.utc).isoformat()}] * 5
else:
    rq = urllib.request.Request(f"https://api.github.com/users/{login}/events/public?per_page=100", headers={"Accept": "application/vnd.github+json"})
    if os.environ.get("GITHUB_TOKEN"): rq.add_header("Authorization", "Bearer " + os.environ["GITHUB_TOKEN"])
    ev = json.load(urllib.request.urlopen(rq, timeout=20))
today, cnt = dt.datetime.now(dt.timezone.utc).date(), [0] * 60
for e in ev:
    d = (today - dt.datetime.fromisoformat(e["created_at"].replace("Z", "+00:00")).date()).days
    if 0 <= d < 60: cnt[59 - d] += 1
build.w("activity.svg", build.activity(cnt if any(cnt) else None, "live" if any(cnt) else "sample")); print("activity.svg updated", sum(cnt), "events")
