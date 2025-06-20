def extract_geo(location):
    """
    Extract latitude and longitude as a schema.org GeoCoordinates object.

    Args:
        location (dict): A location object from the raw event data.

    Returns:
        dict or None: A schema.org-compatible GeoCoordinates block, or None if missing.
    """
    coords = location.get("coords")

    # Handle if coords is a list of dicts
    if isinstance(coords, list) and coords:
        coords = coords[0]

    # Handle if coords is a single dict
    if isinstance(coords, dict):
        return {
            "@type": "GeoCoordinates",
            "latitude": coords.get("lat"),
            "longitude": coords.get("lng"),
        }

    # Fallback if coords is missing or unrecognized format
    return None
