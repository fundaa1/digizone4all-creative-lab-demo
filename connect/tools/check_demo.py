"""Checks DigiZone Connect v0.2 static records, pages and v0.1 preservation."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONNECT = ROOT / "connect"
DATA = CONNECT / "data" / "organisations.json"
CATEGORIES = {"ECD Centre", "Bakery", "Plumbing"}
CONTACT = "Demo enquiry only"
STATIC_NOTE = "Included in the fictional static demo. This is not a live public listing."
EXPORT_NOTE = "Exporting this file does not publish a public profile. Public publication in this version is a controlled static build and deploy step."
V01 = [
    "index.html",
    "visible.html",
    "connected.html",
    "capable.html",
    "robots.txt",
    "vercel.json",
    "README.md",
]
PHONE = re.compile(r"(?:\+|00)27[\s-]?\d|\b0\d{2}[\s-]?\d{3}[\s-]?\d{4}\b")
EMAIL = re.compile(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", re.I)
IDENTITY = re.compile(r"\b\d{13}\b")
WHATSAPP = re.compile(r"whatsapp", re.I)

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def private_hits(label: str, text: str) -> None:
    if PHONE.search(text):
        fail(f"{label} contains a telephone-like pattern")
    if EMAIL.search(text):
        fail(f"{label} contains an email address")
    if IDENTITY.search(text):
        fail(f"{label} contains a 13-digit identity-like number")
    if WHATSAPP.search(text):
        fail(f"{label} contains a messaging handle")


def check_record(record: dict, *, exported: bool) -> None:
    label = record.get("id", "<missing id>")
    required = [
        "schemaVersion",
        "id",
        "name",
        "category",
        "location",
        "summary",
        "hours",
        "offerings",
        "contact",
        "fictional",
        "publication",
        "profilePath",
    ]
    for key in required:
        if key not in record:
            fail(f"{label} missing {key}")
    if record.get("schemaVersion") != "0.2":
        fail(f"{label} schemaVersion")
    if record.get("category") not in CATEGORIES:
        fail(f"{label} category")
    if record.get("fictional") is not True:
        fail(f"{label} fictional flag")
    contact = record.get("contact") or {}
    if contact.get("label") != CONTACT:
        fail(f"{label} contact label")
    if set(contact) != {"label"}:
        fail(f"{label} contact has extra fields")
    location = record.get("location") or {}
    for key in ("area", "city", "province"):
        if not str(location.get(key, "")).strip():
            fail(f"{label} missing location.{key}")
    summary = str(record.get("summary", ""))
    if len(summary) < 12 or len(summary) > 280:
        fail(f"{label} summary length {len(summary)}")
    name = str(record.get("name", ""))
    if len(name) < 2 or len(name) > 80:
        fail(f"{label} name length")
    hours = str(record.get("hours", ""))
    if len(hours) < 2 or len(hours) > 80:
        fail(f"{label} hours length")
    offerings = record.get("offerings")
    if not isinstance(offerings, list) or len(offerings) > 6:
        fail(f"{label} offerings")
    publication = record.get("publication") or {}
    if exported:
        if publication.get("status") != "not-published" or publication.get("note") != EXPORT_NOTE:
            fail(f"{label} export publication")
        if record.get("profilePath") != "":
            fail(f"{label} export path must be empty")
    else:
        if publication.get("status") != "static-demo" or publication.get("note") != STATIC_NOTE:
            fail(f"{label} static publication")
        if record.get("profilePath") != f"/connect/{record.get('id')}":
            fail(f"{label} profilePath")
    blob = json.dumps(record)
    private_hits(label, blob)


def matches(record: dict, query: str, category: str, location: str) -> bool:
    if category != "all" and record["category"] != category:
        return False
    loc = record["location"]
    if location != "all" and location not in (loc["area"], loc["city"]):
        return False
    if query:
        blob = " ".join(
            [
                record["name"],
                record["category"],
                loc["area"],
                loc["city"],
                loc["province"],
                record["summary"],
                record["hours"],
                *record["offerings"],
            ]
        ).lower()
        if query not in blob:
            return False
    return True


def main() -> int:
    records = json.loads(DATA.read_text(encoding="utf-8"))
    if [item["id"] for item in records] != ["bright-steps-ecd", "sindis-bakery", "ubuntu-plumbing"]:
        fail("directory order or ids drifted")
    expected = {
        "bright-steps-ecd": ("Bright Steps ECD", "ECD Centre", "KwaMashu", "Durban"),
        "sindis-bakery": ("Sindi's Bakery", "Bakery", "Umlazi", "Durban"),
        "ubuntu-plumbing": ("Ubuntu Plumbing", "Plumbing", "Pietermaritzburg", "Pietermaritzburg"),
    }
    for record in records:
        check_record(record, exported=False)
        name, category, area, city = expected[record["id"]]
        if (record["name"], record["category"], record["location"]["area"], record["location"]["city"]) != (
            name,
            category,
            area,
            city,
        ):
            fail(f"{record['id']} identity mismatch")
        if record["location"]["province"] != "KwaZulu-Natal":
            fail(f"{record['id']} province")
        individual = json.loads((CONNECT / "data" / f"{record['id']}.json").read_text(encoding="utf-8"))
        if individual != record:
            fail(f"{record['id']} individual JSON drifted")
        page = (CONNECT / f"{record['id']}.html").read_text(encoding="utf-8")
        plain = html.unescape(page)
        for needle in (
            record["name"],
            "DEMO — FICTIONAL DATA ONLY",
            "DZ",
            "DigiZone",
            "4All",
            "Demo enquiry only",
            f"/connect/{record['id']}",
            "noindex,nofollow",
        ):
            if needle not in plain:
                fail(f"{record['id']} page missing {needle!r}")
        private_hits(record["id"] + ".html", plain)
        if "localStorage" in page:
            fail(f"{record['id']} page uses localStorage")

    directory = (CONNECT / "index.html").read_text(encoding="utf-8")
    capture = (CONNECT / "capture.html").read_text(encoding="utf-8")
    for page_name, page in (("directory", directory), ("capture", capture)):
        if "DEMO — FICTIONAL DATA ONLY" not in page or "does not publish" not in page.lower() and "not public" not in page.lower() and "not a public profile" not in page.lower():
            if "Exporting JSON is not public publication." not in page and "not a public profile" not in page:
                fail(f"{page_name} missing publication boundary")
        private_hits(page_name, page)
        if "localStorage" in page:
            fail(f"{page_name} uses localStorage")
    if "not a public profile" not in directory:
        fail("directory missing publication boundary")
    if "Exporting JSON is not public publication." not in capture:
        fail("capture missing publication boundary")
    for record in records:
        if f'{record["id"]}.html' not in directory:
            fail(f"directory does not link {record['id']}")

    script = (CONNECT / "assets" / "dz-connect.js").read_text(encoding="utf-8")
    if "localStorage" in script:
        fail("script uses localStorage")
    if EXPORT_NOTE not in script:
        fail("script missing export note")

    css = (CONNECT / "assets" / "dz-connect.css").read_text(encoding="utf-8")
    for token in ("#10192d", "#dafa74", "#f7f8f4", "#ff796b"):
        if token not in css:
            fail(f"css missing {token}")
    private_hits("css", css)

    cases = [
        ("geyser", "all", "all", ["ubuntu-plumbing"]),
        ("", "Bakery", "all", ["sindis-bakery"]),
        ("", "all", "Durban", ["bright-steps-ecd", "sindis-bakery"]),
        ("", "Plumbing", "Durban", []),
        ("", "all", "KwaMashu", ["bright-steps-ecd"]),
        ("", "ECD Centre", "Pietermaritzburg", []),
        ("sindi", "all", "all", ["sindis-bakery"]),
    ]
    for query, category, location, expected_ids in cases:
        found = [record["id"] for record in records if matches(record, query, category, location)]
        if found != expected_ids:
            fail(f"filter {query!r} {category} {location} -> {found} expected {expected_ids}")

    diff = subprocess.run(
        ["git", "diff", "--exit-code", "main", "--", *V01],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if diff.returncode != 0:
        fail("v0.1 files differ from main")

    if failures:
        print("FAIL")
        for item in failures:
            print("-", item)
        return 1
    print("PASS")
    print(f"records={len(records)} filter_cases={len(cases)} v0.1=unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
