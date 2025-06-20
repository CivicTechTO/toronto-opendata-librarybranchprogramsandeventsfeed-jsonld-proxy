# Festival & Events JSON-LD Proxy

**A daily-refreshed JSON-LD proxy for Toronto’s Festivals & Events open data feed.**  
Built to help make Toronto the most programmable city in the world.

## Function

This project transforms the [City of Toronto’s Festivals and Events dataset](https://open.toronto.ca/dataset/festivals-events/) into structured, linked data using the [schema.org/Event](https://schema.org/Event) vocabulary.

The result is a free, publicly hosted JSON-LD feed that enables developers, search engines, and civic tools to discover and reuse Toronto's official event listings in a standardized, machine-readable format.

## Purpose

- Demonstrates how open data can power real-world tools with **minimal cost and friction**.
- Enables **events aggregators, civic apps, and open data projects** to work with a common standard and data ontology.
- Bridges the gap between _open datasets_ and _programmable cities_.

## Orientation

### Build

**Install dependencies**

```zsh
pip install -r requirements.txt
```

**Generate the JSON-LD**

```zsh
python scripts/generate_jsonld.py
```

### Usage

> _(Coming soon)_

You can use this link directly in:

- Events apps and civic dashboards
- Schema.org-aware tools and validators

## About

### Origin

This project was built as part of **PROGRAM: Toronto** — a hackathon to make Toronto the world’s most programmable city — in collaboration with the City of Toronto Open Data team.

### Acknowledgments

Built by [@jordyarms](https://github.com/jordyarms)  
Maintained by _(you?)_

Special thanks to:

- [City of Toronto Open Data](https://open.toronto.ca/)
- PROGRAM: Toronto

## License

- **Code** is licensed under the [MIT License](LICENSE).
- **Source event data** is licensed under the [Open Government Licence – Toronto](https://open.toronto.ca/open-data-licence/).  
  Please attribute as:
  > Contains information licensed under the Open Government Licence – Toronto.
