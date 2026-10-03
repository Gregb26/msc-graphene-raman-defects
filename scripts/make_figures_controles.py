"""Figures de contrôle du chapitre 4 retenues pour le mémoire, redessinées au style graphene_raman.plotting depuis les
json/npz des campagnes copiés dans donnees/controles/, donnees/alignement/, donnees/kaasbjerg/ et donnees/ch4/ (config ; aucun calcul). C : figures dans le corps du texte, A : figure en annexe.

  A: fig_resonance_vs_nkint_plateau        données controles/r9_b_results{,_plateau}.json
  A: fig_rcut_aligned                      max|ΔM|/max|M| contre R_cut, trois alignements ; controles/r9_a3_results{,_plateau}.json
  C: fig_folded_vs_R7                      chaîne repliée contre QE, limite diluée ; controles/r9_c_results.json
  A: fig_offset_profiles_13                profils ΔV et plateau des 13 tailles ; alignement/r10_a1_results.json, alignement/profiles_<S>.npz
  A: fig_alignement_regions               C_N selon quatre régions d'échantillonnage (A)–(D), 13 tailles ; ch4/alignement_regions.npz
                                          (statistiques calculées par GR:campagnes/M/ch4/ch4_chiffres.py regions, qui lit les scf.in de Rorqual)
  C: fig_kaasbjerg_plateau_ws              cartes A_cell|M_k'k| autour de K, non aligné (a, b) et aligné (c, d) (décision G du 2026-10-03) ; kaasbjerg/r10_c2_kaasbjerg_maps.npz

Sortie : figures/electron_defect/fig_<nom>.{pdf,png} (reproductibles au bit, palette.save). Texte en français, panneaux (a), (b), …
Usage : python scripts/make_figures_controles.py [--only nom,nom] [--outdir figures/electron_defect]
"""

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

from graphene_raman.plotting import palette as pal
from graphene_raman.plotting.palette import use_style, save
from graphene_raman.config import load_production, campaigns_dir

ROOT = Path(__file__).resolve().parents[1]            # scripts/ -> racine
CFG = load_production(verbose=False)                   # données : donnees/<sujet>/ (config campaigns_results_dir = donnees)
CTRL = Path(campaigns_dir(CFG, "controles"))           # R7, R9, R10 b/c3, R6 d4
ALIGN = Path(campaigns_dir(CFG, "alignement"))         # R10 a, c6
KAAS = Path(campaigns_dir(CFG, "kaasbjerg"))           # R8, R10 c2
CH4 = Path(campaigns_dir(CFG, "ch4"))                  # campagne M/ch4 (régions d'alignement)

FAM3 = {6, 9, 12, 15, 18, 21, 24, 27}                 # famille N = 3m (K replié sur Γ)
ALL13 = ["5x5", "6x6", "7x7", "8x8", "9x9", "10x10", "11x11", "12x12", "15x15", "18x18", "21x21", "24x24", "27x27"]
PLATEAU_FRAC = 0.75                                    # décision R9 : atomes à d >= 0,75 r_max
K_RED = np.array([2 / 3, 1 / 3, 0.0])
FIG_LABEL = {"aligne": "site unique", "exact": "site unique, exact", "aligne_lu": "site unique", "exact_lu": "site unique, exact",
             "aligne_plateau": "Kumagai–Oba", "exact_plateau": "Kumagai–Oba, exact"}


def jload(p):
    return json.load(open(p, encoding="utf-8"))


def size_n(S):
    return int(S.split("x")[0])


def times(S):
    return S.replace("x", r"$\times$")

# ---------------------------------------------------------------------------------------------------- R9 (r9_driver.b_figure, cmd_synth, c_figure)
def _b_figure(res, name, outdir):
    """Pic de la courbe Γ_T, pic de −Im T̄(K) et E_res contre 1/N_k^int, 9×9 et 12×12, une courbe par variante d'alignement."""
    sizes = [S for S in ("9x9", "12x12") if S in res]
    fig, axes = plt.subplots(1, len(sizes), figsize=(6.5, 3.5), sharey=True, squeeze=False)
    for ax, S, lab in zip(axes[0], sizes, "ab"):
        for var, ls, mk in [(v, l_, m_) for v, l_, m_ in (("brut", "-", "o"), ("aligne", "--", "s"), ("exact", ":", "^"), ("aligne_lu", "--", "s"),
                                                          ("exact_lu", ":", "^"), ("aligne_plateau", "-.", "D"), ("exact_plateau", ":", "v")) if v in res[S]]:
            rr = sorted(res[S][var].items(), key=lambda kv: int(kv[0])); x = [1.0 / int(nk) for nk, _ in rr]
            suf = "" if var == "brut" else " (" + FIG_LABEL.get(var, var) + ")"
            ax.plot(x, [r["peak_GT_fine"] for _, r in rr], ls, marker=mk, ms=3, color=pal.NAVY, label=r"pic de $\Gamma_T$" + suf)
            ax.plot(x, [r["peak_ImTbar"] for _, r in rr], ls, marker=mk, ms=3, color=pal.ORANGE, label=r"pic de $-\mathrm{Im}\,\bar T(K)$" + suf)
            ax.plot(x, [r["E_res"] for _, r in rr], ls, marker=mk, ms=3, color=pal.GREEN, label=r"$E_\mathrm{res}$ (états $240^2$)" + suf)
        ax.set_xlabel(r"$1/N_k^\mathrm{int}$"); ax.set_title(f"({lab}) {times(S)}", fontsize=9)
    axes[0][0].set_ylabel(r"Énergie $\varepsilon - E_D$ (eV)")
    h, l_ = axes[0][0].get_legend_handles_labels()                               # légende commune sous les panneaux (ne couvre aucune courbe)
    fig.legend(h, l_, loc="lower center", ncol=3, fontsize=5, frameon=False)
    fig.tight_layout(rect=(0, 0.035 * ((len(l_) + 2) // 3) + 0.03, 1, 1)); save(fig, name, outdir); plt.close(fig)


def _b_res(path, keys):
    res = jload(path)
    return {S: {v: res[S][v] for v in keys if v in res[S]} for S in ("9x9", "12x12") if S in res}

def fig_resonance_vs_nkint_plateau(outdir):
    """Variantes plateau seules (aligné (i) et aligné exact), comme `r9_driver.py b --cn plateau`."""
    _b_figure(_b_res(CTRL / "r9_b_results_plateau.json", ("aligne_plateau", "exact_plateau")), "fig_resonance_vs_nkint_plateau", outdir)


def fig_rcut_aligned(outdir):
    """max|ΔM|/max|M| (paire π) contre R_cut, 9×9 et 12×12, pour M2 tel quel, C_N Lu et C_N plateau (+ variantes exactes)."""
    A9 = jload(CTRL / "r9_a3_results.json"); AP = jload(CTRL / "r9_a3_results_plateau.json")
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.0), sharey=True)
    for ax, S, lab in zip(axes, ("9x9", "12x12"), "ab"):
        r9 = A9[f"rcut_{S}"]["rows"]; rp = AP[f"rcut_{S}"]["rows"]
        series = [(r9["brut"], pal.NAVY, "-", "o", "non aligné"), (r9["aligne"], pal.ORANGE, "--", "s", "site unique"),
                  (rp["aligne_plateau"], pal.GREEN, "-.", "D", "Kumagai–Oba")]
        if "exact" in r9 and "exact_plateau" in rp:
            series += [(r9["exact"], pal.ORANGE, ":", "^", "site unique, exact"), (rp["exact_plateau"], pal.GREEN, ":", "v", "Kumagai–Oba, exact")]
        for rows, c, ls, mk, lb in series:
            ax.semilogy([r["R_cut"] for r in rows], [r["max_dM_over_maxM"] for r in rows], ls, marker=mk, ms=3, color=c, label=lb, mfc="none")
        ax.set_xlabel(r"Rayon de coupure $R_\mathrm{cut}$ (mailles)"); ax.set_title(f"({lab}) {times(S)}", fontsize=9)
    axes[0].set_ylabel(r"$\max|\Delta M|/\max|M|$ (paire $\pi$)"); axes[0].legend(fontsize=5)
    fig.tight_layout(); save(fig, "fig_rcut_aligned", outdir); plt.close(fig)


def fig_folded_vs_R7(outdir):
    """Chaîne repliée N×N contre QE (R7) : état π quasi-lié (a) et maximum de la LDOS des voisins (b) contre 1/N, limite diluée."""
    out = jload(CTRL / "r9_c_results.json")
    fig, ax = plt.subplots(1, 2, figsize=(6.5, 3.0))
    N1 = sorted(int(N) for N in out.get("C1", {})); N2 = sorted(int(N) for N in out.get("C2", {}) if not out["C2"][N].get("skipped"))
    qe = [(N, out["C1"][str(N)]["QE"]["pi_quasi_bound"]["x"]) for N in N1 if out["C1"][str(N)]["QE"]]
    ax[0].plot([1 / N for N, _ in qe], [x for _, x in qe], "o", ms=3, color=pal.REF, label="QE (R7)")
    for var, c, mk in (("brut", pal.NAVY, "s"), ("aligne", pal.ORANGE, "^")):
        lab = "modèle replié" + (" (site unique)" if var == "aligne" else "")
        ax[0].plot([1 / N for N in N1] + [1 / N for N in N2 if N > 27], [out["C1"][str(N)][var]["odd"]["quasi_bound"]["x"] for N in N1]
                   + [out["C2"][str(N)][var]["odd"]["quasi_bound"]["x"] for N in N2 if N > 27], mk, ms=3, mfc="none", color=c, label=lab)
        ax[1].plot([1 / N for N in N1] + [1 / N for N in N2 if N > 27], [out["C1"][str(N)][var]["ldos_max"]["at_eV"] for N in N1]
                   + [out["C2"][str(N)][var]["ldos_max"]["at_eV"] for N in N2 if N > 27], mk, ms=3, mfc="none", color=c, label=lab)
        if "C3" in out and "600" in out["C3"]:
            ax[1].axhline(out["C3"]["600"][var]["at_eV"], color=c, lw=0.8, ls="--", label=r"matrice $T$" + (" (site unique)" if var == "aligne" else ""))
    Ns = N1 + [N for N in N2 if N > 27]
    for a_ in ax:
        a_.set_ylim(-1.12, 0.05)                                                # N = 6 : maximum de LDOS au bord de [−1, 0] (état π à −1,04 eV)
    ax[1].plot([1 / N for N in Ns], [(out["C1"].get(str(N)) or out["C2"].get(str(N)))["first_crown"]["pi"] for N in Ns], "-", color=pal.LIGHT, lw=0.8, label="première couronne")
    ax[0].set_xlabel(r"$1/N$"); ax[0].set_ylabel(r"État $\pi$ quasi-lié $\varepsilon - E_D$ (eV)"); ax[0].set_title("(a)", fontsize=9); ax[0].legend(fontsize=5)
    ax[1].set_xlabel(r"$1/N$"); ax[1].set_ylabel(r"Maximum de la LDOS des voisins (eV)"); ax[1].set_title("(b)", fontsize=9); ax[1].legend(fontsize=5)
    fig.tight_layout(); save(fig, "fig_folded_vs_R7", outdir); plt.close(fig)


# ---------------------------------------------------------------------------------------------------- R10 (a1_figure, a2_figure, c2_figure)
def fig_offset_profiles_13(outdir):
    """Décalages de sphère ΔV contre la distance à la lacune, 13 tailles ; zone grisée = plateau (d ≥ 0,75 r_max), C_N = sa moyenne."""
    out = jload(ALIGN / "r10_a1_results.json")
    sizes = [S for S in ALL13 if S in out["sizes"]]
    fig, axes = plt.subplots(4, 4, figsize=(6.5, 7.6), squeeze=False); nout = []
    for ax in axes.ravel()[len(sizes):]:
        ax.set_visible(False)
    for i, (ax, S) in enumerate(zip(axes.ravel(), sizes)):
        r = out["sizes"][S]; Z = np.load(ALIGN / f"profiles_{S}.npz")
        d, s = Z["dist"], Z["shift10"] * 1e3; C = r["C_N_eV"] * 1e3; far = Z["far"]
        ax.axvspan(PLATEAU_FRAC * r["r_max_A"], r["r_max_A"] * 1.03, color=pal.LIGHT, alpha=0.35, lw=0)
        ax.plot(d, s, "o", ms=1.6, color=pal.NAVY, label=r"sphères de 1.0 Å")
        ax.axhline(C, color=pal.NAVY, lw=0.8, label=r"$\Delta V_\mathrm{PA}^{(N)}$ (Kumagai–Oba)")
        ax.axhline(r["Lu"]["published_meV"], color=pal.REF, lw=0.8, ls="--", label="site unique (un atome, distances axe par axe)")
        ax.plot(d[far], s[far], "D", ms=3.2, mfc="none", mec=pal.ORANGE, mew=0.9, label="atomes vraiment les plus loin")
        keep = d >= 2.0                                                         # cadre sans les premiers voisins (1,42 Å)
        lo = min(s[keep].min(), C, r["Lu"]["published_meV"]); hi = max(s[keep].max(), C, r["Lu"]["published_meV"]); pad = 0.08 * (hi - lo)
        lo, hi = lo - pad, hi + pad; nout.append(int(((s < lo) | (s > hi)).sum()))
        ax.set_ylim(lo, hi); ax.set_title(f"({chr(97 + i)}) {times(S)}", fontsize=7, loc="left")
        ax.tick_params(labelsize=6)
        if i % 4 == 0:
            ax.set_ylabel(r"$\Delta V$ (meV)", fontsize=7)
        if i >= len(sizes) - 4:
            ax.set_xlabel("Distance à la lacune (Å)", fontsize=7)
    h, l_ = axes[0][0].get_legend_handles_labels()
    fig.legend(h, l_, loc="lower center", ncol=2, fontsize=6, frameon=False, bbox_to_anchor=(0.5, 0.012))
    fig.text(0.5, 0.004, f"Hors cadre : {', '.join(map(str, sorted(set(nout))))} point(s) par panneau, les premiers voisins de la lacune (1.42 Å). Zone grisée : "
             + r"$d \geq 0.75\, r_\mathrm{max}$.",
             ha="center", va="bottom", fontsize=5.5, color=pal.MUTED)
    fig.tight_layout(rect=(0, 0.065, 1, 1)); save(fig, "fig_offset_profiles_13", outdir); plt.close(fig)

def fig_alignement_regions(outdir):
    """C_N (moyenne ± rms des décalages de sphère) contre N pour quatre régions d'échantillonnage : (A) d ≥ 0.75 r_max (production),
    (B) Kumagai–Oba 2D d ≥ N·a/2, (C) Kumagai–Oba 3D d ≥ min(N·a/2, c/2), (D) site unique. Porté de GR:campagnes/M/ch4/ch4_chiffres.py
    (make_regions_figure) le 2026-10-01 : même tracé, données lues dans le npz au lieu d'être recalculées, point décimal."""
    Z = np.load(CH4 / "alignement_regions.npz")
    sizes = [str(S) for S in Z["sizes"]]
    Ns = np.array([int(Z[f"{S}_N"]) for S in sizes])
    fam3 = np.array([str(Z[f"{S}_family"]) == "3m" for S in sizes])
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    series = [(r"(A) $\geq 0.75\,r_\mathrm{max}$ (nous)", "meanA", "rmsA", pal.CYCLE[0]),
              (r"(B) Kumagai–Oba 2D, $\geq N a/2$", "meanB", "rmsB", pal.CYCLE[1]),
              (r"(C) Kumagai–Oba 3D, $\min(Na/2, c/2)$", "meanC", "rmsC", pal.CYCLE[2])]
    for i, (lab, mk, rk, col) in enumerate(series):
        m = np.array([float(Z[f"{S}_{mk}"]) for S in sizes]) * 1e3
        r = np.array([float(Z[f"{S}_{rk}"]) for S in sizes]) * 1e3
        off = (i - 1) * 0.12
        for sel, mark in ((fam3, "o"), (~fam3, "s")):
            ax.errorbar(Ns[sel] + off, m[sel], yerr=r[sel], fmt=mark, color=col, ms=4, capsize=2, lw=1, label=lab if mark == "o" else None)
    lu = np.array([float(Z[f"{S}_Lu"]) for S in sizes]) * 1e3
    for sel, mark in ((fam3, "o"), (~fam3, "s")):
        ax.plot(Ns[sel] + 0.24, lu[sel], mark, mfc="none", color=pal.CYCLE[3], ms=4, label="(D) site unique" if mark == "o" else None)
    ax.plot([], [], "o", color=pal.MUTED, label="famille $N = 3m$")
    ax.plot([], [], "s", color=pal.MUTED, label=r"famille $N \neq 3m$")
    ax.set_xlabel("Taille de la super-cellule $N$")
    ax.set_ylabel(r"$\Delta V_\mathrm{PA}^{(N)}$ (meV), moyenne $\pm$ rms")
    ax.set_xticks(Ns)
    ax.legend(fontsize=7, ncol=2)
    fig.tight_layout(); save(fig, "fig_alignement_regions", outdir); plt.close(fig)


def fig_kaasbjerg_plateau_ws(outdir):
    """Cartes A_cell|M_k'k| (valence, conduction) autour de K, étiquettes de Wigner-Seitz : (a, b) non aligné (= convention
    de Kaasbjerg, référence du vide), (c, d) aligné (Kumagai–Oba). Décision G du 2026-10-03 : les deux variantes."""
    Z = np.load(KAAS / "r10_c2_kaasbjerg_maps.npz"); Bc = Z["Bc"]; kc = Z["kc"]
    maps = {"tel quel": {"valence": Z["tel_quel_valence"], "conduction": Z["tel_quel_conduction"]},
            "plateau": {"valence": Z["plateau_valence"], "conduction": Z["plateau_conduction"]}}
    imgs = np.array([[i, j] for i in (-1, 0, 1) for j in (-1, 0, 1)]) @ Bc[:2, :2].T
    kf = np.array([kc[i] + imgs[np.argmin(np.linalg.norm(kc[i] + imgs, axis=1))] for i in range(len(kc))])
    corners = np.array([Bc[:2, :2] @ np.array(c) for c in [(2/3, 1/3), (1/3, 2/3), (-1/3, 1/3), (-2/3, -1/3), (-1/3, -2/3), (1/3, -1/3)]])
    corners = corners[np.argsort(np.arctan2(corners[:, 1], corners[:, 0]))]; Kc = Bc @ K_RED
    labs = list(maps); fig, axes = plt.subplots(len(labs), 2, figsize=(6.5, 3.0 * len(labs)), squeeze=False)
    vmax = max(np.nanmax(maps[v][b]) for v in labs for b in ("valence", "conduction")); vmin = min(np.nanmin(maps[v][b]) for v in labs for b in ("valence", "conduction"))
    tl = {"tel quel": "non aligné", "plateau": "aligné"}
    for i, lab in enumerate(labs):
        for j, (band, bl) in enumerate((("valence", r"valence ($\pi$)"), ("conduction", r"conduction ($\pi^*$)"))):
            ax = axes[i][j]; z = maps[lab][band]; m = np.isfinite(z)
            sc = ax.scatter(kf[m, 0], kf[m, 1], c=z[m], s=0.6, cmap=pal.CMAP_SEQ, vmin=vmin, vmax=vmax, rasterized=True)
            ax.plot(np.r_[corners[:, 0], corners[0, 0]], np.r_[corners[:, 1], corners[0, 1]], color=pal.REF, lw=0.6)
            ax.plot(Kc[0], Kc[1], "x", color=pal.ORANGE, ms=4)
            ax.set_aspect("equal"); ax.set_xlabel(r"$k'_x$ (Å$^{-1}$)", fontsize=7); ax.set_ylabel(r"$k'_y$ (Å$^{-1}$)", fontsize=7)
            ax.set_title(f"({'abcd'[2*i+j]}) {bl}, {tl[lab]}", fontsize=8)
            fig.colorbar(sc, ax=ax, label=r"$A_\mathrm{cell}|M_{k'k}|$ (eV Å$^2$)")
    fig.tight_layout(); save(fig, "fig_kaasbjerg_plateau_ws", outdir); plt.close(fig)


FIGURES = {f.__name__[4:]: f for f in (fig_resonance_vs_nkint_plateau, fig_rcut_aligned,
                                       fig_folded_vs_R7, fig_offset_profiles_13, fig_alignement_regions, fig_kaasbjerg_plateau_ws)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", default="", help="noms séparés par des virgules (sans le préfixe fig_)")
    ap.add_argument("--outdir", default=str(ROOT / "figures" / "electron_defect"))
    a = ap.parse_args()
    use_style()
    names = [n for n in a.only.split(",") if n] or list(FIGURES)
    for n in names:
        FIGURES[n](a.outdir); print(f"écrit {a.outdir}/fig_{n}.pdf/.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
