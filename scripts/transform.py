from urllib.parse import urljoin
from html import unescape
from utils import extract_geo

# Used to prepend image URLs if they are relative
TORONTO_IMAGE_BASE = "https://www.toronto.ca"


def transform_event(cal_event):
    """
    Convert a single raw event record to schema.org/Event JSON-LD format.
    """
    evt = cal_event["calEvent"]
    location = evt.get("locations", [{}])[0]
    address = location.get("address", "")
    reservation = evt.get("reservation", {})

    # Get first datetime range for the event
    start_dt = evt.get("dates", [{}])[0].get("startDateTime")
    end_dt = evt.get("dates", [{}])[0].get("endDateTime")

    # Clean up relative image URLs
    image_url = evt.get("image", {}).get("url")
    if image_url and not image_url.startswith("http"):
        image_url = urljoin(TORONTO_IMAGE_BASE, image_url)

    # Choose the most relevant URL: reservation site preferred
    primary_url = reservation.get("website") or evt.get("eventWebsite")

    # Convert category string to a list of keywords
    raw_keywords = evt.get("categoryString", "")
    keywords = [unescape(k.strip()) for k in raw_keywords.split(",") if k.strip()]

    # Build core schema.org Event structure
    event = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": unescape(evt.get("eventName", "")),
        "startDate": start_dt,
        "endDate": end_dt,
        "location": {
            "@type": "Place",
            "name": unescape(location.get("locationName", "Toronto")),
            "address": {
                "@type": "PostalAddress",
                "streetAddress": address,
                "addressLocality": "Toronto",
                "addressRegion": "ON",
                "addressCountry": "CA",
            },
            "geo": extract_geo(location),  # Optional but added if available
        },
        "description": unescape(evt.get("description", "")),
        "url": primary_url,
        "image": image_url,
        "organizer": {
            "@type": "Organization",
            "name": unescape(evt.get("orgName", "")),
            "email": evt.get("orgEmail"),
            "telephone": evt.get("orgPhone"),
        },
        "isAccessibleForFree": evt.get("freeEvent", "").strip().lower() == "yes",
        "keywords": keywords,
    }

    # Optionally add offer block (e.g. cost + ticket URL)
    offer = build_offer(evt)
    if offer:
        event["offers"] = offer

    return event


def build_offer(evt):
    """
    Optionally build an Offer block for pricing and ticketing.
    """
    cost = evt.get("cost", {})
    reservation_url = evt.get("reservation", {}).get("website")
    offer = {}

    if isinstance(cost, dict):
        # Handle different cost formats
        if "from" in cost or "to" in cost:
            offer["price"] = cost.get("from") or cost.get("to")
        elif "ga" in cost:
            offer["price"] = cost["ga"]

        if "price" in offer:
            offer["priceCurrency"] = "CAD"

    if reservation_url:
        offer["url"] = reservation_url

    return {"@type": "Offer", **offer} if offer else None


def transform_all(raw_events):
    """
    Transform all raw records into JSON-LD Event objects.
    """
    return [transform_event(evt) for evt in raw_events]
