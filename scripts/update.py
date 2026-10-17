"""Fetch the open SneakerPicks price data and merge it into data/prices.csv.

Reads the model list from https://sneakerpicks.nl/data, downloads the JSON per
model and upserts one row per (date, brand, model). Rows already in the CSV are
kept, so the file grows into a full history even though the live endpoints only
return the last 90 days.
"""
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://sneakerpicks.nl"
UA = "sneakerpicks-open-prijsdata/1.0 (+https://github.com/roelvdkrabben/sneakerpicks-open-prijsdata)"
OUT = Path(__file__).resolve().parent.parent / "data" / "prices.csv"
FIELDS = ["date", "brand_slug", "model_slug", "brand", "model", "lowest_price_eur",
          "normal_price_30d_eur", "shops", "model_url"]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def fmt(v):
    return "" if v is None else str(v)


def main():
    page = get(f"{BASE}/data")
    slugs = sorted(set(re.findall(r"/data/([a-z0-9-]+)/([a-z0-9-]+)\.json", page)))
    if not slugs:
        sys.exit("No models found on /data")

    rows = {}
    if OUT.exists():
        with OUT.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                rows[(r["date"], r["brand_slug"], r["model_slug"])] = r

    for brand_slug, model_slug in slugs:
        try:
            d = json.loads(get(f"{BASE}/data/{brand_slug}/{model_slug}.json"))
        except urllib.error.HTTPError as e:
            print(f"skip {brand_slug}/{model_slug}: HTTP {e.code}")
            continue
        m = d["model"]
        for day in d.get("earlier_days", []) + d.get("days", []):
            key = (day["date"], brand_slug, model_slug)
            rows[key] = {
                "date": day["date"],
                "brand_slug": brand_slug,
                "model_slug": model_slug,
                "brand": m["brand"],
                "model": m["model"],
                "lowest_price_eur": fmt(day.get("lowest_price")),
                "normal_price_30d_eur": fmt(day.get("normal_price_30d")),
                "shops": fmt(day.get("shops")),
                "model_url": m["url"],
            }
        time.sleep(1)  # stay far below the 120 requests/hour limit

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        for key in sorted(rows):
            w.writerow(rows[key])
    print(f"{len(slugs)} models, {len(rows)} rows -> {OUT}")


if __name__ == "__main__":
    main()
