"""Appariement des chiffres du chapitre 5 (memoire/chapitres/eph.tex) aux données de donnees/epw/.

Pool des valeurs (chaque entrée porte sa source « fichier : clé ») :
  - scalaires de tous les npz de donnees/epw/ (unités natives ; eV aussi offerts en meV, meV en cm⁻¹ et inversement) ;
  - tables internes : phself key_values (mode, T, ω, γ), d2_table, validation bands_err / ph_err, g_* statistiques ;
  - dérivés : médianes de Γ^ep des selfen_* en meV et écarts (%) à la ligne de production 240² / σ 0.02 / 300 K,
    écart 300 K → 10 K, positions des maxima de Γ^ep(ε) (van Hove), bosse à E_D (hauteur, largeur), Γ^ed/Γ^ep
    (ed_vs_ep_24k24q_mv0.02.npz), fréquences cm⁻¹ des modes E2g(Γ) et A1'(K) de dfpt_path_freq_* et phself_* ;

Sortie : donnees/epw/eph_nombres.md. Usage : python scripts/chiffres_ch5.py
"""

import json
import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
EPW = ROOT / "donnees" / "epw"
TEX = ROOT / "memoire" / "chapitres" / "eph.tex"
OUT = EPW / "eph_nombres.md"
MEV_CM = 8.065544                      # 1 meV = 8.0655 cm⁻¹
RY_EV = 13.605693                     # 1 Ry en eV
PROD = "selfen_240_dg0.02_mv0.02_T300.npz"

pool = []                              # (valeur, source, étiquette de conversion)


def add(v, src, conv=""):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return
    if not np.isfinite(v):
        return
    pool.append((v, src, conv))


def add_units(v, src, unit):
    """Ajoute v et ses conversions usuelles selon l'unité native."""
    add(v, src)
    if unit == "eV":
        add(v * 1e3, src, "×10³ (eV→meV)"); add(v * 1e3 * MEV_CM, src, "eV→cm⁻¹")
    elif unit == "meV":
        add(v / 1e3, src, "÷10³ (meV→eV)"); add(v * MEV_CM, src, "meV→cm⁻¹")
    elif unit == "cm":
        add(v / MEV_CM, src, "cm⁻¹→meV")
    elif unit == "frac":
        add(v * 100, src, "×100 (fraction→%)")


# ---------------- 1. scalaires de tous les npz
for f in sorted(EPW.glob("*.npz")):
    D = np.load(f, allow_pickle=True)
    units = str(D["units"]) if "units" in D else ""
    for k in D.keys():
        v = D[k]
        if v.dtype.kind in "OUS":
            continue
        if v.ndim == 0 or v.size <= 6:
            for i, x in enumerate(np.atleast_1d(v).ravel()):
                src = f"{f.name} : {k}" + (f"[{i}]" if np.atleast_1d(v).size > 1 else "")
                unit = "eV" if ("eV" in units and "meV" not in units.split(";")[0]) else ("meV" if units.startswith("meV") else "")
                if k.startswith("gamma") and "HWHM" in units:
                    unit = "eV"
                add_units(x, src, unit)
                if "ratio" in k or k.startswith("Sg_") or "err" in k:
                    add(x * 100, src, "×100 (fraction→%)")

# ---------------- 2. tables internes
for f in sorted(EPW.glob("phself_path_*.npz")):
    D = np.load(f, allow_pickle=True)
    for row in D["key_values"]:
        mode, _, T, om, ga = row[0], row[1], float(row[2]), float(row[3]), float(row[4])
        src = f"{f.name} : key_values {mode} T={T:g}"
        add_units(om, src + " ω (meV)", "meV"); add_units(ga, src + " γ_epw (meV)", "meV")
        add(ga / 2, src + " γ/2 (HWHM, meV)"); add(ga / 2 / 1e3, src + " γ/2 (HWHM, eV)")
    # 300 K → 10 K sur les modes clés (fraction)
    kv = {(r[0], float(r[2])): float(r[4]) for r in D["key_values"]}
    for (m, T), g in kv.items():
        if T == 10.0 and (m, 300.0) in kv:
            add((1 - kv[(m, 300.0)] / g) * 100, f"{f.name} : key_values {m} : 1 − γ(300 K)/γ(10 K) (%)")
for f in sorted(EPW.glob("d2_extract_*.npz")):
    D = np.load(f, allow_pickle=True)
    for row in D["d2_table"]:
        for j, x in enumerate(row[1:]):
            add(float(x), f"{f.name} : d2_table « {row[0]} » col. {j + 1}")
    # D²/g² : S_D / S_g (eV/Å²) et rapport inverse
    for pt in ("G", "K"):
        for ch in ("epw", "dfpt"):
            add(float(D[f"SD_{pt}_{ch}"]) / float(D[f"Sg_{pt}_{ch}"]), f"{f.name} : SD_{pt}_{ch}/Sg_{pt}_{ch}")
for f in sorted(EPW.glob("validation_*.npz")):
    D = np.load(f, allow_pickle=True)
    for name in ("bands_err", "ph_err"):
        A = D[name]
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                add_units(A[i, j], f"{f.name} : {name}[{i},{j}]", "eV" if name == "bands_err" else "cm")
    for name in ("g_G", "g_K"):
        A = D[name]; m = np.isfinite(A)
        add_units(np.nanmedian(A), f"{f.name} : médiane {name}", "meV"); add_units(np.nanmax(A), f"{f.name} : max {name}", "meV")
    for name in ("decay_H", "decay_dynmat", "decay_epmate", "decay_epmatp"):      # tables de décroissance en Ry
        r, v = D[name + "_r"], D[name + "_v"]; m = np.isfinite(v) & (v > 0)
        tail = v[m][r[m] >= 0.9 * r[m].max()]                                       # plancher = médiane de la queue (r ≥ 0.9 r_max)
        for lab, x in (("max", v[m].max()), ("plancher (médiane r ≥ 0.9 r_max)", np.median(tail)), ("min", v[m].min())):
            add(x, f"{f.name} : {name} {lab} (Ry)"); add(x * RY_EV, f"{f.name} : {name} {lab}", "Ry→eV")
        add(np.nanmax(r), f"{f.name} : portée max {name}_r (Å)")
for f in sorted(EPW.glob("ring_check_*.npz")):
    D = np.load(f, allow_pickle=True)
    for k in ("E2g_qGamma", "A1p_qK"):
        for i, x in enumerate(D[k]):
            add_units(x, f"{f.name} : {k}[{i}]", ["eV", "", "", "eV", "meV"][i])
        add(float(D[k][4]) / (2 * float(D[k][3]) * 1e3), f"{f.name} : {k} : γ_epw / (2 Im Π)")

# ---------------- 3. dérivés des selfen_*
P = np.load(EPW / PROD, allow_pickle=True)
for f in sorted(EPW.glob("selfen_*.npz")):
    D = np.load(f, allow_pickle=True)
    for w in ("3eV", "1p2eV"):
        m = float(D[f"median_{w}"]); add_units(m, f"{f.name} : median_{w}", "eV")
        add((m / float(P[f"median_{w}"]) - 1) * 100, f"{f.name} : (median_{w} / production − 1) (%)")
    eg, Ge = D["eg"] - float(D["E_D"]), D["Gamma_e"]
    for lo, hi, nm in ((-3, -1), ("vH π"), ) if False else ((-3.0, -1.0, "max Γ^ep(ε) sur [−3, −1] eV (van Hove π)"), (1.0, 3.0, "max Γ^ep(ε) sur [1, 3] eV (van Hove π*)")):
        sel = (eg >= lo) & (eg <= hi)
        i = np.argmax(Ge[sel]); add(eg[sel][i], f"{f.name} : position du {nm}"); add_units(Ge[sel][i], f"{f.name} : valeur du {nm}", "eV")
    # bosse à E_D : hauteur au-dessus du min voisin et largeur à mi-hauteur
    sel = np.abs(eg) <= 0.6
    i0 = np.argmin(np.abs(eg)); top = Ge[i0]
    left = Ge[(eg < 0) & sel].min(); right = Ge[(eg > 0) & sel].min(); base = max(left, right)
    add_units(top - base, f"{f.name} : bosse à E_D, hauteur au-dessus des minima voisins", "eV")
    add_units(top, f"{f.name} : Γ^ep(E_D) de la courbe moyennée", "eV")
    half = base + (top - base) / 2; inside = sel & (Ge >= half)
    if inside.any():
        add(eg[inside].max() - eg[inside].min(), f"{f.name} : bosse à E_D, largeur à mi-hauteur (eV)")
    # états individuels près de E_D
    E = D["E"] - float(D["E_D"]); G = D["Gamma"]
    for d in (0.0, 0.067, 0.114):
        sel = np.abs(np.abs(E) - d) < 0.01
        if sel.any():
            add_units(np.median(G[sel]), f"{f.name} : Γ^ep des états à |ε−E_D| ≈ {d} eV", "eV")
    add(int(D["n_states_3eV"]), f"{f.name} : n_states_3eV"); add(int(D["n_states_1p2eV"]), f"{f.name} : n_states_1p2eV")
    add(len(D["k"]), f"{f.name} : nombre de k listés"); add(len(np.unique(D["ik"])), f"{f.name} : nombre de k dans la fenêtre")
# ---------------- 4. Γ^ed / Γ^ep
f = ROOT / "donnees" / "M2_plateau" / "ed_vs_ep_24k24q_mv0.02.npz"
if f.exists():
    D = np.load(f, allow_pickle=True)
    for k in ("median", "min", "x_min", "max", "x_max", "median_ed", "median_ep", "c", "T"):
        add_units(float(D[k]), f"{f.name} : {k}", "eV" if k.startswith("median_") else "")
    for i, x in enumerate(D["crossings"]):
        add(x, f"{f.name} : crossings[{i}]")
    x, r = D["x"], D["ratio"]; m = np.isfinite(r)
    add(r[np.argmin(np.abs(x))], f"{f.name} : ratio à E_D")
    add(np.median(r[m]) / 10, f"{f.name} : médiane du rapport à c = 0.1 %"); add(float(D["max"]) / 10, f"{f.name} : max du rapport à c = 0.1 %")
    add(1 / (np.median(r[m]) / 10), f"{f.name} : 1 / médiane à c = 0.1 %")
    rr = r / 10; sel = m & (rr > 1)
    if sel.any():
        add(x[sel].min(), f"{f.name} : c = 0.1 % : ratio > 1 depuis (eV)"); add(x[sel].max(), f"{f.name} : c = 0.1 % : ratio > 1 jusqu'à (eV)")
# ---------------- 5. fréquences des modes sur le chemin DFPT (cm⁻¹) : Γ (s = 0) et K
for f in sorted(EPW.glob("dfpt_path_freq_*.npz")):
    D = np.load(f, allow_pickle=True); s, F = D["s"], D["freq"]
    iG, iK = int(np.argmin(s)), int(np.argmin(np.abs(s - s[np.argmin(np.linalg.norm(D["q_cart"] - D["q_cart"][np.argmax(np.linalg.norm(D['q_cart'], axis=1))], axis=1))])))
    for j in range(F.shape[1]):
        add_units(F[iG, j], f"{f.name} : freq[Γ, branche {j}]", "cm")
    # K : point du chemin dont |q| est maximal n'est pas sûr ; on offre toutes les fréquences du chemin aux points de symétrie
    for idx in np.where(np.isin(np.round(s, 3), np.round([s[0], s[len(s)//3], s[2*len(s)//3], s[-1]], 3)))[0]:
        for j in range(F.shape[1]):
            add_units(F[idx, j], f"{f.name} : freq[s={s[idx]:.3f}, branche {j}]", "cm")
    for j in range(F.shape[1]):
        add_units(F[:, j].max(), f"{f.name} : max freq branche {j} sur le chemin", "cm")
# ---------------- 6. nombres des notes et de la config
for name in ("NOTES_EPW.md", "NOTES_EPW_REPERES.md"):
    for i, l in enumerate((EPW / name).read_text(encoding="utf-8").split("\n"), 1):
        for mm in re.finditer(r"(?<![\w.])[+-]?\d+(?:[.,]\d+)?(?:\s*[×x]\s*10[\^⁻−-]*\{?-?\d+\}?|e-?\d+)?", l):
            tok = mm.group(0).replace(",", ".")
            try:
                v = float(re.sub(r"\s*[×x]\s*10[\^⁻−-]*\{?(-?\d+)\}?", r"e\1", tok).replace("⁻", "-").replace("−", "-"))
            except ValueError:
                continue
            if abs(v) >= 100 and float(v).is_integer() and 1900 <= v <= 2100:
                continue
            add(v, f"{name} l.{i}")
cfg = json.loads((ROOT / "config" / "production.json").read_text())
def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, path + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, path + f"[{i}]")
    elif isinstance(o, (int, float)) and not isinstance(o, bool):
        add(o, "config/production.json : " + path.lstrip("."))
walk(cfg, "")

# ---------------- 7. nombres du texte
text = TEX.read_text(encoding="utf-8").split("\n")
pat = re.compile(r"(?<![\w\\^_{])[+-]?\d+(?:[.,]\d+)?(?:\s*\\times\s*10\^\{?-?\d+\}?)?")
items = []
for i, l in enumerate(text, 1):
    s = l.split("%")[0]
    s = re.sub(r"\\(?:label|ref|eqref|cite|includegraphics)\{[^}]*\}", "", s).replace("\\pm", " ± ")
    in_tab = "&" in s or "\\\\" in s
    for mm in pat.finditer(s):
        tok = mm.group(0).strip()
        if re.search(r"(19|20)\d\d", tok) and len(tok) == 4:
            continue
        sci = "\\times" in tok
        v = float(re.sub(r"\s*\\times\s*10\^\{?(-?\d+)\}?", r"e\1", tok).replace(",", "."))
        if not sci and float(v).is_integer() and abs(v) < 100 and not in_tab:
            continue
        mant = tok.split("\\times")[0].strip().replace(",", ".")
        dec = len(mant.split(".")[1]) if "." in mant else 0
        expo = int(re.search(r"10\^\{?(-?\d+)\}?", tok).group(1)) if sci else 0
        tol = 0.5 * 10 ** (expo - dec)                     # ½ unité de la dernière décimale de la mantisse
        ctx = s[max(0, mm.start() - 45):mm.end() + 25].strip()
        items.append((i, tok, v, tol, ctx))

# ---------------- 8. appariement
def fmt(v):
    return f"{v:.6g}"
lines = ["# Chiffres du chapitre 5 — appariement à `donnees/epw/`", "",
         f"Généré par `scripts/chiffres_ch5.py` (ne pas éditer). Texte : `memoire/chapitres/eph.tex`, {len(items)} nombres comparés "
         f"(entiers < 100 hors tabular exclus) ; pool : {len(pool)} valeurs. Tolérance : ½ unité de la dernière décimale du texte "
         "(mantisse comprise en notation scientifique). Un appariement est mécanique, pas une identification ; « non apparié » = à vérifier à la main "
         "ou valeur de la littérature / d'un paramètre d'entrée.", "",
         "| ligne | nombre | contexte | appariements (valeur : source) |", "|---|---|---|---|"]
n_ok = 0; unmatched = []
for (i, tok, v, tol, ctx) in items:
    hits = [(pv, src, conv) for (pv, src, conv) in pool if abs(pv - v) <= tol]
    # dédoublonner par source
    seen = set(); hh = []
    for pv, src, conv in hits:
        key = (src, conv)
        if key in seen: continue
        seen.add(key); hh.append(f"{fmt(pv)} : {src}" + (f" ({conv})" if conv else ""))
    if hh:
        n_ok += 1
    else:
        unmatched.append((i, tok, ctx))
    cell = " ; ".join(hh[:6]) + (f" … (+{len(hh) - 6})" if len(hh) > 6 else "") if hh else "**non apparié**"
    lines.append(f"| {i} | {tok} | {ctx.replace('|', '¦')} | {cell} |")
lines += ["", f"Comptes : {n_ok} appariés, {len(unmatched)} non appariés.", "", "## Non appariés", ""]
lines += [f"- l.{i} `{tok}` — {ctx.replace('|', '¦')}" for i, tok, ctx in unmatched]
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"[chiffres_ch5] {OUT.relative_to(ROOT)} : {len(items)} nombres, {n_ok} appariés, {len(unmatched)} non appariés")
