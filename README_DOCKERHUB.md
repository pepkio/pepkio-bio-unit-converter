# Pepkio Bio Unit Converter

Container image for the Pepkio bio-unit-converter CLI—molarity, OD600, dilution, and unit conversion via the hosted API.

# What It Does

The image runs `pepkio-bio-unit-converter`, a client for the Pepkio Bio Unit Converter REST API. Submit manifest-defined inputs for molarity, OD600/cell density, dilution (C₁V₁=C₂V₂), or dimensional unit conversion; receive structured results, warnings, and shareable run permalinks.

Typical workflows include ng/mL to nM conversion for assay prep, OD600 to cells/mL for culture monitoring, bench dilution volume calculations, and scripted unit conversion in CI. Calculator logic runs on Pepkio servers; provide a network connection and API key for `run` commands.

# Features

- Four modes: `molarity`, `od600`, `dilution`, `unit_convert`
- Molarity from mass, volume, and MW; OD600 with `species_id` or `custom_factor`
- Dilution solver for any missing C₁, V₁, C₂, or V₂
- Unit conversion including ng/mL ↔ nM and cells/mL ↔ OD600
- Named manifest examples (`bsa_molarity`, `ecoli_od`, `dilution_solve_v1`, `ng_ml_to_nM`, etc.)
- Manifest inspection without an API key

# Quick Start

```bash
docker pull pepkio/bio-unit-converter:0.1.0
docker run --rm -e PEPKIO_API_KEY="your-key" pepkio/bio-unit-converter:0.1.0 \
  run --example dilution_solve_v1
```

Manifest only (no API key):

```bash
docker run --rm pepkio/bio-unit-converter:0.1.0 manifest --examples
```

Set `PEPKIO_API_BASE_URL` to override the API host (default: `https://tools.pepkio.com`). Create an API key with **tools:run** scope at https://www.pepkio.com/account/api-keys.

# Quick Example

```bash
docker run --rm -e PEPKIO_API_KEY="$PEPKIO_API_KEY" pepkio/bio-unit-converter:0.1.0 \
  run --example ng_ml_to_nM
```

# Typical Use Cases

- OD600 to cells/mL conversion in reproducible container environments
- Dilution volume calculations in CI or pipeline runners
- ng/mL to nM batch conversion for protein assay setup
- Manifest inspection in deployment smoke tests
- Fixed-environment workflow runners without local Python installs

# Scientific Background

Molarity: C = mass / (MW × volume). OD600: cells/mL = OD × factor. Dilution: C₁V₁ = C₂V₂. Unit conversion pairs require MW or OD factor as documented in the manifest.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/bio-unit-converter

The web UI adds searchable compound MW lookup, species-aware OD factors with uncertainty ranges, cross-tab chaining, copy-ready notebook records, shareable input links, and browser calculation history.

# Documentation and Resources

GitHub Repository (source and Dockerfile): https://github.com/pepkio/pepkio-bio-unit-converter

Web Application: https://www.pepkio.com/tools/bio-unit-converter

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).
