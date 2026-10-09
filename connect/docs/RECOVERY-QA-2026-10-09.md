# DigiZone Connect v0.2 — Recovery and QA

**Date:** 2026-10-09

**Input:** User-uploaded ZIP of untracked Cursor `connect/` tree. Branch as reported by Human: `work/digizone-connect-v0.2`. No Git commit/push/deploy performed in this review.

## Evidence and method

- Zip safety: 14 files, all extraction paths within target directory; originals preserved in this document bundle.
- JSON: 3 records pass Draft 2020-12 JSON Schema using `jsonschema`; individual JSON equals records in `organisations.json`.
- JavaScript: `node --check connect/assets/dz-connect.js` passed.
- Generator: `python connect/tools/render_pages.py` executed on disposable extracted copy. Generated content matches the ZIP originals **after line-ending normalization**; output files were not content-changed.
- Chromium: 39/39 embedded-source interaction tests passed across 320, 390 and 1280 widths (3 directory/profile/filters, invalid/valid capture JSON export, overflow and console-page errors). No detected JavaScript runtime exceptions during those paths. Browser was loaded via `set_content` with inline CSS and JS because the test runtime blocks navigation to `localhost` and `file://`.
- Visual: static screenshot at 390px visually checked; DZ↗ nameplate, lime/navy and card layout consistent with v0.1.

## Precisely NOT verified

- HTTP200 or live Vercel `connect/` URLs, HTTP redirects, real page navigation via link clicks, and clipboard/web share APIs on deployed origin.
- The `check_demo.py` repository-baseline comparison (`git diff main -- v0.1 files`) because supplied archive contains only `connect/`, not main history and original root files.
- Imvelo/DigiZone domain ownership, DNS and hosting readiness.
- UX/reliability with real people and public data collection.

## Specific deployment/manual checks

1. In the actual demo repo `work/digizone-connect-v0.2`, run `git status --short` and inspect the untracked `connect/` tree; do not clean it.
2. Run `python connect/tools/render_pages.py` only if intentional, inspect `git status`, then `python connect/tools/check_demo.py` in the real repo to exercise its main-branch baseline assertion.
3. Publish only a controlled fictional preview via a separate explicit Human approval.
4. Test `/connect/`, `/connect/bright-steps-ecd`, `/connect/sindis-bakery`, `/connect/ubuntu-plumbing`, `/connect/capture` in a fresh mobile/desktop browser and check each HTTP status; actual path behavior depends on Vercel config.
5. Test on-page profile share/copy, navigation and forms after deployment, then update this report with real observations.

**Conclusion:** Working static v0.2 simulation candidate; technically coherent, partially browser QA-verified. Not yet a publicly verified shareable Connect product. Two proposed `.org.za` domains unchanged.
