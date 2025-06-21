import os
import json
from datetime import datetime, timezone
from glob import glob

INPUT_DIR = "data/daily_jsonl"
OUTPUT_ALL = "data/all.jsonld"
OUTPUT_UPCOMING = "data/upcoming.jsonld"

def load_all_events():
    events = []
    for file_path in sorted(glob(f"{INPUT_DIR}/*.jsonl")):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    event = json.loads(line)
                    events.append(event)
                except json.JSONDecodeError:
                    continue
    return events

def save_jsonld(events, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

def main():
    print("🔄 Building merged JSON-LD files...")
    all_events = load_all_events()
    save_jsonld(all_events, OUTPUT_ALL)
    print(f"✅ Wrote {len(all_events)} events to {OUTPUT_ALL}")

    # Filter upcoming
    now = datetime.now(timezone.utc).isoformat()
    upcoming = [e for e in all_events if e.get("startDate") >= now]
    save_jsonld(upcoming, OUTPUT_UPCOMING)
    print(f"✅ Wrote {len(upcoming)} upcoming events to {OUTPUT_UPCOMING}")

if __name__ == "__main__":
    main()
