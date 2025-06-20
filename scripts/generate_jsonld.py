import os
import json
from ckan import get_latest_resource_url, download_resource_data
from transform import transform_all

# Output path for the JSON-LD file (served via GitHub Pages)
OUTPUT_PATH = "output/events.jsonld"


def save_jsonld(events, path=OUTPUT_PATH):
    """
    Save a list of JSON-LD event objects to a file.

    Args:
        events (list): The transformed schema.org Event objects.
        path (str): Path to write the JSON file to (default is docs/events.jsonld).
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(events)} events to {path}")


def main():
    print("🚀 Starting JSON-LD generation")

    # Step 1: Get the latest resource URL from CKAN
    resource_url = get_latest_resource_url()

    # Step 2: Download all paginated raw data
    raw_data = download_resource_data(resource_url)

    # Step 3: Transform into schema.org/Event format
    jsonld_events = transform_all(raw_data)

    # Step 4: Write output to file
    save_jsonld(jsonld_events)

    print("🏁 Done.")


if __name__ == "__main__":
    main()
