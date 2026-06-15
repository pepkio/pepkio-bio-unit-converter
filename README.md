# Pepkio Bio Unit Converter

Convert mass, molarity, OD600, and dilution volumes in one tabbed workspace—no switching calculators.

# Overview

Laboratory work routinely requires translating between mass concentration and molarity, converting OD600 readings to cell density, solving dilution problems, and moving between related unit systems. Researchers often rely on separate vendor calculators or spreadsheet formulas for each conversion type, which slows bench prep and increases transcription errors when chaining steps (for example, from an OD reading to a working concentration to a dilution volume).

The **Pepkio Bio Unit Converter** addresses this by combining four conversion modes—molarity, OD600/cell density, dilution (C₁V₁=C₂V₂), and dimensional unit conversion—in a single workspace. Enter concentrations, masses, volumes, or an OD600 reading in the units you already use; search common reagents and proteins to fill molecular weight automatically, or enter MW yourself. Results update as you type.

The hosted [Bio Unit Converter](https://www.pepkio.com/tools/bio-unit-converter) runs in the browser with no install or account. A Python client repository is maintained at [github.com/pepkio/pepkio-bio-unit-converter](https://github.com/pepkio/pepkio-bio-unit-converter) for programmatic access via the Pepkio Tools REST API.

Alternative search terms include laboratory unit converter, molarity calculator, OD600 to cells/mL converter, C1V1C2V2 dilution calculator, ng/mL to nM converter, mass-to-molarity conversion, and bioinformatics concentration math.

# Features

- **Four modes on one page:** Molarity, OD600 / Cells, Dilution, and Unit Converter tabs with live results
- **Molarity:** Compute molar and mass concentration from mass, volume, and molecular weight (C = mass / MW / volume)
- **OD600 / Cells:** Convert OD600 to cells/mL using species-specific factors; optional custom factor override; uncertainty ranges for supported organisms
- **Dilution:** Solve C₁V₁=C₂V₂ for any missing concentration or volume field
- **Unit Converter:** Dimensional conversions including ng/mL ↔ nM when molecular weight is provided, and cells/mL ↔ OD600 when an OD factor is supplied
- **Compound lookup:** Search common reagents and proteins to populate molecular weight (or enter MW manually)
- **Cross-tab chaining:** Send results to the next tab with one click instead of retyping
- **Notebook-ready output:** Copy a formatted calculation record for your ELN
- **Shareable links:** URLs that restore your inputs; reload past calculations from browser history
- **REST API:** Four `mode` values (`molarity`, `od600`, `dilution`, `unit_convert`) with manifest-defined inputs and structured JSON output

# Common Use Cases

- **Protein and small-molecule concentration math:** Convert between mass concentration (µg/mL, ng/mL) and molarity (nM, µM) for Western blot, ELISA, or stock preparation
- **Bacterial, yeast, and mammalian culture:** Convert OD600 readings to cells/mL with organism-aware factors and reported uncertainty ranges
- **Bench dilutions:** Solve how much stock to add when diluting 10 mM to 1 mM in a fixed final volume, or find the final concentration after a known transfer
- **Chained workflows:** Read OD → estimate cell density → compute working concentration → calculate dilution volume in one session via cross-tab chaining
- **Scripted pipelines:** Submit the same inputs through the Pepkio Tools API for notebooks, CI, or LIMS integration

# Why This Tool Exists

Spreadsheets and single-purpose vendor calculators (for example, separate molarity, OD600, or dilution tools) force researchers to switch contexts mid-prep and re-enter values manually. Many OD600 calculators apply a single generic factor and do not reflect strain-to-strain variation or report uncertainty. Chaining an OD reading to cell density to working concentration to dilution volume typically requires multiple disconnected steps.

The [Bio Unit Converter](https://www.pepkio.com/tools/bio-unit-converter) combines four conversion modes with live results, searchable compound MW lookup, species-aware OD factors, solve-any dilution, cross-tab chaining, local history, and share links—without installing software or creating an account. For powder mass, hydrate correction, or pipette-aware serial dilution protocols, Pepkio provides related tools (`molarity-solution-calculator`, `serial-dilution-planner`) that chain well with this converter.

# Installation

PyPI package:

# Quick Start

The Pepkio Tools API exposes `bio-unit-converter` with synchronous execution. Fetch the manifest for the current input schema and examples:

```bash
curl -s https://tools.pepkio.com/api/tools/v1/tools/bio-unit-converter/manifest
```

Run a molarity conversion (example `bsa_molarity` from the manifest):

```bash
curl -s -X POST https://tools.pepkio.com/api/tools/v1/tools/bio-unit-converter/run \
  -H "Authorization: Bearer $PEPKIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "mode": "molarity",
      "mass": 1,
      "mass_unit": "ug",
      "volume": 100,
      "volume_unit": "uL",
      "molecular_weight_g_per_mol": 66463,
      "output_molar_unit": "nM"
    }
  }'
```

Other manifest examples include `ecoli_od` (OD600 for *E. coli* K-12), `dilution_solve_v1` (solve stock volume), and `ng_ml_to_nM` (mass-to-molar unit conversion). Create an API key with **tools:run** scope at [pepkio.com/account/api-keys](https://www.pepkio.com/account/api-keys).

Python client (when published):

# Example Output

API responses include `run_id`, `status`, `result`, and `permalink`. The tool `result` object follows the manifest output schema:

| Field | Description |
| --- | --- |
| `mode` | Active mode: `molarity`, `od600`, `dilution`, or `unit_convert` |
| `result` | Mode-specific calculated values (structure defined in the manifest) |
| `warnings` | Optional array of caution messages |
| `chain` | Optional object for cross-tab chaining metadata |
| `error` | Error string when validation or calculation fails |

Representative manifest example inputs (verified):

| Example name | Mode | Key inputs |
| --- | --- | --- |
| `bsa_molarity` | molarity | 1 µg in 100 µL, MW 66463 g/mol → nM |
| `nacl_1M` | molarity | 58.44 g in 1 L, MW 58.44 g/mol → M |
| `ecoli_od` | od600 | OD600 0.5, `species_id` e_coli_k12 |
| `dilution_solve_v1` | dilution | 10 mM → 1 mM in 1 mL (solve v1) |
| `ng_ml_to_nM` | unit_convert | 100 ng/mL → nM, MW 11000 g/mol |
| `dilution_solve_c2` | dilution | 10 mM, 100 µL stock into 1 mL (solve c2) |

Exact numeric `result` payloads depend on the live calculator; inspect a completed run via the API or the web interface.

# Scientific Background

## Molarity

Molar concentration relates mass, molecular weight, and volume:

\[
C_{\text{molar}} = \frac{m_{\text{mass}}}{M_r \times V}
\]

where \(m_{\text{mass}}\) is solute mass, \(M_r\) is molecular weight (g/mol), and \(V\) is solution volume. Mass concentration and molarity interconvert when \(M_r\) is known.

## OD600 and cell density

Optical density at 600 nm (OD600) is commonly used to estimate microbial or cell culture density. A standard linear approximation is:

\[
\text{cells/mL} = \text{OD600} \times f
\]

where \(f\) is an organism-specific cells-per-OD factor (cells/mL per OD unit). Factors vary by species and strain; the web tool reports uncertainty ranges for supported organisms. A custom factor can be supplied when `species_id` is `custom`.

## Dilution (C₁V₁ = C₂V₂)

For diluting a stock solution:

\[
C_1 V_1 = C_2 V_2
\]

Leave one of \(C_1\), \(V_1\), \(C_2\), or \(V_2\) empty to solve for the unknown. Units must be consistent within each concentration pair and each volume pair.

## Mass ↔ molar unit conversion

Converting ng/mL to nM (or related pairs) requires molecular weight. The `unit_convert` mode handles dimensional conversions between manifest-defined unit pairs, including cells/mL ↔ OD600 when `od_factor` is provided.

# Frequently Asked Questions

**What is the Bio Unit Converter?**  
A Pepkio laboratory calculator that combines molarity, OD600/cell density, dilution, and unit conversion in one tabbed workspace, available at [pepkio.com/tools/bio-unit-converter](https://www.pepkio.com/tools/bio-unit-converter).

**How do I convert ng/mL to nM?**  
Use the Unit Converter tab (or API `mode: unit_convert`) with `from_unit` ng_per_mL, `to_unit` nM, and the compound molecular weight in g/mol.

**What is the formula for molarity from mass?**  
Molarity = mass / (molecular weight × volume), with consistent SI-compatible units.

**How do I convert OD600 to cells per mL?**  
Use the OD600 / Cells tab or API `mode: od600` with your OD reading and a `species_id` (for example `e_coli_k12`) or a `custom_factor`.

**What is C₁V₁ = C₂V₂?**  
The dilution equation relating stock concentration \(C_1\), stock volume \(V_1\), final concentration \(C_2\), and final volume \(V_2\). Leave one variable empty to solve for it.

**How do I dilute 10 mM stock to 1 mM in 1 mL?**  
Use Dilution mode with c1=10 mM, c2=1 mM, v2=1 mL, and leave v1 empty (manifest example `dilution_solve_v1`).

**Can I look up molecular weight for BSA or other proteins?**  
The web interface supports searching common reagents and proteins to fill MW automatically. The API accepts `compound_id` (for example `bsa`) or `molecular_weight_g_per_mol`.

**Does the tool support custom OD600 factors?**  
Yes. Set `species_id` to `custom` and provide `custom_factor` (cells/mL per OD unit) in the API or the web UI.

**What mass and volume units are supported?**  
Manifest-documented mass units: ug, mg, g, kg. Volume units: uL, mL, L. Molar output units include M, mM, uM, nM.

**Can I chain OD reading to dilution without retyping?**  
The web application supports one-click cross-tab chaining. The API returns optional `chain` metadata for related workflows.

**Is there a Python package?**  
Repository: [github.com/pepkio/pepkio-bio-unit-converter](https://github.com/pepkio/pepkio-bio-unit-converter). PyPI publication status:

**Do I need an account for the web calculator?**  
No install or account is required for the browser tool.

**How do I share a calculation with a colleague?**  
The web version generates shareable links that restore your inputs.

**What related Pepkio tools should I use for powder or serial dilution?**  
For powder mass, hydrate, or serial prep use `molarity-solution-calculator`; for pipette-aware serial dilution use `serial-dilution-planner`. Both chain well with bio-unit-converter per the API manifest.

**How do I authenticate API requests?**  
Send `Authorization: Bearer <PEPKIO_API_KEY>` with a key that has **tools:run** scope.

**What is the difference between molarity mode and unit_convert mode?**  
`molarity` computes concentration from mass, volume, and MW. `unit_convert` transforms between compatible unit pairs (for example ng/mL ↔ nM) given a value and MW or OD factor.

**Can I convert cells/mL back to OD600?**  
Yes, via `unit_convert` with `from_unit` cells_per_mL, `to_unit` od600, and `od_factor` (manifest example `cells_to_od`).

**Where is the API manifest?**  
`GET https://tools.pepkio.com/api/tools/v1/tools/bio-unit-converter/manifest`

**Does the web tool store my data on a server?**  
Browser history and share links are described on the product page; API runs return a `permalink` for completed calculations.

# Web Application

The [Bio Unit Converter](https://www.pepkio.com/tools/bio-unit-converter) web version provides an interactive tabbed interface, searchable compound MW lookup, species-aware OD600 factors with uncertainty ranges, cross-tab result chaining, copy-ready notebook records, shareable links that restore inputs, and reload of past calculations from browser history—without installing software.

Web Application: https://www.pepkio.com/tools/bio-unit-converter

# Related Resources

GitHub Repository: https://github.com/pepkio/pepkio-bio-unit-converter

PyPI Package:

Web Application: https://www.pepkio.com/tools/bio-unit-converter

API manifest: https://tools.pepkio.com/api/tools/v1/tools/bio-unit-converter/manifest

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

# Citation

# License

# Keywords

bio unit converter, Pepkio Bio Unit Converter, laboratory unit converter, molarity calculator, mass to molarity, ng/mL to nM, µg/mL to µM, protein concentration calculator, OD600 to cells/mL, OD600 cell density, E. coli OD600 factor, yeast OD600 conversion, C1V1C2V2, dilution calculator, stock dilution volume, serial dilution concentration, molecular weight lookup, BSA molarity, mass concentration conversion, molar concentration conversion, cells per mL calculator, custom OD600 factor, laboratory concentration math, solution prep calculator, Western blot concentration, ELISA antibody dilution, cell culture OD reading, REST API unit conversion, pepkio-bio-unit-converter, bioinformatics calculator, bench calculator, shareable dilution link, cross-tab unit chaining, how to convert ng/mL to nM for protein, OD600 to cells per mL E coli K12, calculate molarity from mass and volume, solve C1V1C2V2 for unknown volume, convert micrograms per mL to nanomolar, bacterial culture density from OD600, dilute 10 mM to 1 mM how much stock, mass molarity volume formula lab, species specific OD600 uncertainty range, chain OD to concentration to dilution, API molarity od600 dilution unit_convert, laboratory ELN calculation record copy, no account web molarity tool, molecular weight compound search reagent
