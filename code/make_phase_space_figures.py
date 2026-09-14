#!/usr/bin/env python3
"""Regenerate the two phase-space charts from curated data.

The other packaged PDF figures are preserved publication outputs. Their exact
plotted numerical values are available in the packaged CSV tables.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
data = ROOT / "data"
figures = ROOT / "figures"

parent = pd.read_csv(data / "parent_phase_space_registry.csv")
confirm = pd.read_csv(data / "confirmatory_sample.csv")
markers = {"S1":"o","S2":"s","S3":"^","S4":"D"}

def phase_xy():
    fig, ax = plt.subplots(figsize=(6.5,5.2))
    ax.scatter(parent["X_kpc"], parent["Y_kpc"], s=20, color="0.52",
               alpha=0.72, linewidths=0.35, label="165-cluster registry")
    for s in ("S1","S2","S3","S4"):
        d=confirm[confirm["stratum"]==s]
        ax.scatter(d["X_kpc"],d["Y_kpc"],s=70,marker=markers[s],label=s)
    ax.axhline(0,linewidth=0.7,color="0.75")
    ax.axvline(0,linewidth=0.7,color="0.75")
    ax.set_xlabel(r"$X$ [kpc]"); ax.set_ylabel(r"$Y$ [kpc]")
    ax.set_title("Galactocentric plane")
    ax.legend(ncol=3,fontsize=8,frameon=False)
    fig.tight_layout()
    fig.savefig(figures/"phase_space_xy.pdf",bbox_inches="tight")
    fig.savefig(figures/"phase_space_xy.png",dpi=300,bbox_inches="tight")
    plt.close(fig)

def phase_rz():
    fig, ax = plt.subplots(figsize=(6.5,5.2))
    ax.scatter(parent["R_GC_kpc"], parent["Z_kpc"], s=20, color="0.52",
               alpha=0.72, linewidths=0.35, label="165-cluster registry")
    for s in ("S1","S2","S3","S4"):
        d=confirm[confirm["stratum"]==s]
        ax.scatter(d["R_GC_kpc"],d["Z_kpc"],s=70,marker=markers[s],label=s)
    ax.axhline(0,linewidth=0.7,color="0.75")
    ax.set_xlabel(r"$R_{\rm GC}$ [kpc]"); ax.set_ylabel(r"$Z$ [kpc]")
    ax.set_title("Cylindrical radius and height")
    ax.legend(ncol=3,fontsize=8,frameon=False)
    fig.tight_layout()
    fig.savefig(figures/"phase_space_rz.pdf",bbox_inches="tight")
    fig.savefig(figures/"phase_space_rz.png",dpi=300,bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    phase_xy()
    phase_rz()
