#!/usr/bin/env python
"""
Figures du chapitre 4 du mémoire, style graphene_raman.plotting (memoire.mplstyle), français, données lues dans <results_dir>/*.npz.
C : figures dans le corps du texte. A : figures en annexe.

  A: fig_convergence        (a) Γ^ed/c vs R_cut, six tailles ; (b) carte plateau (grille × η), référence     — 6.5 × 3.4 po
  C: fig_locality_final     (a) 5×5, (b) 8×8 avec grille aliasée ; (c) 9×9, (d) 12×12                 — 6.5 × 5.6 po
  C: fig_spectral_final     (a) Γ(ε) T vs Born (log) ; (b) δρ ; (c) T̄_ππ(K,K;ε) ; (d) critère det / λ_min       — 6.5 × 5.6 po
  C: fig_M_scaling_final    max|M| vs N, convention cellule unitaire (panneau unique)                           — 6.5 × 4.0 po
  C: fig_Ved                (a) carte 5×5, (b) carte 9×9 (colorbar commune) ; (c) profil radial masqué, + C_N (pointillés, R10) — 6.5 × 7.2 po
  C: fig_Ved_zoom           V_ed^L dans le plan, zoom ±3 Å : (a) 8×8, (b) 9×9 (reprise à l'identique de make_figures.py)
  A: fig_level2             Γ^ed/c (médiane ±3 eV) contre la taille N de la super-cellule, paramètres de production      — 6.5 × 3.6 po
  C: fig_ks_reconstruction  |ε_calc − ε_QE| contre N, grilles N×N et denses, moyenne et max (reprise à l'identique de make_figures.py)
Usage : python scripts/make_figures_defaut.py [--outdir figures/electron_defect]
"""

import argparse, os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm
from graphene_raman.config import load_production, results_dir, alignment_C
RES = results_dir(load_production(verbose=False))          # R10 : produits (results/M2_plateau) ; matrices par matrices_dir

from graphene_raman.plotting.palette import save as palette_save, use_style; use_style()
from graphene_raman.plotting.palette import NAVY, ORANGE, GREEN, GOLD, PINK, SKY, REF, INK, MUTED, LIGHT, COL, CMAP_SEQ, CMAP_DIV
FAM3 = {"6x6", "9x9", "12x12"}
C_T, C_BORN, C_REF, C_DIS = NAVY, ORANGE, REF, GREEN
LBL_E = r"Énergie $\varepsilon - E_D$ (eV)"; LBL_G = r"$\Gamma^\mathrm{ed}/c$ (meV)"
ap = argparse.ArgumentParser(); ap.add_argument("--outdir", default="figures/electron_defect"); a = ap.parse_args()
cfg = load_production(); RC, GRID, ETA = cfg["R_cut"], cfg["grid"], cfg["eta_eV"]; REF = cfg["reference_size"]
SIZES = ["5x5", "6x6", "7x7", "8x8", "9x9", "12x12"]; DONE = []
def lab(S): return S.replace("x", r"$\times$")
def famlab(S): return lab(S)                      # (mention N = 3m retirée des figures, 2026-09-15)
def panel(ax, letter):
    t = ax.get_title(loc="left"); ax.set_title(f"({letter}) {t}" if t else f"({letter})", loc="left", fontsize=ax.title.get_fontsize())
def save(fig, name):
    palette_save(fig, name, a.outdir)          # pdf + png, métadonnées fixées (reproductible au bit)
    w, h = fig.get_size_inches(); DONE.append((name, w, h)); plt.close(fig); print(f"écrit {a.outdir}/{name}.pdf/.png  ({w:.2f} × {h:.2f} po)")
def load_map(S):
    f = f"{RES}/specwd_{S}_prod.npz"
    if not os.path.exists(f): return None
    r = np.load(f)["results"]; return {(int(x[0]), int(x[1]), round(float(x[2]), 4)): float(x[3]) for x in r}
maps = {S: m for S in SIZES if (m := load_map(S))}

# ---------------- 1. fig_convergence : (a) R_cut, (b) plateau
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.5, 3.4), gridspec_kw=dict(width_ratios=[1.0, 1.15]))
rcs = sorted({k[0] for m in maps.values() for k in m})
for S, m in maps.items():
    y = [m.get((rc, GRID, ETA), np.nan) for rc in rcs]; ax1.plot(rcs, y, "-o", color=COL[S], ms=5, label=famlab(S))
ax1.set_xlabel(r"Rayon de coupure $R_\mathrm{cut}$ (indices réduits)"); ax1.set_ylabel(LBL_G); ax1.set_xticks(rcs)
ax1.set_title(rf"Grille $k$ {GRID}$\times${GRID}, $\eta$ = {ETA} eV", loc="left", fontsize=9); ax1.legend(title="Super-cellule", ncol=1, fontsize=7, title_fontsize=8, loc="upper right", borderaxespad=0.3); panel(ax1, "a")
m = maps[REF]; grids = sorted({k[1] for k in m}); etas = sorted({k[2] for k in m}, reverse=True)
Z = np.array([[m[(RC, N, e)] for e in etas] for N in grids]); ref = Z[grids.index(GRID), etas.index(ETA)]; D = (Z / ref - 1) * 100; vmax = max(5, np.abs(D).max())
im = ax2.imshow(np.abs(D), cmap=CMAP_SEQ, vmin=0, vmax=vmax, origin="lower", aspect="auto")
ax2.set_xticks(range(len(etas))); ax2.set_xticklabels([f"{e:g}" for e in etas]); ax2.set_yticks(range(len(grids))); ax2.set_yticklabels([rf"{N}$^2$" for N in grids]); ax2.grid(False)
for i in range(len(grids)):
    for j in range(len(etas)): ax2.text(j, i, f"{Z[i,j]:.0f}\n({D[i,j]:+.1f}\\,\\%)", ha="center", va="center", fontsize=8, color=INK if abs(D[i, j]) < 0.6 * vmax else "white")
ax2.set_xlabel(r"Élargissement $\eta$ (eV)"); ax2.set_ylabel(r"Grille $k$ de sortie"); ax2.set_title(rf"{lab(REF)}, $R_\mathrm{{cut}}$ = {RC} : $\Gamma^\mathrm{{ed}}/c$ (meV)", loc="left", fontsize=9); panel(ax2, "b")
cb = fig.colorbar(im, ax=ax2, shrink=0.9, pad=0.02); cb.set_label(rf"Écart à ({GRID}$^2$, {ETA} eV) (\%)")
fig.tight_layout(); save(fig, "fig_convergence")

# ---------------- 2. fig_locality_final : 5×5, 8×8 (aliasée), 9×9, 12×12
L = np.load(f"{RES}/mwr_locality.npz")
fig, axs = plt.subplots(2, 2, figsize=(6.5, 5.6), sharex=True, sharey=True); axs = axs.ravel()
for i, S in enumerate(["5x5", "8x8", "9x9", "12x12"]):
    ax = axs[i]; onv = float(L[f"{S}_dense_onsite_pzvac"])
    ax.semilogy(L[f"{S}_dense_dist"], L[f"{S}_dense_w"], "o", color=COL[S], ms=3.2, zorder=2, label="Grille élargie")
    if f"{S}_coarse_w" in L:
        ax.semilogy(L[f"{S}_coarse_dist"], L[f"{S}_coarse_w"], "x", color=C_REF, ms=4, zorder=3, label="Grille grossière")
    ax.set_title(famlab(S), loc="left"); ax.legend(loc="upper right", fontsize=7, handletextpad=0.4); ax.set_ylim(2e-5, 60); panel(ax, "abcd"[i])
for ax in axs[2:]: ax.set_xlabel(r"Distance $|R|$ ($a$)")
for ax in axs[::2]: ax.set_ylabel(r"$\|M_{ij}(R,0)\|$ (eV)")
fig.tight_layout(); save(fig, "fig_locality_final")

# ---------------- 3. fig_spectral_final : 2×2
R = np.load(f"{RES}/resonance_{REF}.npz"); C = np.load(f"{RES}/resonance_criteria_{REF}.npz")
ED = float(R["E_D"]); x = R["eg"] - ED; xg = R["egrid"] - ED; c = float(R["conc"])
fig, axs = plt.subplots(2, 2, figsize=(6.5, 5.6)); (a1, a2), (a3, a4) = axs
GT, GB = R["Gamma_T"] * 1e3, R["Gamma_Born"] * 1e3
a1.semilogy(x, GT, color=C_T, label=r"matrice $T$ (exacte)"); a1.semilogy(x, GB, color=C_BORN, label="approximation de Born (2$^\\mathrm{e}$ ordre)")
a1.set_ylabel(LBL_G); a1.set_title(rf"$\Gamma(\varepsilon)$ sur-couche, {lab(REF)}", loc="left", fontsize=9); a1.set_ylim(0.5 * min(GT.min(), GB.min()), 10 * max(GT.max(), GB.max())); a1.legend(fontsize=7, loc="upper center", title=rf"$\eta$ = {float(R['eta'])} eV", title_fontsize=7)
a2.plot(x, R["rho0"], color=C_REF, label=r"$\rho_0$ (cristal parfait)"); a2.plot(x, R["rho_dis"], color=C_DIS, label=rf"$\rho_0 + c\,\delta\rho$, $c$ = {c*100:.0f}\,\%")
a2.set_ylabel("Densité d'états (états/eV/cellule)"); a2.set_title(r"$\delta\rho = \rho_\mathrm{dis}-\rho_0$", loc="left", fontsize=9); a2.legend(fontsize=8)
tr = R["Tbar_tr"]; a3.plot(xg, tr.real, color=C_T, label=r"Re $\bar T_{\pi\pi}(K,K;\varepsilon)$"); a3.plot(xg, tr.imag, color=C_BORN, label=r"Im $\bar T_{\pi\pi}(K,K;\varepsilon)$"); a3.axhline(0, color=MUTED, lw=0.8)
a3.set_ylabel(r"$\bar T$ (eV, par défaut)"); a3.set_title(r"$\bar T_{\pi\pi}$ en $K$ (trace/2)", loc="left", fontsize=9); a3.legend(fontsize=8)
xc = C["eg"] - float(C["E_D"]); a4.semilogy(xc, np.exp(C["logdet_rel"]), color=C_T, label=r"$|\det\mathbf{\Lambda}_\mathcal{C}|$ / max"); a4.semilogy(xc, C["minlam"], color=C_BORN, label=r"$\min_i|\lambda_i|$, $\lambda_i$ valeurs propres de $\mathbf{\Lambda}_\mathcal{C}$")
a4.set_ylabel("Sans dimension"); a4.set_title("Critère de résonance", loc="left", fontsize=9); a4.legend(fontsize=8)
for i, ax in enumerate(axs.ravel()): ax.set_xlabel(LBL_E); ax.axvline(0, color=MUTED, lw=0.8, ls=":"); panel(ax, "abcd"[i])
fig.tight_layout(); save(fig, "fig_spectral_final")

# ---------------- 4. fig_M_map_final : retirée le 2026-10-05 (figure supprimée du chapitre, décision G du 2026-10-04) ; M_analysis.npz reste lu pour fig_M_scaling_final
Zm = np.load(f"{RES}/M_analysis.npz", allow_pickle=True)

# ---------------- 5. fig_M_scaling_final : panneau unique
Ns = [int(S.split("x")[0]) for S in SIZES if f"scale_{S}_dense" in Zm]; dd = [float(Zm[f"scale_{S}_dense"]) for S in SIZES if f"scale_{S}_dense" in Zm]; cc_ = [float(Zm[f"scale_{S}_coarse"]) for S in SIZES if f"scale_{S}_dense" in Zm]
fig, ax = plt.subplots()
ax.plot(Ns, dd, "o-", color=C_T, label="Grille élargie"); ax.plot(Ns, cc_, "x--", color=C_REF, label="Grille grossière")
ax.set_ylabel(r"$\max|M|$ (eV)"); ax.set_ylim(0, max(dd + cc_) * 1.25); ax.set_xlabel(r"Taille de la super-cellule $N$"); ax.set_xticks(Ns); ax.legend()
ax.set_title("Vérification de la convention intensive", loc="left", fontsize=9); save(fig, "fig_M_scaling_final")

# ---------------- 6. fig_Ved : (a) carte 5×5, (b) carte 9×9, (c) profil radial masqué
V = np.load(f"{RES}/ved_analysis.npz"); LIN = 1e-2
fig = plt.figure(figsize=(6.5, 6.0)); gs = fig.add_gridspec(2, 2, height_ratios=[0.78, 1.55], hspace=0.45, wspace=0.10, top=0.97, bottom=0.16)
axa, axb, axc = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, :])
vmax = max(np.abs(V["5x5_map"]).max(), np.abs(V["9x9_map"]).max()); norm = SymLogNorm(linthresh=LIN, vmin=-vmax, vmax=vmax, base=10)
for ax, S, let in ((axa, "5x5", "a"), (axb, "9x9", "b")):
    pc = ax.pcolormesh(V[f"{S}_map_X"], V[f"{S}_map_Y"], V[f"{S}_map"], norm=norm, cmap=CMAP_DIV, shading="nearest", rasterized=True)
    ax.set_aspect("equal"); ax.set_xlabel(r"$x$ (Å)"); ax.set_title(rf"{lab(S)}, plan $z = z_\mathrm{{C}}$", loc="left", fontsize=9); panel(ax, let)
axa.set_ylabel(r"$y$ (Å)"); axb.tick_params(labelleft=False)
cb = fig.colorbar(pc, ax=[axa, axb], shrink=1.0, pad=0.02, aspect=16); cb.ax.tick_params(labelsize=7); cb.set_label("$V_\\mathrm{ed}^L$ (eV)\nsymlog, lin. entre $\\pm10^{-2}$ eV", fontsize=7)
for S in SIZES:
    if f"{S}_rad_masked" in V:
        axc.plot(V[f"{S}_rc_masked"], V[f"{S}_rad_masked"], color=COL[S], label=famlab(S))
        axc.axhline(alignment_C(cfg, S), color=COL[S], ls=":", lw=0.9)                                 # R10 : C_N (Kumagai–Oba, config) de la taille
axc.axhline(0, color=MUTED, lw=0.8); axc.set_yscale("symlog", linthresh=LIN, linscale=0.4)
axc.set_xlabel(r"Distance au site $r$ (Å)"); axc.set_ylabel(r"$\bar V_\mathrm{ed}^{L}$ (eV)"); axc.legend(title="Super-cellule", ncol=6, fontsize=7, title_fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.20), frameon=False)
axc.set_title("Moyenne du potentiel local dans le plan du graphène", loc="left", fontsize=9); panel(axc, "c")
save(fig, "fig_Ved")

# ---------------- 7. trois figures reprises de make_figures.py (2026-10-01) : fig_level2, fig_ks_reconstruction, fig_Ved_zoom
# fig_level2 : Γ^ed/c (médiane sur ±3 eV) contre N aux paramètres de production ; retirée le 2026-10-05, rétablie le 2026-10-07 pour l'annexe D
# (décision G ; même donnée que la colonne R_cut = 3 de tab:convergence_gamma, specwd_<N>_prod.npz). Étiquette Γ^ed/c, pas Γ N_cells.
if maps:
    fig, ax = plt.subplots(figsize=(6.5, 3.6)); Ns = [int(S.split("x")[0]) for S in maps]; ys = [maps[S][(RC, GRID, ETA)] for S in maps]
    for S, N, y in zip(maps, Ns, ys): ax.plot([N], [y], "o", color=COL[S], ms=7, label=famlab(S))
    pts = sorted(zip(Ns, ys)); ax.plot([q[0] for q in pts], [q[1] for q in pts], "-", color=MUTED, lw=1, zorder=0); ax.axvspan(0, cfg["N_min"] - 0.5, color="#e6e6e3", alpha=0.5, lw=0)
    ax.set_xlabel(r"Taille de la super-cellule $N$ ($N\times N$)"); ax.set_ylabel(LBL_G); ax.set_xticks(Ns); ax.set_xlim(min(Ns) - 1, max(Ns) + 1)
    ax.set_title(rf"$R_\mathrm{{cut}}$ = {RC}, grille {GRID}$^2$, $\eta$ = {ETA} eV", loc="left", fontsize=9); ax.legend(ncol=2, fontsize=8); save(fig, "fig_level2")


ks = f"{RES}/ks_reconstruction.npz"                      # reconstruction KS avec V_p (super-cellule parfaite), moyenne sur bandes et k
if os.path.exists(ks):
    K = np.load(ks); mc = []; md = []; xc = []; xd = []
    for S in SIZES:
        mc.append(float(K[f"{S}_coarse_mean_meV"]) if f"{S}_coarse_mean_meV" in K else np.nan); xc.append(float(K[f"{S}_coarse_max_meV"]) if f"{S}_coarse_max_meV" in K else np.nan)
        md.append(float(K[f"{S}_dense_mean_meV"]) if f"{S}_dense_mean_meV" in K else np.nan); xd.append(float(K[f"{S}_dense_max_meV"]) if f"{S}_dense_max_meV" in K else np.nan)
    Nall = [int(S.split("x")[0]) for S in SIZES]
    fig, ax = plt.subplots()
    ax.plot(Nall, mc, "o-", color=C_REF, label=r"grille $N\times N$ : moyenne")
    ax.plot(Nall, xc, "o--", color=C_REF, mfc="none", label=r"grille $N\times N$ : max")
    ax.plot(Nall, md, "s-", color=C_T, label="dense : moyenne")
    ax.plot(Nall, xd, "s--", color=C_T, mfc="none", label="dense : max")
    ax.set_yscale("log"); ax.set_xticks(Nall); ax.set_xlabel(r"Taille de la super-cellule $N$"); ax.set_ylabel(r"$|\varepsilon_\mathrm{calc} - \varepsilon_\mathrm{QE}|$ (meV)")
    ax.set_title(r"Reconstruction KS avec $V_p$ (décalage constant retiré), bandes et $k$ confondus", loc="left", fontsize=10); ax.legend(ncol=2)
    save(fig, "fig_ks_reconstruction")

vfz = f"{RES}/ved_analysis.npz"                           # zoom 8×8 contre 9×9 (±3 Å, même échelle, atomes superposés)
if os.path.exists(vfz) and "9x9_rad_masked" in np.load(vfz):
    Vz = np.load(vfz); LINZ = 1e-2; Z = 3.0
    fig, axs = plt.subplots(1, 2, figsize=(6.5, 3.4), layout="constrained"); vmax = 0.0
    for S in ("8x8", "9x9"):
        Xm, Ym, Vm = Vz[f"{S}_map_X"], Vz[f"{S}_map_Y"], Vz[f"{S}_map"]; sel = (np.abs(Xm) <= Z) & (np.abs(Ym) <= Z); vmax = max(vmax, np.abs(Vm[sel]).max())
    norm = SymLogNorm(linthresh=LINZ, vmin=-vmax, vmax=vmax, base=10)
    for ax, S, let in ((axs[0], "8x8", "a"), (axs[1], "9x9", "b")):
        pc = ax.pcolormesh(Vz[f"{S}_map_X"], Vz[f"{S}_map_Y"], Vz[f"{S}_map"], norm=norm, cmap=CMAP_DIV, shading="nearest", rasterized=True)
        at = Vz[f"{S}_atoms_xy"]; ax.plot(at[:, 0], at[:, 1], "o", mfc="none", mec=INK, mew=0.7, ms=5); ax.plot(0, 0, "x", color=INK, ms=6)
        ax.set_xlim(-Z, Z); ax.set_ylim(-Z, Z); ax.set_aspect("equal"); ax.set_xlabel(r"$x$ (Å)"); ax.set_title(rf"{lab(S)}, plan $z = z_\mathrm{{C}}$", loc="left", fontsize=10); panel(ax, let)
    axs[0].set_ylabel(r"$y$ (Å)"); cb = fig.colorbar(pc, ax=axs, shrink=0.9); cb.set_label(r"$V_\mathrm{ed}^L$ (eV), échelle symlog")
    save(fig, "fig_Ved_zoom")

print("\nFichiers finaux (largeur × hauteur, po) :")
for n, w, h in DONE: print(f"  {n:24s} {w:.2f} × {h:.2f}")
