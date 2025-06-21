import os
import json
from datetime import datetime
from ckan import get_latest_resource_url, stream_resource_data
from transform import transform_event
import hashlib

OUTPUT_DIR = "data/daily_jsonl"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_event_key(event):
    """Create a unique key for an event using its name, date, and location."""
    key_source = f"{event.get('name', '')}|{event.get('startDate', '')}|{event.get('location', {}).get('name', '')}"
    return hashlib.sha1(key_source.encode("utf-8")).hexdigest()

def write_event_jsonl(event):
    """Write a single event to its respective daily .jsonl file if not already present."""
    date_str = event.get("startDate", "")[:10]
    if not date_str:
        return

    output_path = os.path.join(OUTPUT_DIR, f"{date_str}.jsonl")
    event_key = generate_event_key(event)

    # Load existing keys for the day (just once per day/file)
    existing_keys = set()
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    existing_event = json.loads(line)
                    key = generate_event_key(existing_event)
                    existing_keys.add(key)
                except json.JSONDecodeError:
                    continue

    # Only write if the event is not already in the file
    if event_key not in existing_keys:
        with open(output_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")



def main():
    print("🚀 Starting JSON-LD generation")
    resource_url = get_latest_resource_url()
    print(f"📡 Resource URL: {resource_url}")

    count = 0
    for item in stream_resource_data(resource_url):
        try:
            jsonld_event = transform_event(item)
            if jsonld_event:
                write_event_jsonl(jsonld_event)
                count += 1
                if count % 500 == 0:
                    print(f"✍️ Processed {count} events...")
        except Exception as e:
            print(f"⚠️ Failed to process event: {e}")

    print(f"✅ Finished. Wrote {count} events to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
