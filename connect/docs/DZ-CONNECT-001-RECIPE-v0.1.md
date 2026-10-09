# DZ-CONNECT-001 — Digital Presence Generation / Working Recipe v0.1

**Date:** 2026-10-09
**Status:** Technical working pattern demonstrated in a bounded fictional browser simulation. **Not proven in live community use, not accepted as an IGV organisational capability.**
**Human design input:** Founder-approved DigiZone4All v0.1 look. Source record: `fundaa1/digizone4all-creative-lab-demo`, branch `docs/design-baseline-v0.1`, commit `2a16f65`.

## Problem and outcome

**Problem:** Small organisations can struggle to create clear, consistent and easily shared digital presences. Bespoke sites can require disproportionate setup, asset collection and manual revision.

**Desired outcome:** From basic validated organisational information, produce consistent lightweight profiles and a searchable directory with independently shareable URLs.

## Simulation records

| ID | Fictional organisation | Category | Location |
|---|---|---|---|
| `bright-steps-ecd` | Bright Steps ECD | ECD Centre | KwaMashu, Durban |
| `sindis-bakery` | Sindi's Bakery | Bakery | Umlazi, Durban |
| `ubuntu-plumbing` | Ubuntu Plumbing | Plumbing | Pietermaritzburg |

Names, descriptions, operating hours and all offerings are simulated; no direct contacts or beneficiary details.

## Data contract / inputs

`connect/data/organisation.schema.json` defines schema version `0.2`. Core fields: `id`, `name`, `category`, `location.{area,city,province}`, `summary`, `hours`, `offerings[]`, `contact.label`, `fictional`, `publication.{status,note}`, `profilePath`, `schemaVersion`.

- Categories limited in this simulation to ECD Centre, Bakery and Plumbing.
- No real contact details accepted or published; label is `Demo enquiry only`.
- `fictional` must be true.
- Browser-exported records have `publication.status=not-published` and `profilePath=''`.
- Records included in the static demo are explicitly marked `static-demo`; this is **not** evidence of real-world publication.

## Recipe

1. **Capture:** Input organisation name, category, area/city/province, summary, hours and up to six offerings via `connect/capture.html`.
2. **Validate:** Check required fields, lengths, supported category, simulation acknowledgements and basic patterns for phones/emails/identity numbers; create a slug. These checks are only bounded demo safeguards, not complete personal-information screening.
3. **Export:** Produce a JSON record on the visitor's device. This **does not add a directory listing** or publish anything.
4. **Review for static inclusion:** Human reviews the fictional data and places it in `connect/data/organisations.json` with intentional `static-demo` status and the correct profile path.
5. **Generate:** `python connect/tools/render_pages.py` reads the static records and writes `connect/index.html`, three profile pages and their individual JSON records. This command mutates generated files; run in a controlled checkout and inspect changes.
6. **Verify:** Validate JSON against schema, check page content, search/category/location filtering, direct profile opens, export behaviour, responsive layout, copy/share and no private information.
7. **Share/discover after deployment:** Only after an approved demo deployment, test publicly accessible profile URLs from a fresh device and search each profile from the directory.

## Reusable components discovered

- One JSON schema and data array for multiple industries.
- One page generator and shared profile template.
- One static directory with text/category/location filters.
- One capture-to-validated-JSON export interface.
- Reused DZ↗ nameplate, navy/lime/coral design language and responsive components.

## Recorded evidence, 9 October 2026

- Three sample JSON records: schema-valid using Python `jsonschema`; individual records equal array entries.
- JavaScript syntax: `node --check` passed.
- Browser simulation: 39 checks passed at widths 320, 390 and 1280. Includes directory listing, filters, profile rendering, absence of horizontal overflow, capture invalid state, valid JSON export and JS runtime errors.
- Generated HTML/individual JSON compared with recovered files: semantically identical after CRLF/LF normalization.
- Visual review: 390px directory screenshot reflects v0.1 approved style.

**Testing boundary:** Chromium interactions were verified using embedded local HTML/CSS/JS because this environment blocked navigation to localhost/file URLs. That is not a true end-to-end HTTP/Vercel test. Share/copy workflows and deployed deep links still need public verification. The ZIP alone cannot verify the repository's `main` baseline check in `check_demo.py`.

## Effort and cost

Local salvage time and original Cursor execution time are not a reliable per-profile build-cost estimate. User reported a failed ~30-minute Cursor run; that does not establish end-to-end production throughput. No external API consumption in this recovered static simulation has been verified. Future repeatability and maintenance economics are **unknown**.

## Not yet demonstrated

Real onboarding, real participant permission, data persistence, edit approvals, communications, third-party sharing, search-engine discovery, public HTTP status, DNS control, durability/hosting costs, actual referrals/sales/learning outcomes, broader capability register acceptance.

## Next evidence gate

Deploy the three fictional profiles to an isolated preview and verify directory + independently opened HTTP paths with 200 status on mobile and desktop. If those tests pass, classify as **verified static demo**, not a live operational capability.
