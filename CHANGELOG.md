# Changelog

All notable changes to this project will be documented in this file.

The format is intentionally simple and optimized for release notes and repository readers.

## [Unreleased]

### Changed

- **License changed from PolyForm Noncommercial 1.0.0 (plus non-commercial additional terms) to Apache License 2.0.**
  Commercial use is now permitted; derivatives no longer have to be published as source. Added `NOTICE`
  recording the change; removed `LICENSE.md` and `ADDITIONAL_TERMS.md`, replaced by `LICENSE`.

### Added
- Tiered detection routing: zero-dependency rule-based review by default, automatic escalation to image/patent data sources when credentials are present.
- `scripts/detect_capabilities.py` — credential probe that reports availability only and never prints secret values.
- `references/escalation.md` — triage table, endpoint/pricing reference, and discipline for paid IP data channels.
- Mandatory detection-coverage statement in every report, stating what was and was not checked.

- HTML companion report workflow for full compliance reviews.
- Standard-library `scripts/render_html_report.py` renderer with source-image embedding and numbered hotspot annotations.
- HTML report data template for image-based IP, trademark, and listing-scope risk reviews.

### Changed

- Updated install URLs and default installer repo to `WaytoAIC/ecommerce-content-compliance-review`.

## [v1.0.0] - 2026-03-27

First public release.

### Added

- Initial `ecommerce-content-compliance-review` skill
- Multi-dimensional compliance review workflow for ecommerce content
- Built-in references for advertising law, IP, marketplace rules, and cross-border regulations
- Report template, risk checklist, and installer for Codex and OpenClaw
- Bilingual README and source-available license files
