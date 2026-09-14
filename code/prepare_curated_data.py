#!/usr/bin/env python3
"""Rebuild curated CSV tables from packaged authority/source artifacts.

This script performs post-processing only. It does not integrate orbits,
evaluate tidal tensors, or compute Lyapunov exponents.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source_artifacts"
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

phase = pd.read_csv(SRC / "STAGE2A1_FROZEN_PHASESPACE_SOURCE_v0_7_1.csv")
state = pd.read_csv(SRC / "stage1c2_initial_state_registry.csv")
parent = phase.merge(state, on="cluster_key", how="inner", validate="one_to_one")
parent["R_GC_kpc"] = np.sqrt(parent["X_kpc"]**2 + parent["Y_kpc"]**2)
parent.to_csv(DATA / "parent_phase_space_registry.csv", index=False)

matrix = json.loads((SRC / "CLEANROOM_T6_CHAOS_REPLICATION_MATRIX_v1_0_0.json").read_text(encoding="utf-8-sig"))
chaos = json.loads((SRC / "t6_v1_0_6_96row_chaos_classification_results_v1_0_0.json").read_text(encoding="utf-8-sig"))
func = json.loads((SRC / "t6_v1_0_6_endpoint_preflight_functional_grouping_false_gate_forensics_v1_0_0.json").read_text(encoding="utf-8-sig"))
endpoint = json.loads((SRC / "t6_v1_0_6_primary_endpoint_synthesis_results_v1_0_0.json").read_text(encoding="utf-8-sig"))
horizon = json.loads((SRC / "cleanroom_t5_tidal_functional_memory_horizons.json").read_text(encoding="utf-8-sig"))

strata = {r["cluster"]: r["stratum"] for r in matrix["rows"]}
confirm_names = list(dict.fromkeys(r["cluster"] for r in matrix["rows"]))
registry_to_canonical = {"ESO 456-SC29": "ESO 456 SC29"}

tmp = parent.copy()
tmp["canonical_cluster_key"] = tmp["cluster_key"].replace(registry_to_canonical)
confirm = tmp[tmp["canonical_cluster_key"].isin(confirm_names)].copy()
confirm["cluster_key_registry"] = confirm["cluster_key"]
confirm["cluster_key"] = confirm["canonical_cluster_key"]
confirm.drop(columns=["canonical_cluster_key"], inplace=True)
confirm["stratum"] = confirm["cluster_key"].map(strata)

pmra = confirm["pmra_masyr"].to_numpy(float)
pmdec = confirm["pmdec_masyr"].to_numpy(float)
sra = confirm["pmra_sigma_masyr"].to_numpy(float)
sdec = confirm["pmdec_sigma_masyr"].to_numpy(float)
corr = confirm["pmra_pmdec_corr"].to_numpy(float)
cov = corr * sra * sdec
pm2 = pmra**2 + pmdec**2
num = pmra**2*sra**2 + pmdec**2*sdec**2 + 2*pmra*pmdec*cov
confirm["pm_vector_frac_sigma"] = np.where(pm2 > 0, np.sqrt(np.clip(num,0,None))/pm2, np.nan)
confirm["vlos_abs_frac_sigma"] = np.where(
    np.abs(confirm["vlos_kms"]) > 0,
    confirm["vlos_sigma_kms"] / np.abs(confirm["vlos_kms"]), np.nan)

confirm_cols = [
    "cluster_key","cluster_key_registry","stratum","ra_deg","dec_deg",
    "distance_kpc","distance_sigma_kpc","distance_frac_sigma","pmra_masyr",
    "pmdec_masyr","pmra_sigma_masyr","pmdec_sigma_masyr","pmra_pmdec_corr",
    "pm_vector_frac_sigma","vlos_kms","vlos_sigma_kms","vlos_abs_frac_sigma",
    "X_kpc","Y_kpc","Z_kpc","R_GC_kpc","U_kms","V_kms","W_kms"]
confirm = confirm[confirm_cols].sort_values(["stratum","cluster_key"])
if len(confirm) != 12:
    raise RuntimeError(f"Expected 12 confirmatory clusters, found {len(confirm)}")
confirm.to_csv(DATA / "confirmatory_sample.csv", index=False)
confirm[["cluster_key","cluster_key_registry","stratum","distance_frac_sigma",
         "pm_vector_frac_sigma","vlos_abs_frac_sigma"]].to_csv(
    DATA / "observational_uncertainty_confirmatory_sample.csv", index=False)

lyap = pd.DataFrame(chaos["rows"]).rename(columns={
    "cluster":"cluster_key", "final_lambda_Gyr_minus1":"lambda_6Gyr_Gyr_minus1"})
lyap["stratum"] = lyap["cluster_key"].map(strata)
lyap = lyap[["chaos_index","cluster_key","stratum","potential","direction_id",
             "tolerance_level","lambda_6Gyr_Gyr_minus1","N_L_6Gyr"]].sort_values("chaos_index")
lyap.to_csv(DATA / "lyapunov_configurations.csv", index=False)

rows=[]
for g in chaos["groups"]:
    vals=np.array([r["N_L_6Gyr"] for r in g["rows"]],float)
    lams=np.array([r["final_lambda_Gyr_minus1"] for r in g["rows"]],float)
    med_l=float(np.median(lams))
    rows.append({
        "cluster_key":g["cluster"],"stratum":strata[g["cluster"]],
        "potential":g["potential"],"chaos_class":g["chaos_class"],
        "N_L_min":float(vals.min()),"N_L_median":float(np.median(vals)),
        "N_L_max":float(vals.max()),"N_L_max_over_min":float(vals.max()/vals.min()),
        "lambda_median_Gyr_minus1":med_l,"tau_L_median_Gyr":float(1.0/med_l)})
pd.DataFrame(rows).sort_values(["potential","stratum","cluster_key"]).to_csv(
    DATA / "lyapunov_group_summary.csv", index=False)

irr = func["decision"]["Irrgang13III_functional_class_by_cluster"]
mcm = {k:v["McMillan17"] for k,v in func["details"]["clusters_with_potential_dependent_functional_class"].items()}
frows=[]
for c in sorted(irr):
    frows += [
        {"cluster_key":c,"stratum":strata[c],"potential":"Irrgang13III","functional_state":irr[c]},
        {"cluster_key":c,"stratum":strata[c],"potential":"McMillan17","functional_state":mcm[c]}]
pd.DataFrame(frows).to_csv(DATA / "functional_state_by_cluster_potential.csv", index=False)

edf = pd.DataFrame(endpoint["cluster_endpoints"]).rename(columns={"cluster":"cluster_key"})
edf["stratum"] = edf["cluster_key"].map(strata)
edf.to_csv(DATA / "primary_endpoint_rows.csv", index=False)

hrows=[]
for potential, d in horizon["potentials"].items():
    for lane,key in (("primary","primary_window_PASS"),
                     ("distribution","distribution_window_PASS"),
                     ("TV_diagnostic","TV_tide_window_PASS_diagnostic_only")):
        for window, passed in d[key].items():
            hrows.append({"potential":potential,"lane":lane,
                          "lookback_Gyr":float(window.replace("Gyr","")),
                          "pass":bool(passed),"H_primary_Gyr":d["H_primary_Gyr"],
                          "H_distribution_Gyr":d["H_distribution_Gyr"],"H_F_Gyr":d["H_F_Gyr"]})
pd.DataFrame(hrows).sort_values(["potential","lane","lookback_Gyr"]).to_csv(
    DATA / "discovery_functional_horizon.csv", index=False)

print("CURATED_DATA_REBUILD=PASS")
