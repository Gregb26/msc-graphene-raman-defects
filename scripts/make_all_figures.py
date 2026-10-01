"""Génère toutes les figures du mémoire en lançant, l'un après l'autre, les sept scripts make_figures_*.py de ce dossier.

Usage (depuis n'importe où, avec le Python de l'environnement du dépôt) :

    python scripts/make_all_figures.py                    # toutes les figures
    python scripts/make_all_figures.py --only epw,em      # seulement certains scripts
    python scripts/make_all_figures.py --list             # liste des scripts, sans rien lancer

Les figures sont écrites en PDF et en PNG dans figures/<chapitre>/ (dossier par défaut de chaque script).
`make_figures_epw.py` est lancé avec les options de la chaîne de production (élargissement de 0,02 Ry) ;
sans elles, il tracerait l'ancienne chaîne à 0,002 Ry.
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

# nom : (script, options). L'ordre suit celui des chapitres.
SCRIPTS = {
    "electron": ("make_figures_electron.py", []),
    "phonons": ("make_figures_phonons.py", []),
    "em": ("make_figures_em.py", []),
    "defauts": ("make_figures_defauts.py", []),
    "controles": ("make_figures_controles.py", []),
    "kaasbjerg": ("make_figures_kaasbjerg.py", []),
    "epw": ("make_figures_epw.py", ["--prod-tag", "240_dg0.02_mv0.02", "--phself-tag", "path_1200_dg0.02_mv0.02",
                                    "--val-tag", "24k24q_mv0.02", "--sel-suffix", "_mv0.02", "--control",
                                    "--kohn-val-tags", "24k24q,24k24q_mv0.02", "--dfpt-tag", "24k24q"]),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", default=None, help="noms séparés par des virgules : " + ", ".join(SCRIPTS))
    ap.add_argument("--list", action="store_true", help="affiche les scripts et leurs options, sans rien lancer")
    a = ap.parse_args()

    names = a.only.split(",") if a.only else list(SCRIPTS)
    inconnus = [n for n in names if n not in SCRIPTS]
    if inconnus:
        ap.error(f"nom inconnu : {', '.join(inconnus)} (choix : {', '.join(SCRIPTS)})")

    if a.list:
        for n in names:
            script, options = SCRIPTS[n]
            print(f"{n:10s} {script} {' '.join(options)}")
        return 0

    echecs = []
    for n in names:
        script, options = SCRIPTS[n]
        t0 = time.time()
        # cwd = racine du dépôt : deux scripts ont un dossier de sortie par défaut relatif (figures/...)
        r = subprocess.run([sys.executable, str(HERE / script), *options], cwd=ROOT, capture_output=True, text=True)
        etat = "ok" if r.returncode == 0 else f"ÉCHEC (code {r.returncode})"
        print(f"{n:10s} {script:28s} {etat}  {time.time() - t0:5.1f} s", flush=True)
        if r.returncode != 0:
            echecs.append(n)
            print(r.stdout[-2000:], r.stderr[-2000:], sep="\n")

    pdf = sorted((ROOT / "figures").rglob("*.pdf"))
    print(f"\n{len(pdf)} figures (PDF) dans {ROOT / 'figures'}")
    if echecs:
        print(f"scripts en échec : {', '.join(echecs)}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
