import os
import json
from datetime import datetime
from ckan import get_latest_resource_url, download_resource_data
from transform import transform_event

BASE_PATH = "docs/events"


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def event_month(event):
    try:
        dt = datetime.fromisoformat(event["startDate"].replace("Z", "+00:00"))
        return dt.strftime("%Y-%m")
    except Exception:
        return None


def initialize_streams():
    return {}


def append_event_to_file(event, streams, month):
    if month not in streams:
        path = os.path.join(BASE_PATH, f"{month}.jsonld")
        f = open(path, "w", encoding="utf-8")
        f.write("[\n")
        streams[month] = {"file": f, "count": 0}

    stream = streams[month]
    if stream["count"] > 0:
        stream["file"].write(",\n")
    json.dump(event, stream["file"], ensure_ascii=False, indent=2)
    stream["count"] += 1


def finalize_streams(streams):
    for stream in streams.values():
        stream["file"].write("\n]\n")
        stream["file"].close()


def write_index_file(available_months):
    index_path = os.path.join(BASE_PATH, "index.json")
    index = {
        "available": sorted(available_months),
        "latest": max(available_months) if available_months else "",
    }
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    print(f"📁 Index file written with {len(available_months)} months")


def main():
    print("🚀 Starting memory-efficient JSON-LD generation")
    ensure_dir(BASE_PATH)
    resource_url = get_latest_resource_url()
    raw_events = download_resource_data(resource_url, batch_size=500, max_pages=2000)

    streams = initialize_streams()
    seen_months = set()
    event_count = 0

    for raw in raw_events:
        try:
            transformed = transform_event(raw)
            month = event_month(transformed)
            if not month:
                continue
            append_event_to_file(transformed, streams, month)
            seen_months.add(month)
            event_count += 1
        except Exception as e:
            print(f"⚠️ Error transforming event: {e}")

    finalize_streams(streams)
    write_index_file(seen_months)
    print(f"✅ Written {event_count} events across {len(seen_months)} month files")
    print("🏁 Done.")


if __name__ == "__main__":
    main()
