# Mémoire de maîtrise sur la spectroscopie Raman résonante du graphène avec défauts à partir des premiers principes

Grégoire Barrette, Université de Montréal, 2026. Directeur de recherche : Michel Côté.

Ce repo contient les fichiers sources du mémoire ainsi que les données ayant servies à la génération des tableaux et des figures. 

## Structure

| Dossier            | Contenu                                                        |
|--------------------|----------------------------------------------------------------|
| `calculs/`         | Inputs QE, Wannier90, EPW et scripts bash pour le lancement des calculs|
| `config/`          | Paramètres de production                                       |
| `donnees/`         | Données des figures et tableaux                      |
| `memoire/`         | Source LaTeX du mémoire                                        |
| `scripts/`         | Scripts de génération des figures et des tableaux à partir des données|
| `src/`             | Partie du code source requise pour rouler les scripts. Le reste du code source est dans un repo privé |

## Compiler le mémoire

Requiert TeX Live (LuaLaTeX, biber).

```bash
cd memoire
latexmk -g
```

Le PDF est écrit à la racine du dépôt et les fichiers auxiliaires vont dans `memoire/build/`.

## Reproduire les figures

**Pour installer l'environnement :**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install -e . --no-deps
```

**Script pour générer les figures :**

```bash
python scripts/make_all_figures.py
```


