"""
Tableaux du chapitre 4, générés depuis donnees/ et config/. C : tableaux dans le corps du texte. A : tableaux en annexe. Le script retourne :

    memoire/tables/<nom>.tex    le tabular seul, la légende et le \\label restent dans le chapitre (\\input{tables/<nom>}).
    memoire/tables/SOURCES.md   l'index : pour chaque tableau, chaque valeur affichée, la valeur lue et sa source.

<nom> prend les valeurs : 

    C : t_echantilonnage
    C : t_L_NL
    C : t_kaasbjerg
    A : t_rcut_M
    A : t_tests_M
    A : tests_T
    A : t_convergence_gamma
    A : t_grille_interne

Usage : depuis la racine et dans l'environnement de requirements.txt : 

    .venv/bin/python scripts/make_tables.py                 # tous les tableaux e
    .venv/bin/python scripts/make_tables.py --only <nom>    # un seul tableau, spéficié par <nom>
    .venv/bin/python scripts/make_tables.py --list          # liste des tableaux, sans rien écrire
    .venv/bin/python scripts/make_tables.py --check         # compare à memoire/tables/ sans écrire ; code de sortie 1 si l'un diffère, à figer une fois que le chap4 est verrouillé seulement.
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
SYM_CN = r"$\Delta V_\text{PA}^{(N)}$"                                           # symbole de la constante d'alignement 
SIZES = ["5x5", "6x6", "7x7", "8x8", "9x9", "12x12"]
FAM_3M, FAM_NON3M = ["6x6", "9x9", "12x12"], ["5x5", "7x7", "8x8"]


# lectures 

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


# mise en forme

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


# tableaux

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


# tab:échantillonnage 

def t_echantillonnage():
    """Décision G du 2026-10-03 : tableau dans la référence du vide (brut, tel que sorti de QE) — ΔE_F et V̄^L(a_CC) non
    alignés, pas de colonne C_N ni d'écart-type du vide. Les valeurs alignées (brut − C_N) ne sont plus affichées."""
    f = RES / "sampling_table.csv"
    rows = []
    for N in (6, 9, 12, 5, 7, 8, 10, 11):
        r = csv_row(f, N=str(N))
        gate(int(r["N_mod_3"]) == N % 3, f"{rel(f)} : N_mod_3 de N = {N}")
        dE, vraw = float(r["dE_F_meV"]), float(r["Ved_radial_1.42A_meV"])
        rows.append([L(f"{N}"), L(f"{N % 3}"),
                     Cell(fixed(dE, 1, sign=True), f"{rel(f)} : dE_F_meV [N = {N}]", dE),
                     Cell(fixed(vraw, 1, sign=True), f"{rel(f)} : Ved_radial_1.42A_meV [N = {N}]", vraw)])
        if N == 12:
            rows.append(HLINE)
    return Table("echantillonnage", "tab:échantillonnage", "§4.1.5, corps", "c c r r",
                 [r"$N$ & $N \bmod 3$ & $\Delta E_F$ & $\bar V^\text{L}_\text{ed}(a_\text{CC})$ \\"],
                 ["N", "N mod 3", "ΔE_F (meV)", "V̄^L(a_CC) brut (meV)"], rows,
                 ["Toutes les valeurs en meV, **brutes** (référence du vide, décision G du 2026-10-03) : ni ΔE_F ni V̄^L(a_CC) "
                  "ne sont alignés ; les valeurs alignées valent brut − C_N (`config/production.json : alignment.C_N_eV`).",
                  "N = 10 et 11 : SCF de super-cellules seulement (pas de matrice M)."])


# tab:L_NL

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
    return Table("L_NL", "tab:L_NL", "§4.1.5, corps", "c c c c c c", head,
                 ["N", "M̄^L(K) brut (eV)", "M̄^L(K) aligné (eV)", "M̄^NL(K) (eV)", "NL/L BZ brut", "NL/L BZ aligné"], rows,
                 ["Brut et aligné côte à côte (décision du 2026-10-01, R10 D6). M̄^NL ne dépend pas de l'alignement.",
                  "Contrôles : `level2_families.csv` = `M_analysis.npz` (ReML_K, ReML_K_aligned, ReMNL_K) ; aligné − brut = N²|C_N| "
                  "à 1e-8 eV près pour les six tailles.",
                  "N = 5, 7, 8 : grilles élargies 25², 28², 32² sans K ; « K » y est le point de grille le plus proche "
                  "(`lnl_<S>_dK` = 0.055, 0.050, 0.043 Å⁻¹) — à dire dans la légende."])

# tab:rcut_M

def t_rcut_M():
    f = RES / "m_rcut_convergence.csv"
    c2p = Path(campaigns_dir(CFG, "kaasbjerg", "r10_c2_results.json"))
    c2 = read_json(c2p)["rcut"]
    rows = []
    for R in range(7):
        r9, r12 = csv_row(f, size="9x9", R_cut=str(R)), csv_row(f, size="12x12", R_cut=str(R))
        gate(r9["n_sites"] == r12["n_sites"], f"{rel(f)} : n_sites différent entre 9x9 et 12x12 à R_cut {R}")
        cells = [L(f"{R}"), Cell(r9["n_sites"], f"{rel(f)} : n_sites [R_cut = {R}]", int(r9["n_sites"]))]
        for S, r in (("9x9", r9), ("12x12", r12)):
            jb = [x for x in c2[S]["tel_quel"] if x["R_cut"] == R][0]          # brut (non aligné), étiquettes brutes
            ja = [x for x in c2[S]["plateau_ws"] if x["R_cut"] == R][0]        # aligné (Kumagai–Oba), Wigner-Seitz = csv
            for col in ("sv_mismatch_pi_blocks", "diag_max_dM_over_max"):
                v = float(jb[col])
                cells.append(Cell(pct(v), f"{rel(c2p)} : rcut.{S}.tel_quel.{col} [R_cut = {R}]", v))
            for col in ("sv_mismatch_pi_blocks", "diag_max_dM_over_max"):
                v = float(r[col])
                gate(abs(v - ja[col]) <= 1e-4 * abs(ja[col]), f"{rel(f)} : {col} [{S}, R_cut {R}] ≠ r10_c2_results.json plateau_ws")
                cells.append(Cell(pct(v), f"{rel(f)} : {col} [{S}, R_cut = {R}]", v))
        rows.append(cells)
    head = [r"& & \multicolumn{4}{c}{$9\times9$} & \multicolumn{4}{c}{$12\times12$} \\",
            r"\cline{3-6}\cline{7-10}",
            r"& & \multicolumn{2}{c}{brut} & \multicolumn{2}{c}{aligné} & \multicolumn{2}{c}{brut} & \multicolumn{2}{c}{aligné} \\",
            r"$R_\text{cut}$ & Cellules & $\pi$--$\pi^*$ & diag. & $\pi$--$\pi^*$ & diag. & $\pi$--$\pi^*$ & diag. & $\pi$--$\pi^*$ & diag. \\"]
    return Table("rcut_M", "tab:rcut_M", "§4.1.5 → annexe D", "c c cc cc cc cc", head,
                 ["R_cut", "cellules", "9x9 brut π–π*", "9x9 brut diag.", "9x9 aligné π–π*", "9x9 aligné diag.",
                  "12x12 brut π–π*", "12x12 brut diag.", "12x12 aligné π–π*", "12x12 aligné diag."], rows,
                 ["Brut = matrices non alignées (`rcut.<S>.tel_quel`, étiquettes brutes) ; aligné = production finale "
                  "(alignement de Kumagai–Oba, étiquettes de Wigner-Seitz), lu dans le csv et contrôlé contre "
                  "`kaasbjerg/r10_c2_results.json` : rcut.<S>.plateau_ws à 1e-4 près (décision du 2026-10-03 : les deux côte à côte). "
                  "Grille de sortie 60² (colonne `fine_grid`).",
                  "Deux chiffres significatifs."])


# tab:alignement (bloc Alignement du potentiel, §4.1.5 ; demandé par G le 2026-10-03)

def t_alignement():
    """Constante d'alignement selon cinq schémas, dix tailles (18, 24, 27 retirées : vide anormal, décision G du 2026-10-04) :
    (A) nous (sites à d ≥ 0.75 r_max), (B) Kumagai–Oba 2D (hors du cercle inscrit, d ≥ N a/2), (C) Kumagai–Oba 3D tel quel
    (hors de la sphère inscrite, d ≥ min(N a/2, c/2) = c/2 dès N ≥ 7), (D) site unique de Lu et al., (E) vide (ΔV brut pour
    |z| > 5 Å, R10 C.6). Moyenne ± rms (écart-type de population des potentiels de site, ddof 0) ; vide : moyenne ± écart-type."""
    Z = read_npz(DONNEES / "ch4" / "alignement_regions.npz")
    c6p = Path(campaigns_dir(CFG, "alignement", "r10_c6_results.json")); c6 = read_json(c6p)["sizes"]
    src_z = rel(DONNEES / "ch4" / "alignement_regions.npz")
    rows = []
    for S in [str(x) for x in Z["sizes"]]:
        N = int(Z[f"{S}_N"])
        if N in (18, 24, 27):
            continue
        gate(abs(float(Z[f"{S}_meanA"]) - alignment_C(CFG, S)) < 1e-12, f"{src_z} : meanA de {S} ≠ C_N de la config")
        def pm(m, r, src):
            return Cell(f"${1e3 * m:+.1f} \\pm {1e3 * r:.1f}$", src, (1e3 * m, 1e3 * r))
        cells = [L(f"{N}"),
                 pm(float(Z[f"{S}_meanA"]), float(Z[f"{S}_rmsA"]), f"{src_z} : {S}_meanA, {S}_rmsA"),
                 pm(float(Z[f"{S}_meanB"]), float(Z[f"{S}_rmsB"]), f"{src_z} : {S}_meanB, {S}_rmsB"),
                 pm(float(Z[f"{S}_meanC"]), float(Z[f"{S}_rmsC"]), f"{src_z} : {S}_meanC, {S}_rmsC"),
                 Cell(fixed(1e3 * float(Z[f"{S}_Lu"]), 1, sign=True), f"{src_z} : {S}_Lu", 1e3 * float(Z[f"{S}_Lu"])),
                 Cell(f"${c6[S]['vacuum_mean_meV']:+.1f} \\pm {c6[S]['vacuum_std_meV']:.1f}$",
                      f"{rel(c6p)} : sizes.{S}.vacuum_mean_meV, vacuum_std_meV", (c6[S]["vacuum_mean_meV"], c6[S]["vacuum_std_meV"]))]
        rows.append(cells)
        if N == 12:
            rows.append(HLINE)
    head = [r"$N$ & (A) Nous & (B) Kumagai-Oba 2D & (C) Kumagai-Oba 3D & (D) Lu \textit{et al.} & (E) Vide \\"]
    return Table("alignement", "tab:alignement", "§4.1.5, corps (bloc Alignement du potentiel)", "c r r r r r", head,
                 ["N", "(A) nous ± rms (meV)", "(B) K–O 2D ± rms (meV)", "(C) K–O 3D ± rms (meV)", "(D) Lu et al., site unique (meV)", "(E) vide ± écart-type (meV)"], rows,
                 ["Toutes les valeurs en meV, potentiels bruts. (A) = production (`config/production.json : alignment.C_N_eV`, contrôlé au bit) ; "
                  "(B) Kumagai–Oba en 2D : cellule de Wigner-Seitz plane, sites hors du cercle inscrit ; (C) Kumagai–Oba 3D tel quel : hors de la sphère "
                  "inscrite, de rayon c/2 = 7.94 Å dès N ≥ 7 (la hauteur de boîte borne la région) ; (D) site unique publié (Lu et al. 2019) ; "
                  "(E) vide : moyenne de ΔV brut pour |z| > 5 Å (R10 C.6). Tailles 18, 24, 27 retirées (vide anormal, constat ouvert 1 de "
                  "`NOTES_TGAMMA.md` ; décision G du 2026-10-04) ; colonne famille retirée (même décision).",
                  "rms = écart-type de population des potentiels de site de la région (ddof 0) ; pour le vide, écart-type sur la grille.",
                  "Les tailles 15, 21 et 10, 11 n'ont que le SCF (pas de matrice M)."])


# tab:tests_M

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
    return Table("tests_M", "tab:tests_M", "§4.1.5 → annexe D", "l l l l", [r"Test & Quantité & Valeur & Seuil \\"],
                 ["test", "quantité", "valeur", "seuil"], rows,
                 ["Ligne « 16 → 20 bandes » retirée (non rejouable avec M2 ; TODO). Ajouts : application directe de V_ed "
                  "(porte A.2, toutes les tailles ; valeur affichée = le plus grand des écarts L et NL) et convention intensive par famille "
                  "(remplace la ligne sur six tailles).",
                  "Hermiticité : maximum sur les six tailles (la légende actuelle dit « valeur de la 9×9 sauf mention »). "
                  "Reconstruction KS : fourchette sur les six tailles. Deux chiffres significatifs.",
                  "Non repris (à trancher) : « g0 par lots vs référence » (1.2e-14) et « test d'or » (1.8e-13), qui sont des "
                  "tests de la chaîne T (le second est dans `tab:tests_T`) ; portes D6 de l'alignement (`M_analysis.npz` : align_gate_*)."])


# tab:convergence_gamma 

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
    return Table("convergence_gamma", "tab:convergence_gamma", "§4.2.5 → annexe D", "c c ccccc", head,
                 ["N", "N mod 3", "R_cut 0", "R_cut 1", "R_cut 2", "R_cut 3", "R_cut 4"], rows,
                 ["Médiane de Γ N_cells (meV), grille de sortie 240², η = 0.02 eV, grille interne 300², fenêtre ±3 eV ; "
                  "colonne R_cut = 4 remplie pour les six tailles (TODO). Contrôle : R_cut 3 = `level2_summary.csv`."])


# tab:tests_T

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
    Z = read_npz(fr)
    E, G, ED = Z["E_out"], Z["G_T"], float(Z["E_D"])
    win = np.abs(E - ED) <= CFG["e_window_eV"]
    gate(abs(1e3 * np.nanmedian(G[win]) - float(Z["median_GT_states_meV"])) < 1e-6, f"{rel(fr)} : médiane de G_T ≠ median_GT_states_meV")
    gmin = float(np.nanmin(G[win]))
    rows.append([L("Positivité"), L(r"$\min_{n\kv}\Gamma_{n\kv}N_\text{cells}$"),
                 Cell(f"${gmin:.2f}$~eV", f"{rel(fr)} : min de G_T sur |E_out − E_D| ≤ {CFG['e_window_eV']} eV (eV)", gmin),
                 Cell(r"$-10^{-8}$~eV", "ch4/NOTES_TGAMMA.md : l. 122 (C7)", "-1e-8")])
    return Table("tests_T", "tab:tests_T", "§4.2.5 → annexe D", "l l l l", [r"Test & Quantité & Valeur & Seuil \\"],
                 ["test", "quantité", "valeur", "seuil"], rows,
                 ["Lignes 6×6, 12×12 (non rejoués avec M2) et grille d'énergie (v1 seulement) retirées (TODO).",
                  "Ligne « Hermiticité de M_loc » retirée (décision du 2026-10-01) : l'hermiticité de M est déjà dans tab:tests_M "
                  "et aucune valeur de la 9×9 de production n'existe hors des journaux.",
                  "Positivité : minimum réel sur les 41 266 états de la fenêtre (9×9 de production) au lieu de « ≥ 0 »."])


# tab:kaasbjerg 

KAAS_LIT = "lit. : Kaasbjerg 2020 (PRB 101, 045433)"

def t_kaasbjerg():
    def K(name):
        return Path(campaigns_dir(CFG, "kaasbjerg", name))
    fd, fs, f7, fc, ff = (K("r8_dos_results.json"), K("r8_spec_results.json"), K("r8_7a_results.json"),
                          K("r10_c2_results.json"), K("r8_fig_results.json"))
    D, Sp, F = read_json(fd)["metrics"], read_json(fs)["runs"], read_json(ff)["superposition_7b"]
    k13, k14 = read_json(f7)["fig13_metrics"], read_json(f7)["fig14"]
    D1 = read_json(fc)["kaasbjerg"]["D1"]
    grid = 600
    var = (("tel_quel", "tel quel", 0.0), ("aligne", "plateau", alignment_C(CFG, "9x9")))   # (R8, R10 C.2, C_N attendu)
    lit = {"0.001": "0.1", "0.01": "1.0"}                   # c_i -> légende de la Fig. 13 de Kaasbjerg
    for v, _, C in var:                                     # paramètres et concordance entre les json de R8
        for c in ("0.001", "0.01"):
            m, sup = D[f"{v}_{grid}_c{c}"], F[f"{v}_{grid}_c{c}"]
            gate(abs(m["C_N_eV"] - C) < 1e-15 and m["eta_G"] == 0.05 and m["eta_t"] == 0.02 and m["N_k_int"] == 900,
                 f"r8_dos_results.json {v}, c {c} : paramètres inattendus")
            gate(abs(sup["pos_ours"] - m["drho_max_pos_eV"]) < 1e-9, f"r8_fig ≠ r8_dos ({v}, c {c})")
            gate(abs(sup["pos_K"] - k13[lit[c]]["drho_max_pos_eV"]) < 1e-9, f"r8_fig pos_K ≠ r8_7a (c {c})")
        gate(Sp[f"{v}_c0.01"]["eta_G"] == 0.025 and Sp[f"{v}_c0.01"]["N_k_int"] == 900, f"r8_spec_results.json {v} : paramètres")
    sd, ss, s7, sc = rel(fd), rel(fs), rel(f7), rel(fc)

    rows = []
    cells = [L(r"$A_\text{cell}|M_{nn}|$ près de $K$ (eV\,\AA$^2$)"),
             Cell(r"${\sim}70$", f"{KAAS_LIT}, Fig. 3, lu sur la figure (défauts.tex l. 327), aucune donnée numérisée", "~70")]
    for _, w, _ in var:
        a, b = D1[w]["valence | K"]["mean"], D1[w]["conduction | K"]["mean"]
        cells.append(Cell(f"{a:.0f} / {b:.0f}", f"{sc} : kaasbjerg.D1.{w}.{{valence, conduction}} | K.mean", f"{a:.3f} / {b:.3f}"))
    rows.append(cells)
    for c, tex in (("0.001", r"Maximum de $\rho-\rho_0$ (eV), $c = 0.1~\%$"), ("0.01", r"\quad $c = 1~\%$")):
        a = k13[lit[c]]["drho_max_pos_eV"]
        cells = [L(tex), Cell(fixed(a, 3), f"{s7} : fig13_metrics.{lit[c]}.drho_max_pos_eV", a)]
        for v, _, _ in var:
            a = D[f"{v}_{grid}_c{c}"]["drho_max_pos_eV"]
            cells.append(Cell(fixed(a, 4), f"{sd} : metrics.{v}_{grid}_c{c}.drho_max_pos_eV", a))
        rows.append(cells)
    h = k13["1.0"]["drho_max"]
    cells = [L(r"Hauteur, $c = 1~\%$ (eV$^{-1}$)"), Cell(fixed(h, 3), f"{s7} : fig13_metrics.1.0.drho_max", h)]
    for v, _, _ in var:                                     # nos DOS sont par spin : × 2 pour compter le spin comme Kaasbjerg
        x = 2 * D[f"{v}_{grid}_c0.01"]["drho_max"]
        cells.append(Cell(fixed(x, 3), f"{sd} : metrics.{v}_{grid}_c0.01.drho_max × 2 (spin)", x))
    rows.append(cells)
    w0 = k13["1.0"]["drho_fwhm_eV"]
    cells = [L(r"Largeur à mi-hauteur, $c = 1~\%$ (eV)"), Cell(fixed(w0, 2), f"{s7} : fig13_metrics.1.0.drho_fwhm_eV", w0)]
    for v, _, _ in var:
        x = D[f"{v}_{grid}_c0.01"]["drho_fwhm_eV"]
        cells.append(Cell(fixed(x, 2), f"{sd} : metrics.{v}_{grid}_c0.01.drho_fwhm_eV", x))
    rows.append(cells)
    g0 = k14["1.0"]["K_gap_eV"]
    cells = [L(r"Écart des maxima de $A_K$, $c = 1~\%$ (eV)"), Cell(fixed(g0, 3), f"{s7} : fig14.1.0.K_gap_eV", g0)]
    for v, _, _ in var:
        x = Sp[f"{v}_c0.01"]["K_gap_eV"]
        cells.append(Cell(fixed(x, 3), f"{ss} : runs.{v}_c0.01.K_gap_eV", x))
    rows.append(cells)
    head = [r"Grandeur & Kaasbjerg~\cite{kaasbjergAtomisticMatrixTheory2020} & non aligné & Kumagai--Oba \\"]
    return Table("kaasbjerg", "tab:kaasbjerg", "§4.2.5, corps", "l c c c", head,
                 ["grandeur", "Kaasbjerg", "non aligné", "Kumagai–Oba"], rows,
                 ["Colonne Kaasbjerg : Fig. 13 et 14 de l'article numérisées dans `r8_7a_results.json` (Fig. 13 : courbes vectorielles "
                  "du PDF interpolées au meV ; Fig. 14 : points sur des cellules de 10 meV). Seule cellule sans source lisible par "
                  "machine : A_cell|M| ~70 eV Å², lu sur sa Fig. 3.",
                  "Nos colonnes (9×9, R_cut 3, η_t = 20 meV, N_k^int = 900) : ρ − ρ₀ sur la grille 600² avec η_G = 50 meV "
                  "(`r8_dos_results.json`) ; A_K avec η_G = 25 meV (`r8_spec_results.json`) ; A_cell|M_nn| = moyenne sur un disque "
                  "de 0.147 Å⁻¹ autour de K, état initial K + δx̂ (δ = 0.029 Å⁻¹), 512 points (`r10_c2_results.json` : kaasbjerg.meta). "
                  "Nos DOS sont par spin : hauteur × 2 (spin compté, comme Kaasbjerg) ; unité : états/eV/maille. c = défauts par maille "
                  "(convention de Kaasbjerg). A_cell|M_nn| : π / π* (valence / conduction), à dire dans la légende.",
                  "Nos positions tombent sur la grille d'énergie de pas 2.5 meV : quatre décimales (−0.1625 arrondi à trois "
                  "décimales est ambigu). Kaasbjerg : trois décimales (lecture au meV).",
                  "Contrôles : positions de `r8_fig_results.json` (superposition_7b) = `r8_dos_results.json` ; pos_K = `r8_7a_results.json` ; "
                  "C_N, η_t, η_G et N_k^int attendus."])


# tab:grille_interne 

def t_grille_interne():
    f, fl = RES / "nkint_check_9x9.csv", RES / "level1_summary.csv"
    prod = float(csv_row(fl, size="9x9", R_cut="3", grid="240", eta_eV="0.02")["median_Gamma_Ncells_meV"])
    rows = []
    for n in ("150", "300", "450", "600"):
        r = csv_row(f, nk_int=n)
        gate(int(r["nk_tot"]) == int(n) ** 2 and r["n_states"] == "41266" and r["n_ED"] == "4", f"{rel(f)} : nk_int {n}")
        gate(r["E_res"] == r["z_E_res"], f"{rel(f)} : E_res ≠ z_E_res à nk_int {n}")
        if n == "300":
            gate(abs(float(r["medG"]) - prod) < 1e-3, "nkint_check_9x9.csv nk 300 ≠ production (level1_summary.csv)")
        cells = [L(f"${n}^2$")]
        for col in ("medG", "z_medG", "G_ED"):
            x = float(r[col])
            cells.append(Cell(f"{x:.0f}", f"{rel(f)} : {col} [nk_int = {n}]", x))
        x = float(r["E_res"])
        cells.append(Cell(fixed(x, 3), f"{rel(f)} : E_res [nk_int = {n}]", x))
        rows.append(cells)
    head = [r"& \multicolumn{2}{c}{Médiane de $\Gamma N_\text{cells}$ (meV)} & $\Gamma N_\text{cells}(E_D)$ & $E_\text{res}-E_D$ \\",
            r"\cline{2-3}",
            r"$N_{\tilde\kv}$ & $\pm3$~eV & $\pm0.3$~eV & (meV) & (eV) \\"]
    return Table("grille_interne", "tab:grille_interne", "§4.2.5 → annexe D (chaîne T)", "c c c c c", head,
                 ["N_k^int", "médiane ±3 eV (meV)", "médiane ±0.3 eV (meV)", "Γ N_cells(E_D) (meV)", "E_res − E_D (eV)"], rows,
                 ["9×9 de production (Kumagai–Oba), R_cut 3, grille de sortie 240², η = 20 meV. Fenêtre ±3 eV : 41 266 états ; "
                  "zone |ε − E_D| ≤ 0.3 eV : 280 états (`z_n`) ; Γ(E_D) : les 4 états au point de Dirac (`n_ED`). "
                  "Contrôle : 300² = production (`level1_summary.csv`).",
                  "E_res = argmax de Γ sur les états à ±1.5 eV : grandeur **retirée du ch. 4 par la décision R10 B.1** (argmax discret "
                  "sur les états de la grille de sortie), remise ici à la demande de G (2026-10-01) ; à confirmer à la rédaction "
                  "de l'annexe D. E_res = z_E_res dans le csv."])


TABLES = {f.__name__[2:]: f for f in (t_echantillonnage, t_L_NL, t_rcut_M, t_alignement, t_tests_M, t_convergence_gamma, t_tests_T,
                                            t_kaasbjerg, t_grille_interne)}


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
