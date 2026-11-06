# Pepkio Bio Unit Converter

Submit molarity, OD600, dilution, and dimensional unit-conversion jobs to the Pepkio Bio Unit Converter REST API from Python scripts and notebooks.

# What It Does

Bench and pipeline workflows need consistent answers when converting mass to molarity, OD600 to cells/mL, solving C₁V₁=C₂V₂, or translating ng/mL to nM—often across several disconnected calculators. Re-implementing MW lookup, species OD factors, and dilution algebra in every notebook is slow and error-prone.

This package calls the same Pepkio Tools engine as the hosted [Bio Unit Converter](https://www.pepkio.com/tools/bio-unit-converter) web calculator. Send manifest-defined inputs for one of four `mode` values (`molarity`, `od600`, `dilution`, `unit_convert`); receive structured `result`, optional `warnings`, and shareable run permalinks.

Programmatic runs require a network connection and a Pepkio API key. Calculator logic is hosted remotely; the client is not an offline conversion library.

# Features

- Four API modes: molarity (C = mass/MW/volume), od600 (cells/mL = OD × factor), dilution (solve any missing C₁V₁ term), unit_convert (dimensional pairs including ng/mL ↔ nM)
- Compound MW via `compound_id` or `molecular_weight_g_per_mol`
- Manifest examples: `bsa_molarity`, `ecoli_od`, `dilution_solve_v1`, `ng_ml_to_nM`, `dilution_solve_c2`, `bsa_compound_id`, and others
- Configuration via `PEPKIO_API_KEY` and `PEPKIO_API_BASE_URL`

# Installation

```bash
pip install pepkio-bio-unit-converter
```

Set an API key with **tools:run** scope before calling the API:

```bash
export PEPKIO_API_KEY="your-key"
```

Create a key in your [Pepkio account API keys](https://www.pepkio.com/account/api-keys) settings.

# Quick Example

```bash
curl -s -X POST https://tools.pepkio.com/api/tools/v1/tools/bio-unit-converter/run \
  -H "Authorization: Bearer $PEPKIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "mode": "od600",
      "od600": 0.5,
      "species_id": "e_coli_k12"
    }
  }'
```

Manifest (no API key required):

```bash
curl -s https://tools.pepkio.com/api/tools/v1/tools/bio-unit-converter/manifest
```

Python client API:

# Typical Use Cases

- Convert ng/mL antibody or protein stocks to nM for assay design
- Estimate *E. coli* K-12 cells/mL from OD600 in automated culture monitoring
- Solve stock volume for a 10 mM → 1 mM dilution in a fixed final volume
- Batch unit conversions in notebooks or CI without maintaining local conversion tables
- Chain results with `molarity-solution-calculator` or `serial-dilution-planner` workflows

# Scientific Background

Molarity follows C = mass / (MW × volume). OD600 cell density uses cells/mL = OD × organism factor. Dilutions obey C₁V₁ = C₂V₂ with one unknown solved algebraically. ng/mL to nM requires molecular weight. The API manifest documents supported unit strings and validation rules.

# Web Application

For researchers who prefer a graphical interface, an interactive [Bio Unit Converter](https://www.pepkio.com/tools/bio-unit-converter) is available in the browser.

The web interface adds searchable compound MW lookup, species-aware OD factors with uncertainty ranges, cross-tab chaining, copy-ready notebook records, shareable input links, and browser calculation history.

# Documentation and Resources

Source code and issue tracking: [github.com/pepkio/pepkio-bio-unit-converter](https://github.com/pepkio/pepkio-bio-unit-converter)

Web calculator: [pepkio.com/tools/bio-unit-converter](https://www.pepkio.com/tools/bio-unit-converter)

# About Pepkio

Pepkio develops software tools and provides bioinformatics analysis services for life science research. See [pepkio.com](https://www.pepkio.com/) for additional calculators and [analysis services](https://www.pepkio.com/cro).

# Keywords

bio unit converter, molarity API, OD600 cells per mL, C1V1C2V2 dilution, ng/mL to nM, mass concentration conversion, unit_convert mode, pepkio-bio-unit-converter, Python laboratory calculator, REST API dilution solver, E coli OD600 API, molecular weight compound_id, shareable calculation permalink, how to convert ng/mL to nM Python, solve dilution volume API, automate OD600 to cells/mL notebook, Pepkio Tools API client, laboratory concentration script, species custom OD factor, molarity od600 dilution unit_convert, bench prep automation without spreadsheet

A semantic, AI-native version of this document in the K2F format is available at https://k2f.dev (https://k2f.dev/v/de6157b63287945008a22ac66f435866e8bb9dd72900a38ef27bf7d7c8908060)
