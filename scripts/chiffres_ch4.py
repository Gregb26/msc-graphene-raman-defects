"""Chiffres complémentaires du chapitre 4, calculés depuis donnees/ (aucun calcul physique, seulement des lectures et des
statistiques sur les npz/csv de production). Complète donnees/ch4/table_v1_final.md pour les valeurs que la table ne donne pas :

  A. fig:M_map  : M̃_π, M̃_π*, M^L_∥ et M^NL_∥ sur toute la zone (grille élargie 27×27 de la 9×9), brut et aligné
  B. grille interne N_k^int : écarts 300 → 600 sur la fenêtre ±3 eV, la zone |ε − E_D| ≤ 0.3 eV et au point de Dirac
  C. fig:Ved    : cœur au site, décroissance, fond loin de la lacune (comparé à C_N), coin de la 5×5
  D. fig:M_locality : poids sur le site, décroissance sur les premières mailles, plancher
  E. dérivés    : fraction locale à K (tab:L_NL), A_cell·M̄(K), dispersion de max|M| en N (fig:M_scaling)

Sortie : donnees/ch4/chiffres_complementaires.csv (bloc, grandeur, valeur, unité, source) et .md (même contenu, lisible).
Usage : python scripts/chiffres_ch4.py
"""
import csv
from pathlib import Path

import numpy as np

from graphene_raman.config import load_production, results_dir, alignment_C

ROOT = Path(__file__).resolve().parents[1]            # scripts/ -> racine
CFG = load_production(verbose=False)
RES = Path(results_dir(CFG))                           # donnees/M2_plateau
OUT = ROOT / "donnees" / "ch4" / "chiffres_complementaires"
SIZES = ["5x5", "6x6", "7x7", "8x8", "9x9", "12x12"]
rows = []


def put(bloc, nom, valeur, unite, source):
    rows.append(dict(bloc=bloc, grandeur=nom, valeur=valeur, unite=unite, source=source))


def f(x, n=4):
    return float(f"{float(x):.{n}g}")


# ---------------- A. fig:M_map (9×9, grille 27×27)
Z = np.load(RES / "M_analysis.npz", allow_pickle=True)
kx, ky, K = Z["map_kx"], Z["map_ky"], Z["map_K"]
iK = int(np.argmin(np.hypot(kx - K[0], ky - K[1])))
kabs = np.hypot(kx, ky)
src = "M2_plateau/M_analysis.npz"
for key, nom in (("map_Vpi", "M̃_π"), ("map_Vpistar", "M̃_π*"), ("map_Lpar", "M^L_∥"), ("map_Npar", "M^NL_∥")):
    for var, suf in (("brut", ""), ("aligné", "_aligned")):
        v = Z[key + suf]
        put("A", f"{nom} ({var}) en K", f(v[iK]), "eV Å²", f"{src} : {key}{suf}")
        put("A", f"{nom} ({var}) min sur la zone", f(v.min()), "eV Å²", f"{src} : {key}{suf}")
        put("A", f"{nom} ({var}) max sur la zone", f(v.max()), "eV Å²", f"{src} : {key}{suf}")
        put("A", f"{nom} ({var}) |k'| du max", f(kabs[np.argmax(v)], 3), "Å⁻¹", f"{src} : {key}{suf}, map_kx, map_ky")
        sansK = np.delete(v, iK)
        put("A", f"{nom} ({var}) min / max hors K", f"{f(sansK.min())} / {f(sansK.max())}", "eV Å²", f"{src} : {key}{suf}")
diff = [k for k in ("map_Vpi", "map_Vpistar", "map_Lpar", "map_Npar")
        if np.count_nonzero(~np.isclose(Z[k], Z[k + "_aligned"], rtol=0, atol=1e-9))]
nd = {k: int(np.count_nonzero(~np.isclose(Z[k], Z[k + "_aligned"], rtol=0, atol=1e-9))) for k in diff}
put("A", "points k' où brut ≠ aligné", "; ".join(f"{k} : {n}" for k, n in nd.items()) or "aucun", "points", src)
for k in ("map_Vpi", "map_Vpistar", "map_Lpar", "map_Npar"):
    dlt = np.abs(Z[k + "_aligned"] - Z[k]); hors = np.delete(dlt, iK)
    put("A", f"{k} : |aligné − brut| en K / max hors K", f"{f(dlt[iK])} / {f(hors.max(), 3)}", "eV Å²", f"{src} : {k}, {k}_aligned")
put("A", "nombre de points k' de la carte", kx.size, "", src)

# ---------------- B. grille interne N_k^int (9×9, R_cut 3, 240², η 0.02)
nk = list(csv.DictReader(open(RES / "nkint_check_9x9.csv")))
by = {int(r["nk_int"]): r for r in nk}
src = "M2_plateau/nkint_check_9x9.csv"
for col, nom in (("medG", "médiane Γ N_cells, fenêtre ±3 eV"), ("medRe", "médiane Re Σ, fenêtre ±3 eV"),
                 ("z_medG", "médiane Γ N_cells, zone |ε − E_D| ≤ 0.3 eV"), ("z_medRe", "médiane Re Σ, zone |ε − E_D| ≤ 0.3 eV"),
                 ("G_ED", "Γ N_cells au point de Dirac (4 états en K)")):
    x300, x600 = float(by[300][col]), float(by[600][col])
    put("B", f"{nom} : 300² → 600²", f(100 * (x300 - x600) / x600, 3), "% (écart de 300² à 600²)", f"{src} : {col}")
    put("B", f"{nom} : valeurs 150² / 300² / 450² / 600²", " / ".join(f"{float(by[n][col]):.1f}" for n in (150, 300, 450, 600)), "meV", f"{src} : {col}")
g = [float(by[n]["G_ED"]) for n in (150, 300, 450, 600)]
put("B", "Γ(E_D) décroît de façon monotone avec N_k^int", "oui" if all(a > b for a, b in zip(g, g[1:])) else "non", "", f"{src} : G_ED")
put("B", "états dans la zone |ε − E_D| ≤ 0.3 eV / dans la fenêtre", f"{by[300]['z_n']} / {by[300]['n_states']}", "états", f"{src} : z_n, n_states")

# ---------------- C. fig:Ved (potentiel local dans le plan, non aligné ; C_N de la config)
V = np.load(RES / "ved_analysis.npz")
src = "M2_plateau/ved_analysis.npz"
for S in SIZES:
    site = float(V[f"{S}_site"]); r, v = V[f"{S}_rc_masked"], V[f"{S}_rad_masked"]; hb = float(V[f"{S}_halfbox"])
    put("C", f"{S} : V^L au site de la lacune", f(site), "eV", f"{src} : {S}_site")
    i3 = np.argmax(np.abs(v) < 1e-3 * site)
    put("C", f"{S} : distance où |V̄^L| < 10⁻³ × site (premier point)", f(r[i3], 3), "Å", f"{src} : {S}_rc_masked, {S}_rad_masked")
    far = (r >= 0.75 * hb) & (r <= hb)
    put("C", f"{S} : V̄^L moyen pour 0.75 r_max ≤ r ≤ r_max (r_max = {hb:.2f} Å)", f(v[far].mean(), 3), "eV", f"{src} : {S}_rad_masked")
    put("C", f"{S} : V̄^L min / max pour 0.75 r_max ≤ r ≤ r_max", f"{f(v[far].min(), 3)} / {f(v[far].max(), 3)}", "eV", f"{src} : {S}_rad_masked")
    put("C", f"{S} : C_N (Kumagai–Oba)", f(alignment_C(CFG, S), 4), "eV", "config/production.json : alignment.C_N_eV")
for S in ("5x5", "9x9"):
    X, Y, M = V[f"{S}_map_X"], V[f"{S}_map_Y"], V[f"{S}_map"]
    i0 = np.unravel_index(np.argmax(M), M.shape); d = np.hypot(X - X[i0], Y - Y[i0])
    loin = d >= 0.95 * d.max()
    put("C", f"{S} : carte, max de V^L dans les 5 % les plus éloignés de la lacune (coins)", f(M[loin].max(), 3), "eV", f"{src} : {S}_map, {S}_map_X, {S}_map_Y")
    put("C", f"{S} : carte, médiane de V^L dans les 5 % les plus éloignés de la lacune", f(np.median(M[loin]), 3), "eV", f"{src} : {S}_map")

# ---------------- D. fig:M_locality (grilles élargies ; 5×5 et 8×8 aussi grossières)
L = np.load(RES / "mwr_locality.npz")
src = "M2_plateau/mwr_locality.npz"
for S in ("5x5", "8x8", "9x9", "12x12"):
    for grille in ("dense", "coarse"):
        if f"{S}_{grille}_w" not in L:
            continue
        d, w = L[f"{S}_{grille}_dist"], L[f"{S}_{grille}_w"]; w0 = float(w[np.argmin(d)])
        tag = "élargie" if grille == "dense" else "grossière"
        put("D", f"{S} {tag} : ‖M(0,0)‖", f(w0), "eV", f"{src} : {S}_{grille}_w")
        for R in (1, 2, 3, 5):
            sel = np.abs(d - R) < 0.5
            if sel.any():
                put("D", f"{S} {tag} : max ‖M(R,0)‖ pour |R| ∈ [{R - 0.5}, {R + 0.5}[ (a)", f(w[sel].max(), 3), "eV", f"{src} : {S}_{grille}_dist, _w")
        loin = d >= 6
        if loin.any():
            put("D", f"{S} {tag} : médiane / max de ‖M(R,0)‖ pour |R| ≥ 6 a", f"{f(np.median(w[loin]), 2)} / {f(w[loin].max(), 2)}", "eV", f"{src} : {S}_{grille}_w")
        put("D", f"{S} {tag} : |R| max de la boîte", f(d.max(), 3), "a", f"{src} : {S}_{grille}_dist")

# ---------------- E. dérivés : tab:L_NL, fig:M_scaling
A = float(Z["map_A_cell"])
put("E", "A_cell", f(A), "Å²", "M2_plateau/M_analysis.npz : map_A_cell")
for S in SIZES:
    L_, N_, La = float(Z[f"lnl_{S}_ReL"]), float(Z[f"lnl_{S}_ReNL"]), float(Z[f"lnl_{S}_ReL_aligned"])
    put("E", f"{S} : M̄^L(K) brut / aligné ; M̄^NL(K)", f"{f(L_)} / {f(La)} ; {f(N_)}", "eV", "M2_plateau/M_analysis.npz : lnl_<S>_ReL, _ReL_aligned, _ReNL")
    put("E", f"{S} : fraction locale M̄^L / (M̄^L + M̄^NL), brut / aligné", f"{f(L_ / (L_ + N_), 3)} / {f(La / (La + N_), 3)}", "", "id.")
    put("E", f"{S} : A_cell (M̄^L + M̄^NL)(K), brut / aligné", f"{f(A * (L_ + N_))} / {f(A * (La + N_))}", "eV Å²", "id. et map_A_cell")
dense = {S: float(Z[f"scale_{S}_dense"]) for S in SIZES if f"scale_{S}_dense" in Z}
coarse = {S: float(Z[f"scale_{S}_coarse"]) for S in SIZES if f"scale_{S}_coarse" in Z}
vals = np.array(list(dense.values()))
put("E", "max|M| grille élargie, " + ", ".join(dense), " / ".join(f"{x:.3f}" for x in vals), "eV", "M2_plateau/M_analysis.npz : scale_<S>_dense")
put("E", "max|M| élargie : (max − min) / moyenne sur les six tailles", f(100 * (vals.max() - vals.min()) / vals.mean(), 3), "%", "id.")
for fam, ss in (("3m", ("6x6", "9x9", "12x12")), ("non-3m", ("5x5", "7x7", "8x8"))):
    x = np.array([dense[s] for s in ss]); put("E", f"max|M| élargie : (max − min) / moyenne, famille {fam}", f(100 * (x.max() - x.min()) / x.mean(), 3), "%", "id.")
for S in coarse:
    put("E", f"{S} : max|M| grossière / élargie − 1", f(100 * (coarse[S] / dense[S] - 1), 3), "%", "M2_plateau/M_analysis.npz : scale_<S>_coarse, _dense")

# ---------------- sortie
OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT.with_suffix(".csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["bloc", "grandeur", "valeur", "unite", "source"]); w.writeheader(); w.writerows(rows)
titres = {"A": "A. fig:M_map (9×9, grille élargie 27×27)", "B": "B. Grille interne N_k^int (9×9, R_cut 3, 240², η 0.02 eV)",
          "C": "C. fig:Ved (potentiel local dans le plan, non aligné)", "D": "D. fig:M_locality",
          "E": "E. Dérivés : tab:L_NL et fig:M_scaling"}
with open(OUT.with_suffix(".md"), "w", encoding="utf-8") as fh:
    fh.write("# Chiffres complémentaires du chapitre 4\n\nGénéré par `scripts/chiffres_ch4.py` depuis `donnees/` (ne pas éditer). "
             "Sources relatives à `donnees/`.\n")
    for b, t in titres.items():
        fh.write(f"\n## {t}\n\n| grandeur | valeur | unité | source |\n|---|---|---|---|\n")
        for r in rows:
            if r["bloc"] == b:
                fh.write(f"| {r['grandeur']} | {r['valeur']} | {r['unite']} | `{r['source']}` |\n")
print(f"{len(rows)} lignes → {OUT.with_suffix('.csv').relative_to(ROOT)}, .md")
