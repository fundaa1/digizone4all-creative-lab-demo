"""Controlled static build for DigiZone Connect v0.2 profiles.

Reads connect/data/organisations.json and writes the directory page,
one deep-linked profile page per static-demo record, and one JSON file
per record. Exporting a JSON file from the capture page does not run
this script and does not publish a profile.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "organisations.json"
STATIC_NOTE = "Included in the fictional static demo. This is not a live public listing."

LOCATIONS = ["Durban", "KwaMashu", "Umlazi", "Pietermaritzburg"]
CATEGORIES = ["ECD Centre", "Bakery", "Plumbing"]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def place_line(location: dict, include_province: bool) -> str:
    candidates = [location["area"], location["city"]]
    if include_province:
        candidates.append(location["province"])
    parts: list[str] = []
    for part in candidates:
        if part and part not in parts:
            parts.append(part)
    return ", ".join(parts)


def initials(name: str) -> str:
    letters: list[str] = []
    for part in name.split()[:2]:
        cleaned = "".join(character for character in part if character.isalnum())
        if cleaned:
            letters.append(cleaned[0].upper())
    return "".join(letters) or "DZ"


def chrome(title: str, current: str) -> str:
    def link(href: str, label: str, key: str) -> str:
        current_attr = ' aria-current="page"' if current == key else ""
        return f'<a href="{href}"{current_attr}>{label}</a>'

    nav = "".join(
        [
            link("../index.html", "Lab home", "lab"),
            link("index.html", "Directory", "directory"),
            link("capture.html", "Capture", "capture"),
        ]
    )
    return f"""<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#10192d">
<meta name="description" content="DigiZone Connect fictional directory demo, not a live service.">
<meta name="robots" content="noindex,nofollow">
<title>{esc(title)}</title>
<link rel="stylesheet" href="assets/dz-connect.css?v=0.2">
</head>
<body data-page="PAGE">
<aside class="demo-banner" aria-label="Demo notice"><div class="wrap"><strong>DEMO — FICTIONAL DATA ONLY</strong><span>Made-up organisations. No real telephone numbers. No beneficiary information. Nothing here is a live service.</span></div></aside>
<header class="top"><div class="wrap bar"><a class="brand" href="../index.html"><span class="brandmark">DZ<span aria-hidden="true">↗</span></span> DigiZone<span style="color:var(--lime)">4All</span></a><nav class="nav" aria-label="Demo navigation">{nav}</nav></div></header>
"""


def footer() -> str:
    return """<footer class="footer"><div class="wrap"><span>DEMO · DigiZone Connect v0.2 — Fictional founder exploration. No organisational adoption is implied.</span><span>Visible. Connected. Capable. · People First. Technology Second.</span></div></footer>
<script src="assets/dz-connect.js?v=0.2"></script>
</body>
</html>
"""


def profile_card(record: dict) -> str:
    location = record["location"]
    place = place_line(location, True)
    offerings = "".join(f"<li>{esc(item)}</li>" for item in record["offerings"])
    return f"""<div class="business" id="profile">
<div class="banner"><div class="avatar" aria-hidden="true">{esc(initials(record["name"]))}</div><div><span class="tag" style="background:#dafa74">DigiZone Connect · Demo</span><p class="profile-name">{esc(record["name"])}</p><p>⌖ {esc(place)}</p></div></div>
<div class="profile-meta"><span class="pill">{esc(record["category"])}</span><span class="pill">{esc(location["province"])}</span><span class="pill">◷ {esc(record["hours"])}</span></div>
<hr class="softline">
<h2>About</h2>
<p>{esc(record["summary"])}</p>
<h2>What is offered</h2>
<ul class="offerings">{offerings}</ul>
<div class="tip"><strong>How to connect</strong><br>{esc(record["contact"]["label"])}<br><span class="small">Demonstration only. No message is sent and no telephone number is published.</span></div>
<p class="small">Fictional profile. Information is not independently verified. Copying this page does not create a live listing.</p>
</div>"""


def search_blob(record: dict) -> str:
    location = record["location"]
    parts = [
        record["name"],
        record["category"],
        location["area"],
        location["city"],
        location["province"],
        record["summary"],
        record["hours"],
        *record["offerings"],
    ]
    return " ".join(parts)


def directory_page(records: list[dict]) -> str:
    cards = []
    for record in records:
        location = record["location"]
        cards.append(
            f"""<article class="entry" data-category="{esc(record["category"])}" data-area="{esc(location["area"])}" data-city="{esc(location["city"])}" data-search="{esc(search_blob(record))}">
<span class="tag">DEMO · {esc(record["category"])}</span>
<h3>{esc(record["name"])}</h3>
<p>⌖ {esc(place_line(location, False))}</p>
<p>{esc(record["summary"])}</p>
<div class="actions"><a class="btn" href="{esc(record["id"])}.html">Open profile</a></div>
</article>"""
        )
    category_options = '<option value="all">All categories</option>' + "".join(
        f'<option value="{esc(name)}">{esc(name)}</option>' for name in CATEGORIES
    )
    location_options = '<option value="all">All locations</option>' + "".join(
        f'<option value="{esc(name)}">{esc(name)}</option>' for name in LOCATIONS
    )
    page = chrome("DEMO · Directory | DigiZone Connect", "directory")
    page = page.replace('data-page="PAGE"', 'data-page="directory"', 1)
    page += f"""<section class="hero"><div class="wrap inner"><p class="eyebrow">DigiZone Connect · v0.2</p><h1>Find a local organisation. <em>In a fictional directory.</em></h1><p class="lede">Three made-up organisations in KwaZulu-Natal. Search, filter, and open a profile link that stands on its own.</p><div class="chips"><span class="chip">● DEMO · Fictional simulation</span><span class="chip">◆ Static pages · No account</span><span class="chip">↗ Export is not publication</span></div></div></section>
<main class="main" id="content"><div class="wrap">
<section class="panel" aria-label="Search and filters"><p class="smallcaps">Search the demo</p><div class="filters"><div><label class="field" for="search">Search</label><input class="input" id="search" type="search" placeholder="Try bakery, Umlazi or geyser"></div><div><label class="field" for="category-filter">Category</label><select class="input" id="category-filter">{category_options}</select></div><div><label class="field" for="location-filter">Location</label><select class="input" id="location-filter">{location_options}</select></div></div></section>
<div class="row-between" style="margin-top:26px"><h2 class="section-title">Fictional directory</h2><span id="count" class="pill">{len(records)} fictional profiles</span></div>
<div class="directory" id="directory">{"".join(cards)}</div>
<div id="empty" class="panel" hidden><strong>No matches.</strong><p class="help">Try another name, category or location. Only the three fictional profiles are in this demo.</p></div>
<section class="callout boundary"><h2>A downloaded record is not a public profile.</h2><p>The capture page can save a JSON file on your device. That file is not listed here. In this version, public profile publication is a controlled static build and deploy step.</p></section>
<div class="actions"><a class="btn" href="capture.html">Prepare a fictional record</a></div>
</div></main>
"""
    page += footer()
    return page


def profile_page(record: dict) -> str:
    location = record["location"]
    payload = json.dumps(record, ensure_ascii=False, indent=2).replace("<", "\\u003c")
    page = chrome(f"DEMO · {record['name']} | DigiZone Connect", "directory")
    page = page.replace(
        'data-page="PAGE"',
        f'data-page="profile" data-name="{esc(record["name"])}"',
        1,
    )
    # Profile pages should not mark Directory as the current page.
    page = page.replace(' href="index.html" aria-current="page"', ' href="index.html"', 1)
    page += f"""<section class="hero"><div class="wrap inner"><p class="eyebrow">Fictional profile · {esc(record["category"])}</p><h1>{esc(record["name"])}</h1><p class="lede">{esc(place_line(location, True))}. This page is a demonstration profile, not a live listing.</p><div class="chips"><span class="chip">● DEMO · Fictional data</span><span class="chip">◆ No telephone published</span></div></div></section>
<main class="main" id="content"><div class="wrap">
{profile_card(record)}
<section class="panel" style="margin-top:21px"><p class="smallcaps">Copy or share</p><h2>Profile link</h2><p class="help">This address opens the fictional profile directly. It does not depend on a previous visit.</p><div class="url-line"><code id="profile-url">/connect/{esc(record["id"])}</code></div><div class="actions"><button type="button" class="btn" id="copy-url">Copy profile URL</button><button type="button" class="btn secondary" id="share">Share</button><a class="btn secondary" href="data/{esc(record["id"])}.json">View JSON record</a></div><p id="notice" class="status" role="status"></p></section>
<section class="callout boundary"><h2>Static demo listing.</h2><p>{esc(record["publication"]["note"])}</p></section>
<p class="actions"><a class="btn secondary" href="index.html">Back to directory</a></p>
</div></main>
<script type="application/json" id="organisation-record">{payload}</script>
"""
    page += footer()
    return page


def main() -> None:
    records = json.loads(DATA.read_text(encoding="utf-8"))
    if not isinstance(records, list) or len(records) != 3:
        raise SystemExit("organisations.json must contain exactly three demo records")
    for record in records:
        if record["publication"]["status"] != "static-demo":
            raise SystemExit(f"{record['id']} is not marked static-demo")
        if record["publication"]["note"] != STATIC_NOTE:
            raise SystemExit(f"{record['id']} publication note drifted")
        (ROOT / "data" / f"{record['id']}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (ROOT / f"{record['id']}.html").write_text(profile_page(record), encoding="utf-8")
    (ROOT / "index.html").write_text(directory_page(records), encoding="utf-8")
    print("rendered directory and 3 profile pages")


if __name__ == "__main__":
    main()
