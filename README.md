# Mémoire de maîtrise sur la spectroscopie Raman résonante du graphène avec défauts à partir des premiers principes

Grégoire Barrette, Université de Montréal, 2026. Directeur de recherche : Michel Côté.

Ce dépôt contient le texte du mémoire et tout ce qui a servi à produire ses figures et ses résultats numériques.

## Structure

| Dossier            | Contenu                                                        |
|--------------------|----------------------------------------------------------------|
| `calculs/`         | Inputs QE, Wannier90, EPW et scripts bash pour le lancement des calculs|
| `config/`          | Paramètres de production                                       |
| `donnees/`         | Données finales derrière les figures                           |
| `memoire/`         | Source LaTeX du mémoire                                        |
| `scripts/`         | Scripts de génération des figures et des tableaux à partir des données|
| `src/`             | Partie du code source requise pour rouler les scripts. Le reste du code source est dans le repo `graphene-raman`|

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
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install -e . --no-deps
```

**Scripts :**  *à venir*

## Données lourdes

*À venir* 

Les données intermédiaires volumineuses seront archivées séparément.
