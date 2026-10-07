""" Les cinq figures (DOS et A_k moyennées sur le désordre) de comparaison avec la littérature (Kaasbjerg PRB 101, 045433) retenues pour le chapitre 4,
redessinées au style graphene_raman.plotting. C : figures dans le corps du texte. A : figures en annexe.

    M : fig_kaasbjerg_dos_c           ρ − ρ₀ (grille 600²), brut et aligné, c_i = 0.1 % (a) et 1 % (b).
    C : fig_kaasbjerg_spectral_GKM    fonction spectrale A_k(ε) sur Γ–K–M (chemin de la Fig. 14 de Kaasbjerg), aligné, c_i = 0.1 % (a) et 1 % (b) ;
                                      points : deux plus hauts maxima de A_k par k, tracés là où A ≥ 2 % du maximum de la carte.
    A : fig_kaasbjerg_sensibilites    position du maximum de ρ − ρ₀ contre N_k^int, R_cut, taille, η_G ; tirets : valeur déduite de Kaasbjerg
                                      (Fig. 13, c_i = 1 %).
    C : fig_kaasbjerg_superposition   nos DOS ρ (ρ₀ 1 200², η 15 meV ; brut et aligné) sur celles extraites de Kaasbjerg,
                                      c_i = 0.1 % (a) et 1 % (b), spin compté (× 2).
    C : fig_kaasbjerg_sigma_K         self-énergie de désordre intrabande Σ_nn = c_i T̄_nn et effective Σ^eff_nK (éq. 44–45 de Kaasbjerg) à k = K,
                                      c_i = 1 %, brut (a) et aligné (b) ; tirets : ε − ε_nK (leurs croisements avec Re Σ^eff sont les
                                      solutions de quasi-particule). Base de bandes : celle de K + 10⁻⁶ x̂ (limite de K le long de la direction
                                      K + δx̂ de R9 D.1, comme Kaasbjerg) ; Σ(K) étant diagonal dans la base des sous-réseaux à 10⁻² près,
                                      Σ_nn = (Σ_AA + Σ_BB)/2 à 10⁻⁵ eV près, identique pour π et π* ; le terme interbande Σ_nn̄ (jusqu'à 0.27 eV)
                                      entre dans Σ^eff.

Données : donnees/kaasbjerg/: r8_dos_9x9.npz, r8_spectral_GKM_9x9.npz, r8_sens_results.json, r8_fig13_VA_interp_1meV.csv, r8_7a_results.json, r8_sigma_K_9x9.npz, r8_sigeff_results.json.
Sortie : figures/electron_defect/fig_kaasbjerg_<nom>.{pdf,png}

Usage : python scripts/make_figures_kaasbjerg.py [--only nom,nom] [--outdir figures/electron_defect]
"""
import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

from graphene_raman.plotting.palette import use_style, save, NAVY, ORANGE, SKY, GOLD, REF, MUTED, CMAP_SEQ
from graphene_raman.config import load_production, campaigns_dir

ROOT = Path(__file__).resolve().parents[1]            # scripts/ -> racine
R8 = campaigns_dir(load_production(verbose=False), "kaasbjerg")   # donnees/kaasbjerg (config)

# constantes de la campagne : variantes, concentrations, grilles
VARIANTS = ("tel_quel", "aligne")
C_LIST = (0.001, 0.01)                   # c_i, défauts par maille
GRID_SENS, NK_MAIN = 600, 900
P0 = 1200                                # ρ₀ des figures : 1 200², η 15 meV (Greg, 2026-09-29)
col = {"tel_quel": NAVY, "aligne": ORANGE}
lab = {"tel_quel": "brut", "aligne": "aligné"}      # vocabulaire brut / aligné (décision G, 2026-10-04)


def clab(cv):
    """Étiquette de concentration, point décimal : « $c$ = 0.1 % » (c = c_i, défauts par maille ; symbole c du mémoire, décision G 2026-10-07)."""
    return rf"$c$ = {cv * 100:g}" + r"\,\%"


def jload(*p):
    return json.load(open(os.path.join(R8, *p), encoding="utf-8"))


def dos_inputs():
    D = np.load(os.path.join(R8, "r8_dos_9x9.npz"))
    Kx = np.loadtxt(os.path.join(R8, "r8_fig13_VA_interp_1meV.csv"), delimiter=",", skiprows=1)
    eK, rK = Kx[:, 0], {"pristine": Kx[:, 1], 0.001: Kx[:, 2], 0.01: Kx[:, 3]}
    K7 = jload("r8_7a_results.json")["fig13_metrics"]
    egr = D["eg_rel"]
    rho0_fig = D[f"pristine_eta15_{P0}"]
    prot = lambda key: rho0_fig + (D[key] - D[key.rsplit("_c", 1)[0] + "_rho0"])          # rho0(1200^2, 15 meV) + delta rho
    return D, eK, rK, K7, egr, rho0_fig, prot


def fig_dos_c(a):
    D = np.load(os.path.join(R8, "r8_dos_9x9.npz")); egr = D["eg_rel"]
    fig, ax = plt.subplots(1, 2, figsize=(6.5, 2.6), sharex=True)
    for i, cv in enumerate(C_LIST):
        for name in VARIANTS:
            ax[i].plot(egr, D[f"{name}_{GRID_SENS}_c{cv}"] - D[f"{name}_{GRID_SENS}_rho0"], color=col[name], lw=0.9, label=lab[name])
        ax[i].set_title(f"({'ab'[i]}) " + r"$\bar\rho - \rho_0$, " + clab(cv), fontsize=9)
        ax[i].set_xlabel(r"Énergie $\varepsilon - E_D$ (eV)"); ax[i].set_xlim(-1.2, 1.2)
    ax[0].set_ylabel(r"$\bar\rho - \rho_0$ (états/eV/maille/spin)"); ax[0].legend(fontsize=7)
    fig.tight_layout(); save(fig, "fig_kaasbjerg_dos_c", a.outdir); plt.close(fig)

def fig_spectral_GKM(a):
    Sp = np.load(os.path.join(R8, "r8_spectral_GKM_9x9.npz"))
    name = "aligne"
    fig, ax = plt.subplots(1, 2, figsize=(6.5, 3.0), sharex=True, sharey=True)
    s, idx, ege = Sp["s"], Sp["idx"], Sp["eg_rel"]
    for i, cv in enumerate(C_LIST):
        A = Sp[f"A_{name}_c{cv}"]; x = ax[i]
        x.imshow(A, origin="lower", aspect="auto", extent=(s[0], s[-1], ege[0], ege[-1]), cmap=CMAP_SEQ, vmin=0, vmax=np.percentile(A, 99.5))
        for br in ("low", "up"):                                 # plotted only where A >= 2 % of the map maximum (json keeps all) :
            # à 1 %, cinq points isolés à −0.17 eV (c_i = 1 %, s − s_K = 0.26 Å⁻¹ sur K–M : résonance plate, retenue comme « deuxième maximum »
            # quand la bande de valence sort de la fenêtre) passaient le seuil de justesse ; aucun autre point ne change entre 1 et 5 %.
            e_ = Sp[f"{br}_{name}_c{cv}"]; ok_ = np.isfinite(e_)
            h_ = np.zeros_like(e_); h_[ok_] = A[np.abs(ege[:, None] - e_[None, ok_]).argmin(0), np.where(ok_)[0]]
            vis = ok_ & (h_ >= 0.02 * A.max()); x.plot(s[vis], e_[vis], ".", ms=0.8, color=ORANGE)
        x.plot(s, Sp["E_pristine"], color=REF, lw=0.4, ls="--")
        x.set_xticks(s[idx]); x.set_xticklabels([r"$\Gamma$", r"$K$", r"$M$"]); x.set_ylim(-1.2, 1.2)
        x.set_title(f"({'ab'[i]}) {lab[name]}, " + clab(cv), fontsize=9)
    ax[0].set_ylabel(r"$\varepsilon - E_D$ (eV)")
    fig.tight_layout(); save(fig, "fig_kaasbjerg_spectral_GKM", a.outdir); plt.close(fig)

def fig_sensibilites(a):
    Se = jload("r8_sens_results.json"); K7 = jload("r8_7a_results.json")["fig13_metrics"]
    fig, ax = plt.subplots(1, 4, figsize=(6.5, 2.3), sharey=True)
    groups = (("N_k_int", "N_k_int", r"$N_k^\mathrm{int}$"), ("R_cut", "R_cut", r"$R_\mathrm{cut}$"), ("taille", "size", "taille"),
              ("eta_G", "eta_G", r"$\eta_G$ (eV)"))
    for x, (g, fld, xl) in zip(ax, groups):
        for var in VARIANTS:
            rows = [r for r in Se["rows"] if (r["group"] == g or (g == "R_cut" and r["group"] == "N_k_int" and r["N_k_int"] == NK_MAIN)
                                               or (g in ("taille", "eta_G") and r["group"] == "N_k_int" and r["N_k_int"] == NK_MAIN))
                    and r["variant"] == var]
            xs = [r[fld] if fld != "size" else (9 if r["size"] == "9x9" else 12) for r in rows]
            o = np.argsort(xs); x.plot(np.array(xs)[o], np.array([r["drho_max_pos_eV"] for r in rows])[o], "o-", ms=3, lw=0.8, color=col[var],
                                       label=lab[var])
        x.axhline(K7["1.0"]["drho_max_pos_eV"], color=MUTED, lw=0.6, ls="--", label="Kaasbjerg (Fig. 13)")
        x.set_xlabel(xl)
    ax[0].set_ylabel(r"Position du max de $\bar\rho - \rho_0$ (eV)", fontsize=8); ax[0].legend(fontsize=6)
    fig.tight_layout(); save(fig, "fig_kaasbjerg_sensibilites", a.outdir); plt.close(fig)


def fig_superposition(a):
    D, eK, rK, K7, egr, rho0_fig, prot = dos_inputs()
    fig, ax = plt.subplots(1, 2, figsize=(6.5, 2.8), sharex=True)
    for j, cv in enumerate(C_LIST):
        x = ax[j]
        x.plot(eK, rK["pristine"], color=MUTED, lw=0.6, ls="--", label="Kaasbjerg, parfait")
        x.plot(eK, rK[cv], color=REF, lw=1.2, label="Kaasbjerg")
        for name in VARIANTS:
            x.plot(egr, 2 * prot(f"{name}_{GRID_SENS}_c{cv}"), color=col[name], lw=0.8, label=lab[name])
        x.set_xlim(-1.2, 1.2); x.set_xlabel(r"Énergie $\varepsilon - E_D$ (eV)")
        x.set_title(f"({'ab'[j]}) " + clab(cv) + ", spin compté", fontsize=9)
    ax[0].set_ylabel(r"DOS (états/eV/maille)")

    ax[0].legend(fontsize=6)
    fig.tight_layout(); save(fig, "fig_kaasbjerg_superposition", a.outdir); plt.close(fig)

def fig_sigma_K(a):
    Z = np.load(os.path.join(R8, "r8_sigma_K_9x9.npz")); runs = jload("r8_sigeff_results.json")["runs"]
    eg = Z["eg_rel"]
    fig, axs = plt.subplots(1, 2, figsize=(6.5, 2.8), sharey=True)
    for iv, var in enumerate(VARIANTS):
        x = axs[iv]; Se = Z[f"Seff_{var}_K"]; Sb = Z[f"Sigma_{var}_K"]
        x.plot(eg, eg - runs[f"{var} K"]["eps_k"][0], color=REF, lw=0.7, ls="--", label=r"$\varepsilon - \varepsilon_{nK}$")
        x.plot(eg, Sb[:, 0, 0].real, color=SKY, lw=0.7, label=r"Re $\Sigma_{nn}$")
        x.plot(eg, Sb[:, 0, 0].imag, color=GOLD, lw=0.7, label=r"Im $\Sigma_{nn}$")
        x.plot(eg, Se[:, 0].real, color=NAVY, lw=1.0, label=r"Re $\Sigma^\mathrm{eff}_{nK}$")
        x.plot(eg, Se[:, 0].imag, color=ORANGE, lw=1.0, label=r"Im $\Sigma^\mathrm{eff}_{nK}$")
        x.set_xlim(-1, 1); x.set_ylim(-0.35, 0.35); x.set_xlabel(r"Énergie $\varepsilon - E_D$ (eV)")
        x.set_title(f"({'ab'[iv]}) " + ("brut" if var == "tel_quel" else "aligné") + r", $c$ = 1\,\%, $k = K$", fontsize=9)
    axs[0].set_ylabel(r"$\Sigma$ (eV)"); axs[0].legend(fontsize=6, loc="lower left")
    fig.tight_layout(); save(fig, "fig_kaasbjerg_sigma_K", a.outdir); plt.close(fig)


FIGURES = {"dos_c": fig_dos_c, "spectral_GKM": fig_spectral_GKM, "sensibilites": fig_sensibilites, "superposition": fig_superposition,
           "sigma_K": fig_sigma_K}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", default=None, help="noms séparés par des virgules : " + ", ".join(FIGURES))
    ap.add_argument("--outdir", default=str(ROOT / "figures" / "electron_defect"))
    a = ap.parse_args()
    use_style()
    names = a.only.split(",") if a.only else list(FIGURES)
    for n in names:
        FIGURES[n](a); print(f"écrit {a.outdir}/fig_kaasbjerg_{n}.pdf/.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
