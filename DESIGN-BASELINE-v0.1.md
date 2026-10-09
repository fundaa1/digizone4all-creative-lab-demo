# DigiZone4All / DigiZone — Design baseline v0.1

**Status:** Founder-approved visual reference  
**Approval date:** 2026-10-09  
**Approver:** Sphe  
**Source:** `fundaa1/digizone4all-creative-lab-demo`, `main` at [`9aea10c7a3c0fdcecde8c23a791d09868998ebd1`](https://github.com/fundaa1/digizone4all-creative-lab-demo/commit/9aea10c7a3c0fdcecde8c23a791d09868998ebd1).

## Approval and scope

Sphe explicitly approved the DigiZone4All / DigiZone v0.1 visual direction on 2026-10-09: brand appearance, nameplate, colour palette and overall design principles. This records Founder-side approval of a design reference only. It does not establish trademark clearance, company-wide IGV adoption, IP transfer, or production/publication approval for new deployments.

Approval provenance: Sphe's feedback in “Identify IGV Structure” (conversation `6ac8b863-fc94-83e9-acc2-bcd7ab7d6b5b`), explicitly confirmed and scoped by Sphe's instruction to record this baseline on 2026-10-09.

## Actual source palette

All four HTML pages carry the same inline stylesheet. These are its declared colour tokens; declaration alone does not mean every token is visibly used.

| Token | Value | Source role |
| --- | --- | --- |
| navy | #10192d | Header, hero, primary buttons, mark text |
| navy2 | #1d2c42 | Declared secondary navy |
| ink | #182438 | Body text |
| muted | #5a6979 | Supporting text |
| paper | #f7f8f4 | Page background |
| white | #ffffff | Panels and light text |
| line | #e1e7e7 | Borders and dividers |
| lime | #dafa74 | Nameplate suffix, badge, emphasis, active navigation |
| coral | #ff796b | Accent buttons and quote rule |
| cyan | #a3eef5 | Connected home-card accent |
| yellow | #ffdc7d | Capable home-card accent and selected rating |
| shade | #edf4f1 | Declared soft surface |

Supporting treatments include the profile banner gradient `125deg, #24374f → #1b5b62`, pale green/grey surfaces, teal progress `#329b92`, focus outline `#297c8b`, header text `#f5fff7`, hero supporting text `#d5dde3`, and translucent white hero decoration. The shared panel shadow is `0 12px 35px rgba(26,48,62,.09)`. Exact secondary colours remain in the pinned source stylesheet.

## Typography and nameplate

- Body: `16px/1.55 Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`. Inter is named but is not bundled or downloaded; the available system fallback determines rendering.
- Large hero headings: `clamp(39px,5.4vw,72px)`, line-height 1.04, tracking -0.058em; section headings 27px. Labels use small uppercase text with wider tracking; buttons and navigation use bold weights.
- Actual nameplate: **DZ↗ DigiZone4All**, with “4All” in lime and “DigiZone” inheriting the light header colour. The wordmark is 21px, weight 850, tracking -0.04em, with a 10px gap.
- Existing mark: text “DZ” plus an upward-right arrow, navy on a lime badge, 11px corner radius, 5px 10px padding, weight 900, rotated -3 degrees. It is HTML/CSS text, not a separate image or SVG logo. No new logo is introduced. “DigiZone” is included in the approval scope; the implemented nameplate remains DigiZone4All.

## Layout and principles to preserve

- Shared navy header/hero, lime emphasis, warm off-white canvas, white rounded cards, restrained borders and soft shadows.
- Centred 1180px container with 22px side padding; 15px padding below 540px.
- Home: three demo cards with lime/cyan/yellow symbol tiles. Working pages: two-column form/preview panels, profile banner and directory, feedback tabs/ratings/stats/progress/quotes, and a CV paper preview.
- Panels: 19px radius, 23px padding; buttons/inputs: 11px radius. Pill navigation, chips and metadata reinforce a consistent component language.
- Responsive rules at 850px and 540px stack main grids, reduce padding and wrap the header/profile content. Final small-screen hero rule is `clamp(30px,10vw,38px)`. Navigation and inputs retain 44px minimum heights.
- Preserve clear hierarchy, generous spacing, readable supporting text, visible focus indicators, direct actions and the shared nameplate across all demos.
- Preserve prominent DEMO/fictional-data notices and the existing “Visible. Connected. Capable.” / “People First. Technology Second.” framing.

## Change control

Preserve this v0.1 reference. Visual changes require human review by Sphe before replacing the approved baseline. Incremental improvements may be proposed alongside it with a clear comparison and rationale; proposals do not supersede approval. An accepted revision should receive its own versioned baseline and source commit.

This documentation addition changes no HTML, styling, interactions or deployment configuration and authorises no new deployment.
