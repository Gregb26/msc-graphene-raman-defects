# Mémoire de maîtrise sur la spectroscopie Raman résonante du graphène avec défauts à partir des premiers principes

Grégoire Barrette, Université de Montréal, 2026. Directeur de recherche : Michel Côté.

Ce dépôt contient le texte du mémoire et tout ce qui a servi à produire ses figures et ses résultats numériques.

## Structure

| Dossier            | Contenu                                                        |
|--------------------|----------------------------------------------------------------|
| `memoire/`         | Source LaTeX du mémoire                                        |
| `calculs/`         | Inputs QE, Wannier90, EPW et scripts SLURM, un dossier par calcul |
| `analyse/`         | Post-traitement (copie figée du repo de recherche)             |
| `donnees/`         | Données finales derrière les figures                           |
| `scripts_figures/` | Scripts de génération des figures                              |

`master_thesis.pdf` à la racine est la dernière version compilée.

## Compiler le mémoire

Requiert TeX Live (LuaLaTeX, biber).

```bash
cd memoire
latexmk
```

Le PDF est écrit à la racine du dépôt et les fichiers auxiliaires vont dans `memoire/build/`.

## Reproduire les figures

**Pour installer l'environnement :**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Scripts :**  *à venir*

## Données lourdes

*À venir* 

Les données intermédiaires volumineuses seront archivées séparément.
