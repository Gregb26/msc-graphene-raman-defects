"""Tableaux du chapitre 4, générés depuis donnees/ et config/.

Couche d'organisation (décision du 2026-10-01) : les données restent rangées par sujet et par campagne dans donnees/,
sous les mêmes noms que dans graphene-raman ; ce script les range *par tableau du mémoire*. Chaque tableau est une
fonction qui déclare, cellule par cellule, la valeur affichée et sa source (fichier : clé [sélection]), vérifie la
cohérence entre fichiers quand deux sources portent la même grandeur, puis le script écrit :

  memoire/tables/<nom>.tex    le tabular seul ; la légende et le \\label restent dans le chapitre (\\input{tables/<nom>})
  memoire/tables/SOURCES.md   l'index : pour chaque tableau, chaque valeur affichée, la valeur lue et sa source

Aucun calcul physique : lectures, arithmétique élémentaire (écrite dans la source de la cellule) et mise en forme
(point décimal, X~\\%, nombres en mode math). Sortie déterministe (pas de date) : un tableau dont les données n'ont pas
changé est réécrit identique au bit.

Usage (depuis la racine, environnement de requirements.txt) :
  python scripts/make_tables.py                 # tous les tableaux et l'index
  python scripts/make_tables.py --only L_NL     # seulement certains .tex (l'index est toujours réécrit en entier)
  python scripts/make_tables.py --list          # liste des tableaux, sans rien écrire
  python scripts/make_tables.py --check         # compare à memoire/tables/ sans écrire ; code de sortie 1 si l'un diffère

Les tableaux du ch. 5 et de l'annexe D (paramètres) restent saisis à la main (décision du 2026-10-01).
"""
import argparse
import csv
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from graphene_raman.config import load_production, results_dir, campaigns_dir, alignment_C

ROOT = Path(__file__).resolve().parents[1]                  # scripts/ -> racine
DONNEES = ROOT / "donnees"
OUTDIR = ROOT / "memoire" / "tables"
CFG = load_production(verbose=False)
RES = Path(results_dir(CFG))                                # donnees/M2_plateau
CN_SRC = "config/production.json : alignment.C_N_eV"
SYM_CN = r"$C_N$"                                           # symbole de la constante d'alignement (à fixer au §4.1.5)
SIZES = ["5x5", "6x6", "7x7", "8x8", "9x9", "12x12"]
FAM_3M, FAM_NON3M = ["6x6", "9x9", "12x12"], ["5x5", "7x7", "8x8"]


# ------------------------------------------------------------------ lectures (avec cache)

_cache = {}


def rel(path):
    """Chemin affiché dans les sources : relatif à donnees/, sinon à la racine."""
    p = Path(path).resolve()
    try:
        return p.relative_to(DONNEES).as_posix()
    except ValueError:
        return p.relative_to(ROOT).as_posix()


def read_csv(path):
    key = ("csv", str(path))
    if key not in _cache:
        with open(path, newline="", encoding="utf-8") as fh:
            _cache[key] = list(csv.DictReader(fh))
    return _cache[key]


def read_json(path):
    key = ("json", str(path))
    if key not in _cache:
        with open(path, encoding="utf-8") as fh:
            _cache[key] = json.load(fh)
    return _cache[key]


def read_npz(path):
    key = ("npz", str(path))
    if key not in _cache:
        _cache[key] = np.load(path, allow_pickle=True)
    return _cache[key]


def csv_row(path, **match):
    """Unique ligne d'un csv dont les colonnes valent `match` (chaînes comparées telles quelles)."""
    hits = [r for r in read_csv(path) if all(r[k] == v for k, v in match.items())]
    if len(hits) != 1:
        sys.exit(f"[make_tables] {rel(path)} : {len(hits)} lignes pour {match} (une seule attendue)")
    return hits[0]


def gate(ok, message):
    """Contrôle de cohérence entre sources : arrête le script s'il échoue."""
    if not ok:
        sys.exit(f"[make_tables] contrôle échoué : {message}")


# ------------------------------------------------------------------ mise en forme

def fixed(x, nd, sign=False):
    """Décimales fixes, en mode math : $-20.5$, $+58.7$."""
    s = f"{x:+.{nd}f}" if sign else f"{x:.{nd}f}"
    if float(s) == 0:
        s = s.lstrip("+-")
    return f"${s}$"


def sig(x, n=2):
    """n chiffres significatifs, zéros de fin conservés : 2.0, 0.92, 32 (texte brut, sans $)."""
    if x == 0:
        return "0"
    r = float(f"{x:.{n - 1}e}")                             # arrondi d'abord (9.96 -> 10, pas 10.0)
    e = math.floor(math.log10(abs(r)))
    return f"{r:.{max(n - 1 - e, 0)}f}"


def pct(frac, n=2):
    """Fraction -> pourcentage du mémoire : 2.6~\\%."""
    return f"{sig(100 * frac, n)}~\\%"


def sci(x, n=2, mantisse=True):
    """Notation scientifique en mode math : $1.3\\times10^{-15}$ ; mantisse=False et mantisse 1 : $10^{-12}$."""
    m, e = f"{x:.{n - 1}e}".split("e")
    e = int(e)
    if not mantisse and float(m) == 1:
        return f"$10^{{{e}}}$"
    return f"${m}\\times10^{{{e}}}$"


def thr(x):
    """Seuil : un chiffre significatif ; $10^{-12}$ si la mantisse vaut 1, sinon $2\\times10^{-3}$."""
    return sci(x, n=1, mantisse=False)


def first_float(s):
    """Premier nombre d'une chaîne de csv (« 2e-3 (tolérance nscf) » -> 0.002)."""
    m = re.search(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", s)
    if not m:
        sys.exit(f"[make_tables] aucun nombre dans « {s} »")
    return float(m.group())


# ------------------------------------------------------------------ tableaux

@dataclass
class Cell:
    tex: str                 # texte LaTeX affiché
    src: str = ""            # source (fichier : clé [sélection]) ; vide pour un libellé
    raw: object = None       # valeur lue, pour l'index


def L(tex):
    return Cell(tex)


HLINE = r"\hline"


@dataclass
class Table:
    nom: str                 # memoire/tables/<nom>.tex
    label: str               # \label porté par le chapitre
    lieu: str                # section et place (corps / annexe)
    colspec: str
    head: list               # lignes d'en-tête LaTeX complètes
    cols: list               # nom court de chaque colonne, pour l'index
    rows: list               # listes de Cell, ou HLINE
    notes: list = field(default_factory=list)

    def sources(self):
        files = []
        for row in self.rows:
            if row == HLINE:
                continue
            for c in row:
                for part in c.src.split(" ; "):
                    f = part.split(" : ")[0].strip()
                    if f and f not in files:
                        files.append(f)
        return files

    def tex(self):
        body = [r for r in self.rows if r != HLINE]
        ncol = len(self.cols)
        for r in body:
            gate(len(r) == ncol, f"{self.nom} : ligne de {len(r)} cellules pour {ncol} colonnes")
        width = [max(len(r[j].tex) for r in body) for j in range(ncol)]
        out = [f"% Généré par scripts/make_tables.py : ne pas éditer (python scripts/make_tables.py --only {self.nom}).",
               f"% {self.label}, {self.lieu}. Valeurs et sources cellule par cellule : tables/SOURCES.md.",
               "% Sources : " + " ; ".join(self.sources()),
               f"\\begin{{tabular}}{{{self.colspec}}}",
               "    \\hline\\hline"]
        out += ["    " + h for h in self.head]
        out.append("    \\hline")
        for r in self.rows:
            if r == HLINE:
                out.append("    \\hline")
            else:
                out.append("    " + " & ".join(c.tex.ljust(w) for c, w in zip(r, width)).rstrip() + r" \\")
        out += ["    \\hline\\hline", "\\end{tabular}", ""]
        return "\n".join(out)

    def index_md(self):
        out = [f"## `{self.label}` — `tables/{self.nom}.tex` ({self.lieu})", ""]
        for n in self.notes:
            out.append(f"- {n}")
        if self.notes:
            out.append("")
        out += ["| ligne | colonne | affiché | valeur lue | source |", "|---|---|---|---|---|"]
        for r in self.rows:
            if r == HLINE:
                continue
            for c, name in zip(r, self.cols):
                if c.src:
                    raw = c.raw if not isinstance(c.raw, float) else repr(c.raw)
                    esc = lambda x: str(x).replace("|", "\\|")
                    out.append(f"| {esc(r[0].tex)} | {name} | {esc(c.tex)} | {esc(raw)} | `{esc(c.src)}` |")
        return "\n".join(out) + "\n"


# --- tab:échantillonnage (§4.1.6, corps)

def t_echantillonnage():
    f = RES / "sampling_table.csv"
    A = read_npz(RES / "M_analysis.npz")
    for S in SIZES:                                         # mêmes C_N pour le tableau et pour les produits M de R10
        gate(abs(alignment_C(CFG, S) - float(A[f"lnl_{S}_C_N_eV"])) < 1e-15, f"C_N de {S} : config ≠ M_analysis.npz")
    rows = []
    for N in (6, 9, 12, 5, 7, 8, 10, 11):
        r = csv_row(f, N=str(N))
        S = f"{N}x{N}"
        gate(int(r["N_mod_3"]) == N % 3, f"{rel(f)} : N_mod_3 de N = {N}")
        dE, vraw, C = float(r["dE_F_meV"]), float(r["Ved_radial_1.42A_meV"]), 1e3 * alignment_C(CFG, S)
        rows.append([L(f"{N}"), L(f"{N % 3}"),
                     Cell(fixed(dE, 1, sign=True), f"{rel(f)} : dE_F_meV [N = {N}]", dE),
                     Cell(fixed(C, 1, sign=True), f"{CN_SRC} [{S}] × 10³", C),
                     Cell(fixed(vraw - C, 1, sign=True),
                          f"{rel(f)} : Ved_radial_1.42A_meV [N = {N}] − {CN_SRC} [{S}] × 10³", vraw - C)])
        if N == 12:
            rows.append(HLINE)
    return Table("echantillonnage", "tab:échantillonnage", "§4.1.6, corps", "c c r r r",
                 [r"$N$ & $N \bmod 3$ & $\Delta E_F$ & " + SYM_CN + r" & $\bar V^\text{L}_\text{ed}(a_\text{CC})$ \\"],
                 ["N", "N mod 3", "ΔE_F (meV)", "C_N (meV)", "V̄^L(a_CC) aligné (meV)"], rows,
                 ["Toutes les valeurs en meV. V̄^L(a_CC) **aligné** = brut − C_N (décision du TODO, chantier 1) ; la colonne brute "
                  "n'est plus affichée (brut = aligné + C_N). ΔE_F ne dépend pas de l'alignement.",
                  "N = 10 et 11 : SCF de super-cellules seulement (pas de matrice M) ; leurs C_N viennent de la même source."])


# --- tab:L_NL (§4.1.6, corps)

def t_L_NL():
    fa, fl, ff = RES / "M_analysis.npz", RES / "level2_families.csv", RES / "lnl_frobenius.csv"
    A = read_npz(fa)
    rows = []
    for S in SIZES:
        N = int(S.split("x")[0])
        ReL, ReLa, ReNL = (float(A[f"lnl_{S}_{k}"]) for k in ("ReL", "ReL_aligned", "ReNL"))
        r2 = csv_row(fl, size=S)
        for col, v in (("ReML_K_eV", ReL), ("ReML_K_aligned_eV", ReLa), ("ReMNL_K_eV", ReNL)):
            gate(abs(float(r2[col]) - v) < 6e-5, f"{rel(fl)} : {col} [{S}] ≠ {rel(fa)}")
        # identité annoncée au TODO : à k = k′, l'alignement ajoute exactement N²|C_N|
        gate(abs((ReLa - ReL) - N * N * abs(alignment_C(CFG, S))) < 1e-8, f"{S} : M̄^L aligné − brut ≠ N²|C_N|")
        r = csv_row(ff, size=S)
        rb, ra = float(r["ratio_full"]), float(r["ratio_full_aligned"])
        rows.append([L(f"{N}"),
                     Cell(fixed(ReL, 3), f"{rel(fa)} : lnl_{S}_ReL", ReL),
                     Cell(fixed(ReLa, 3), f"{rel(fa)} : lnl_{S}_ReL_aligned", ReLa),
                     Cell(fixed(ReNL, 3), f"{rel(fa)} : lnl_{S}_ReNL", ReNL),
                     Cell(fixed(rb, 3), f"{rel(ff)} : ratio_full [{S}]", rb),
                     Cell(fixed(ra, 3), f"{rel(ff)} : ratio_full_aligned [{S}]", ra)])
    head = [r"& \multicolumn{2}{c}{$\bar M^\text{L}(K)$ (eV)} & $\bar M^\text{NL}(K)$ & \multicolumn{2}{c}{NL/L toute la BZ} \\",
            r"\cline{2-3}\cline{5-6}",
            r"$N$ & brut & aligné & (eV) & brut & aligné \\"]
    return Table("L_NL", "tab:L_NL", "§4.1.6, corps", "c c c c c c", head,
                 ["N", "M̄^L(K) brut (eV)", "M̄^L(K) aligné (eV)", "M̄^NL(K) (eV)", "NL/L BZ brut", "NL/L BZ aligné"], rows,
                 ["Brut et aligné côte à côte (décision du 2026-10-01, R10 D6). M̄^NL ne dépend pas de l'alignement.",
                  "Contrôles : `level2_families.csv` = `M_analysis.npz` (ReML_K, ReML_K_aligned, ReMNL_K) ; aligné − brut = N²|C_N| "
                  "à 1e-8 eV près pour les six tailles.",
                  "N = 5, 7, 8 : grilles élargies 25², 28², 32² sans K ; « K » y est le point de grille le plus proche "
                  "(`lnl_<S>_dK` = 0.055, 0.050, 0.043 Å⁻¹) — à dire dans la légende."])


# --- tab:rcut_M (§4.1.6 → annexe D)

def t_rcut_M():
    f = RES / "m_rcut_convergence.csv"
    c2 = read_json(Path(campaigns_dir(CFG, "kaasbjerg", "r10_c2_results.json")))["rcut"]
    rows = []
    for R in range(7):
        r9, r12 = csv_row(f, size="9x9", R_cut=str(R)), csv_row(f, size="12x12", R_cut=str(R))
        gate(r9["n_sites"] == r12["n_sites"], f"{rel(f)} : n_sites différent entre 9x9 et 12x12 à R_cut {R}")
        cells = [L(f"{R}"), Cell(r9["n_sites"], f"{rel(f)} : n_sites [R_cut = {R}]", int(r9["n_sites"]))]
        for S, r in (("9x9", r9), ("12x12", r12)):
            j = [x for x in c2[S]["plateau_ws"] if x["R_cut"] == R][0]
            for col in ("sv_mismatch_pi_blocks", "diag_max_dM_over_max"):
                v = float(r[col])
                gate(abs(v - j[col]) <= 1e-4 * abs(j[col]), f"{rel(f)} : {col} [{S}, R_cut {R}] ≠ r10_c2_results.json plateau_ws")
                cells.append(Cell(pct(v), f"{rel(f)} : {col} [{S}, R_cut = {R}]", v))
        rows.append(cells)
    head = [r"& & \multicolumn{2}{c}{$9\times9$} & \multicolumn{2}{c}{$12\times12$} \\",
            r"$R_\text{cut}$ & Nombre de cellules & $\pi$--$\pi^*$ & diag. & $\pi$--$\pi^*$ & diag. \\"]
    return Table("rcut_M", "tab:rcut_M", "§4.1.6 → annexe D", "c c cc cc", head,
                 ["R_cut", "cellules", "9x9 π–π*", "9x9 diag.", "12x12 π–π*", "12x12 diag."], rows,
                 ["Production finale : alignement de Kumagai–Oba et étiquettes de Wigner-Seitz ; contrôle : le csv = "
                  "`kaasbjerg/r10_c2_results.json` : rcut.<S>.plateau_ws à 1e-4 près. Grille fine 60² (colonne `fine_grid`).",
                  "Deux chiffres significatifs."])


# --- tab:tests_M (§4.1.6 → annexe D)

def t_tests_M():
    fk, ft, fa = RES / "ks_reconstruction.npz", RES / "M_tests_summary.csv", RES / "M_analysis.npz"
    K, A = read_npz(fk), read_npz(fa)

    def ks(grid, key):
        vals = {S: float(K[f"{S}_{grid}_{key}"]) for S in SIZES}
        return vals, f"{rel(fk)} : <S>_{grid}_{key}, six tailles"

    def test(name):
        return csv_row(ft, test=name)

    rows = []
    v, s = ks("coarse", "max_meV")
    lo, hi = 1e3 * min(v.values()), 1e3 * max(v.values())
    rows.append([L(r"Reconstruction KS, grille $N\times N$"), L(r"$\max|\varepsilon_\text{calc}-\varepsilon_\text{QE}|$"),
                 Cell(f"{sig(lo)}--{sig(hi)}~$\\mu$eV", s + " (min–max, × 10³)", f"{lo:.4g}–{hi:.4g} µeV"), L("---")])
    v, s = ks("coarse", "offdiag_rel")
    rows.append([L(r"\quad éléments hors diagonaux"), L(r"rel. à $\max|\varepsilon|$"),
                 Cell("$\\le " + sci(max(v.values()))[1:], s + " (max)", max(v.values())), L("---")])
    v, s = ks("dense", "max_meV")
    lo, hi = min(v.values()), max(v.values())
    rows.append([L(r"Reconstruction KS, grille élargie"), L(r"$\max|\varepsilon_\text{calc}-\varepsilon_\text{QE}|$"),
                 Cell(f"{sig(lo)}--{sig(hi)}~meV", s + " (min–max)", f"{lo:.4g}–{hi:.4g} meV"), L("---")])
    herm = {S: first_float(test(f"hermiticité M dense {S}")["valeur"]) for S in SIZES}
    for S in SIZES:
        gate(abs(herm[S] - float(A[f"herm_{S}"])) <= 0.01 * herm[S], f"hermiticité {S} : {rel(ft)} ≠ {rel(fa)} herm_{S}")
    seuil = first_float(test("hermiticité M dense 9x9")["seuil"])
    rows.append([L(r"Hermiticité ($M$ élargi, six tailles)"), L(r"$\max|M-M^\dagger|/\max|M|$"),
                 Cell("$\\le " + sci(max(herm.values()))[1:], f"{rel(ft)} : valeur [hermiticité M dense <S>, six tailles] (max)",
                      max(herm.values())),
                 Cell(thr(seuil), f"{rel(ft)} : seuil", seuil)])
    for grille, tex in (("8 fichiers grossiers (N = 5x5, 6x6, 7x7, 8x8, 9x9, 9x9 (128 b), 10x10, 12x12)",
                         r"Application directe de $V_\text{ed}$, $N\times N$"),
                        ("6 fichiers denses (N = 5x5, 6x6, 7x7, 8x8, 9x9, 12x12)", r"\quad grilles élargies")):
        name = f"porte A.2 : ΔV appliqué aux états de Bloch purs contre M2/N_cells, {grille}"
        r = test(name)
        mL = re.search(r"L ([0-9.e+-]+)", r["valeur"]).group(1)
        mN = re.search(r"NL ([0-9.e+-]+)", r["valeur"]).group(1)
        vmax = max(float(mL), float(mN))                    # le plus grand des deux écarts (L et NL) ; les deux dans l'index
        rows.append([L(tex), L(r"$\max|\Delta M|$, L et NL" if "grossiers" in grille else "idem"),
                     Cell("$\\le " + sci(vmax)[1:] + "~eV", f"{rel(ft)} : valeur [{name}] (max de L et NL)", r["valeur"]),
                     Cell(thr(first_float(r["seuil"])) + "~eV", f"{rel(ft)} : seuil", r["seuil"])])
    for name, tex, quant in (
            ("padding : noyau dense à p=1 vs noyau N×N, 9x9", "Remplissage, coefficients coïncidents",
             r"$\max|\Delta M^\text{L}|/\max|M^\text{L}|$"),
            ("padding : k coïncidents, bandes 1–15, 9x9", r"Remplissage, points $\kv$ communs", "écart rel. valeurs singulières"),
            ("fermeture Fourier Wannier (k → R → k), 9x9", r"Fourier $\kv\to\Rv\to\kv$", r"$\max|\Delta M|/\max|M|$"),
            ("fermeture Bloch → Wannier → Bloch (5 bandes), 9x9", r"Bloch$\to$Wannier$\to$Bloch", "écart rel. valeurs singulières")):
        r = test(name)
        gate(r["verdict"] == "OK", f"{rel(ft)} : verdict de « {name} »")
        v, s = first_float(r["valeur"]), first_float(r["seuil"])
        rows.append([L(tex), L(quant), Cell(sci(v), f"{rel(ft)} : valeur [{name}]", v),
                     Cell(thr(s), f"{rel(ft)} : seuil [{name}]", r["seuil"])])
    scale = {S: float(A[f"scale_{S}_dense"]) for S in SIZES}
    for fam, tag, tex in ((FAM_3M, "famille 3m (N = 6, 9, 12)", r"Convention intensive, $N = 6, 9, 12$"),
                          (FAM_NON3M, "famille non-3m (N = 5, 7, 8)", r"\quad $N = 5, 7, 8$")):
        name = f"convention intensive (cellule unitaire), {tag}"
        r = test(name)
        v = first_float(r["valeur"])
        x = np.array([scale[S] for S in fam])
        gate(abs((x.max() - x.min()) / x.mean() - v) < 0.005 * v + 5e-4, f"{name} : csv ≠ M_analysis.npz scale_<S>_dense")
        rows.append([L(tex), L(r"$(\max-\min)/\text{moy.}$ de $\max|M|$" if fam is FAM_3M else "idem"),
                     Cell(sci(v), f"{rel(ft)} : valeur [{name}]", v),
                     Cell(thr(first_float(r["seuil"])), f"{rel(ft)} : seuil", r["seuil"])])
    return Table("tests_M", "tab:tests_M", "§4.1.6 → annexe D", "l l l l", [r"Test & Quantité & Valeur & Seuil \\"],
                 ["test", "quantité", "valeur", "seuil"], rows,
                 ["Ligne « 16 → 20 bandes » retirée (non rejouable avec M2 ; TODO). Ajouts : application directe de V_ed "
                  "(porte A.2, toutes les tailles ; valeur affichée = le plus grand des écarts L et NL) et convention intensive par famille "
                  "(remplace la ligne sur six tailles).",
                  "Hermiticité : maximum sur les six tailles (la légende actuelle dit « valeur de la 9×9 sauf mention »). "
                  "Reconstruction KS : fourchette sur les six tailles. Deux chiffres significatifs.",
                  "Non repris (à trancher) : « g0 par lots vs référence » (1.2e-14) et « test d'or » (1.8e-13), qui sont des "
                  "tests de la chaîne T (le second est dans `tab:tests_T`) ; portes D6 de l'alignement (`M_analysis.npz` : align_gate_*)."])


# --- tab:convergence_gamma (§4.3.5 → annexe D)

def t_convergence_gamma():
    f, f2 = RES / "level1_summary.csv", RES / "level2_summary.csv"
    rows = []
    for S in FAM_3M + FAM_NON3M:
        N = int(S.split("x")[0])
        cells = [L(f"{N}"), L(f"{N % 3}")]
        for R in range(5):
            r = csv_row(f, size=S, R_cut=str(R), grid="240", eta_eV="0.02")
            v = float(r["median_Gamma_Ncells_meV"])
            cells.append(Cell(f"{v:.0f}", f"{rel(f)} : median_Gamma_Ncells_meV [{S}, R_cut = {R}, 240, 0.02]", v))
        prod = float(csv_row(f2, size=S)["median_Gamma_Ncells_meV"])
        gate(abs(prod - cells[2 + 3].raw) < 1e-3, f"{S} : level1 R_cut 3 ≠ level2_summary.csv")
        rows.append(cells)
        if S == "12x12":
            rows.append(HLINE)
    head = [r"$N$ & $N \bmod 3$ & $R_\text{cut}=0$ & 1 & 2 & 3 & 4 \\"]
    return Table("convergence_gamma", "tab:convergence_gamma", "§4.3.5 → annexe D", "c c ccccc", head,
                 ["N", "N mod 3", "R_cut 0", "R_cut 1", "R_cut 2", "R_cut 3", "R_cut 4"], rows,
                 ["Médiane de Γ N_cells (meV), grille de sortie 240², η = 0.02 eV, grille interne 300², fenêtre ±3 eV ; "
                  "colonne R_cut = 4 remplie pour les six tailles (TODO). Contrôle : R_cut 3 = `level2_summary.csv`."])


# --- tab:tests_T (§4.3.5 → annexe D)

def t_tests_T():
    ft, fn, fl, fr = (RES / "M_tests_summary.csv", RES / "nkint_check_9x9.csv", RES / "level1_summary.csv",
                      RES / "resonance_9x9.npz")
    rows = []
    name = "test d'or (local vs compute_T), 5×5 dense"
    r = csv_row(ft, test=name)
    v, s = first_float(r["valeur"]), first_float(r["seuil"])
    rows.append([L(r"Référence, $5\times5$"), L(r"$\max|\Gamma_\text{loc}-\Gamma_\text{dense}|/\max\Gamma$"),
                 Cell(sci(v), f"{rel(ft)} : valeur [{name}]", v), Cell(thr(s), f"{rel(ft)} : seuil", s)])
    m300, m600 = (float(csv_row(fn, nk_int=n)["medG"]) for n in ("300", "600"))
    prod = float(csv_row(fl, size="9x9", R_cut="3", grid="240", eta_eV="0.02")["median_Gamma_Ncells_meV"])
    gate(abs(m300 - prod) < 1e-3, "nkint_check_9x9.csv nk 300 ≠ production (level1_summary.csv)")
    d = abs(m300 - m600) / m600
    rows.append([L(r"Grille interne, $300^2\to600^2$"), L("écart rel. sur la médiane"),
                 Cell(sci(d), f"{rel(fn)} : |medG[300] − medG[600]| / medG[600]", d), L("---")])
    rows.append([L(r"Hermiticité de $M_\text{loc}$, $5\times5$"), L(r"$\max|M_\text{loc}-M_\text{loc}^\dagger|$"),
                 Cell(sci(1.3e-14), "ch4/NOTES_TGAMMA.md : l. 120 (C5, golden 5×5 dense M2, en prose seulement)", "1,3e-14"),
                 Cell(thr(1e-10), "ch4/NOTES_TGAMMA.md : l. 48 (garde-fou b)", "1e-10")])
    Z = read_npz(fr)
    E, G, ED = Z["E_out"], Z["G_T"], float(Z["E_D"])
    win = np.abs(E - ED) <= CFG["e_window_eV"]
    gate(abs(1e3 * np.nanmedian(G[win]) - float(Z["median_GT_states_meV"])) < 1e-6, f"{rel(fr)} : médiane de G_T ≠ median_GT_states_meV")
    gmin = float(np.nanmin(G[win]))
    rows.append([L("Positivité"), L(r"$\min_{n\kv}\Gamma_{n\kv}N_\text{cells}$"),
                 Cell(f"${gmin:.2f}$~eV", f"{rel(fr)} : min de G_T sur |E_out − E_D| ≤ {CFG['e_window_eV']} eV (eV)", gmin),
                 Cell(r"$-10^{-8}$~eV", "ch4/NOTES_TGAMMA.md : l. 122 (C7)", "-1e-8")])
    return Table("tests_T", "tab:tests_T", "§4.3.5 → annexe D", "l l l l", [r"Test & Quantité & Valeur & Seuil \\"],
                 ["test", "quantité", "valeur", "seuil"], rows,
                 ["Lignes 6×6, 12×12 (non rejoués avec M2) et grille d'énergie (v1 seulement) retirées (TODO).",
                  "Hermiticité de M_loc : **aucune valeur lisible par machine** ; seule valeur v2 connue = golden 5×5 dense "
                  "(NOTES_TGAMMA C5, 1.3e-14) ; rien pour la 9×9 de production. À trancher : garder cette ligne ou la retirer "
                  "(l'hermiticité de M est déjà dans tab:tests_M).",
                  "Positivité : minimum réel sur les 41 266 états de la fenêtre (9×9 de production) au lieu de « ≥ 0 »."])


TABLES = {f.__name__[2:]: f for f in (t_echantillonnage, t_L_NL, t_rcut_M, t_tests_M, t_convergence_gamma, t_tests_T)}


def index_md(tables):
    head = ("# Sources des tableaux du mémoire\n\n"
            "Généré par `scripts/make_tables.py` (ne pas éditer). Une ligne par valeur affichée : texte LaTeX, valeur lue et "
            "source (`fichier : clé [sélection]`, chemins relatifs à `donnees/`, sauf `config/`). Les remarques de chaque "
            "tableau notent les choix de présentation et les cellules sans source lisible par machine.\n\n")
    return head + "\n".join(t.index_md() for t in tables)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", nargs="+", choices=list(TABLES), help="tableaux à écrire")
    ap.add_argument("--list", action="store_true", help="liste des tableaux, sans rien écrire")
    ap.add_argument("--check", action="store_true", help="compare à memoire/tables/ sans écrire")
    a = ap.parse_args()
    if a.list:
        for nom, fn in TABLES.items():
            t = fn()
            print(f"{nom:20s} {t.label:24s} {t.lieu}")
        return
    tables = [fn() for fn in TABLES.values()]
    files = {OUTDIR / f"{t.nom}.tex": t.tex() for t in tables if not a.only or t.nom in a.only}
    files[OUTDIR / "SOURCES.md"] = index_md(tables)
    if a.check:
        bad = [p for p, s in files.items() if not p.exists() or p.read_text(encoding="utf-8") != s]
        for p in bad:
            print(f"[make_tables] différent ou absent : {p.relative_to(ROOT)}")
        print(f"[make_tables] {len(files) - len(bad)}/{len(files)} fichiers à jour")
        sys.exit(1 if bad else 0)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    for p, s in files.items():
        p.write_text(s, encoding="utf-8")
        print(f"[make_tables] {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
