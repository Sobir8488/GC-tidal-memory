# Data dictionary

## parent_phase_space_registry.csv
One row per parent-sample cluster. Contains observational phase-space inputs,
uncertainties, Galactocentric Cartesian states, and derived `R_GC_kpc`.

## confirmatory_sample.csv
Twelve confirmatory clusters. `cluster_key` is the canonical science-product
name; `cluster_key_registry` preserves the exact parent-registry spelling.
`stratum` is the frozen S1-S4 design stratum.

## lyapunov_configurations.csv
Ninety-six final configurations: 12 clusters x 2 Galactic potentials x 2
initial deviation directions x 2 tolerance levels. `N_L_6Gyr` is the
six-Gyr dimensionless e-folding count.

## lyapunov_group_summary.csv
Twenty-four cluster-potential rows. Contains minimum, median, maximum and
max/min spread of `N_L`, median finite-time exponent, and median Lyapunov time.

## functional_state_by_cluster_potential.csv
Twenty-four cluster-potential functional classifications. These labels are
independent of the Lyapunov classification.

## primary_endpoint_rows.csv
Primary Irrgang13III endpoint rows from the frozen endpoint synthesis.

## discovery_functional_horizon.csv
Pass/fail status for primary, distributional, and timing-sensitive diagnostic
lanes across the six discovery look-back windows.

## observational_uncertainty_confirmatory_sample.csv
Fractional input-level uncertainties used to quantify the unpropagated
observational covariance limitation.

## mcmillan17_discovery_failure_modes.csv
Discovery-only scalar convergence diagnostics. This table is not a causal
explanation for all 12 confirmatory McMillan17 endpoints.
