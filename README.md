# GC tidal-memory reproducibility package v1.0.0

This archive contains the curated data products, selected source authorities,
publication figures, and lightweight post-processing code used to reproduce the
main numerical summaries for the globular-cluster tidal-memory analysis.

## Important scope

The manuscript is intentionally **not included** in this archive. Journal source
files, manuscript PDFs, bibliography build products, and journal class/style
files are excluded.

The package does not re-run orbit integrations, tidal-tensor evaluations, or
Lyapunov calculations. Instead it preserves the authoritative final tables used
for reporting and plotting, together with source-provenance hashes.

## Contents

- `data/parent_phase_space_registry.csv` - 165-cluster observational and
  Galactocentric registry.
- `data/confirmatory_sample.csv` - 12-cluster confirmatory sample with strata,
  phase-space coordinates, and uncertainty summaries.
- `data/lyapunov_configurations.csv` - all 96 final Lyapunov configurations.
- `data/lyapunov_group_summary.csv` - 24 cluster-potential group summaries.
- `data/functional_state_by_cluster_potential.csv` - 24 final functional-state
  classifications.
- `data/primary_endpoint_rows.csv` - Irrgang13III primary-endpoint rows.
- `data/discovery_functional_horizon.csv` - discovery-stage pass/fail grid over
  six look-back windows.
- `data/observational_uncertainty_confirmatory_sample.csv` - finite input-level
  distance, proper-motion, and radial-velocity uncertainty metrics.
- `data/mcmillan17_discovery_failure_modes.csv` - discovery-stage scalar
  convergence diagnostic for McMillan17.
- `data/observable_draw_bank_165x1024.npz` - existing 1024-draw observable bank;
  these draws were not propagated through the confirmatory calculation.
- `figures/` - vector PDF publication figures and 300-dpi PNG previews for the
  two phase-space panels.
- `source_artifacts/` - selected machine-readable authority/source files from
  which the curated tables were derived.
- `code/prepare_curated_data.py` - reconstructs curated CSV products from the
  packaged source artifacts.
- `code/make_phase_space_figures.py` - regenerates the enhanced phase-space
  panels.
- `code/verify_checksums.py` - verifies the archive manifest.
- `metadata/source_provenance.csv` - source paths, roles, and SHA-256 hashes.
- `metadata/SCOPE_AND_LIMITATIONS.md` - claim boundaries and open tests.
- `metadata/EXCLUDED_INPUTS.md` - deliberately omitted files/namespaces.

## Quick validation

From the unpacked archive:

```bash
python code/verify_checksums.py
```

To reconstruct curated CSV products from the packaged source artifacts:

```bash
python code/prepare_curated_data.py
```

To regenerate the two phase-space panels:

```bash
python code/make_phase_space_figures.py
```

## Scientific claim boundaries

The archive supports the following tested-set statements:

- all 24 tested cluster-potential groups meet the frozen robust-material-chaos
  criterion;
- all 12 Irrgang13III confirmatory endpoints have full functional stability;
- all 12 McMillan17 confirmatory endpoints remain functionally unresolved under
  the same frozen policy;
- the 24/24 chaos count is descriptive of the prespecified test matrix and is
  not a population-prevalence estimate;
- no McMillan17 combined endpoint is defined;
- the chaos label does not rescue a failed functional-convergence result.

Observational covariance is quantified and an existing draw bank is included,
but it was not propagated through the complete confirmatory orbit/tensor/
Lyapunov calculation.

## Zenodo deposition

This directory is prepared for deposition as a Zenodo dataset. Metadata are
provided in `.zenodo.json` and `CITATION.cff`. No DOI is hard-coded: Zenodo
assigns the DOI when the record is deposited/published.

## Licensing

- Code: MIT License (`licenses/LICENSE_CODE_MIT.txt`).
- Curated data and figures: CC BY 4.0 (`licenses/LICENSE_DATA_FIGURES_CC_BY_4_0.txt`).
