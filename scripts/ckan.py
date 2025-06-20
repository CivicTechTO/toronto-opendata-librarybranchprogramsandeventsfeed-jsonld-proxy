import requests
from urllib.parse import urljoin

# Base URL for the City of Toronto's CKAN Open Data instance
BASE_CKAN_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
PACKAGE_NAME = "festivals-events"  # This is the CKAN "package" (dataset) name


def get_latest_resource_url():
    """
    Fetch the latest downloadable (non-datastore) resource URL from CKAN.

    Returns:
        str: The URL of the first non-datastore resource in the package.
    Raises:
        RuntimeError: If no suitable resource is found.
    """
    package_url = urljoin(BASE_CKAN_URL, "/api/3/action/package_show")
    params = {"id": PACKAGE_NAME}

    print("🔍 Fetching CKAN package metadata...")
    response = requests.get(package_url, params=params)
    response.raise_for_status()
    data = response.json()

    for resource in data["result"]["resources"]:
        if not resource.get("datastore_active"):  # We only want direct file downloads
            return resource["url"]

    raise RuntimeError("❌ No suitable non-datastore resource found in CKAN package.")


def download_resource_data(resource_url, batch_size=500, max_pages=20):
    """
    Download all paginated event data from the resource URL using ?limit and ?offset.

    Args:
        resource_url (str): The base data endpoint (e.g. from CKAN resource["url"])
        batch_size (int): Number of records per page (default 500)
        max_pages (int): Safety cap to avoid runaway loops

    Returns:
        list: All event entries combined across pages
    """
    print(f"⬇️ Downloading full event data from: {resource_url}")

    all_events = []
    offset = 0
    page = 0

    while page < max_pages:
        paged_url = f"{resource_url}&limit={batch_size}&offset={offset}"
        response = requests.get(paged_url)
        response.raise_for_status()
        batch = response.json()

        if not batch:
            break  # No more data

        all_events.extend(batch)
        print(f"📦 Page {page + 1}: {len(batch)} events")

        if len(batch) < batch_size:
            break  # Last page

        offset += batch_size
        page += 1

    print(f"✅ Downloaded {len(all_events)} total events")
    return all_events
