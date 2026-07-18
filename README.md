# Vulnerability Explorer

**Live tool:** https://arashnassirpour.com/hazus/

An interactive browser for catastrophe-model vulnerability and fragility functions, centred on FEMA Hazus 6.1. It turns the source datasets into searchable, comparable charts for flood, wind, earthquake, and critical-infrastructure analysis.

## What it provides

- **Flood vulnerability:** depth-damage functions by occupancy and building characteristics.
- **Wind vulnerability:** damage and loss functions from the bundled Hazus wind dataset.
- **Earthquake fragility:** building-type fragility relationships and median PGA parameters.
- **Critical infrastructure:** fragility curves organised by infrastructure system.
- Interactive filtering, curve comparison, charting, and data export.
- A generated static site that runs entirely in the browser after publication.

## Data sources

The repository includes the local source files used for the published Hazus views:

- FEMA Hazus 6.1 flood damage functions.
- FEMA Hazus 6.1 wind functions, with data processing informed by the OS-Climate `physrisk` implementation.
- Static earthquake building-type and fragility data represented in `data_earthquake.py`.
- Critical-infrastructure data handled by `data_ci.py`.

FEMA Hazus data is public-domain source material. The surrounding extraction, validation, presentation, and application code is licensed separately under AGPL-3.0-only.

## Accuracy and validation

The loaders do not silently replace missing or invalid cells with zero. Shared validation in `data_validate.py` checks:

- Missing, textual, negative, and out-of-range values.
- Strictly increasing hazard-intensity axes.
- Damage-curve array consistency.
- Fragility probability monotonicity and damage-state ordering.
- Earthquake median-PGA ordering.

Invalid curves are excluded and reported with their source, curve identifier, sheet or column, and reason. The bundled flood workbook currently contains incomplete cells in a small number of curves; those curves are deliberately excluded rather than fabricated or interpolated.

This project is an exploration and research aid, not a substitute for the Hazus technical manuals, local calibration, engineering judgement, or project-specific catastrophe-model validation. Hazus is calibrated primarily for United States construction and infrastructure.

## Run locally

Requirements:

- Python 3.12 or later
- `pandas`
- `openpyxl`

```bash
python -m pip install -r requirements.txt
python run.py
```

The build generates:

- `index.html` — landing and explanatory page
- `HAZUS_Dashboard.html` — interactive vulnerability explorer

When run outside CI, the generated site opens automatically in the default browser.

## Tests

Run the data-validation suite:

```bash
python test_data_validation.py
```

Run the focused Hazus build check:

```bash
python run_test.py
```

The validation suite covers unit cases and integration checks against the bundled flood and wind datasets without requiring pytest.

## Repository structure

| File | Responsibility |
|---|---|
| `run.py` | Loads data and builds the published pages |
| `html_builder.py` | Generates the interactive dashboard |
| `page_explainer.py` | Generates the landing/about page |
| `data_flood.py` | Flood vulnerability extraction |
| `data_wind.py` | Wind vulnerability extraction |
| `data_earthquake.py` | Earthquake building and fragility data |
| `data_ci.py` | Critical-infrastructure fragility extraction |
| `data_validate.py` | Shared validation and error reporting |
| `test_data_validation.py` | Validation and integration test suite |
| `data_sources/` | Bundled source workbooks and caches |

## Deployment

GitHub Actions rebuilds the static pages from `main` and deploys them to GitHub Pages. The published project is served under the main site’s custom domain at:

https://arashnassirpour.com/hazus/

## Licence

Copyright (C) 2026 Arash Nassirpour.

The application code is licensed under the GNU Affero General Public License v3.0 only (`AGPL-3.0-only`). See [LICENSE](LICENSE).
