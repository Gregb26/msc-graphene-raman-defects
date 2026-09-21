# CLAUDE.md

Mémoire de maîtrise (DMS, Université de Montréal). Rédaction en français.

## Compilation

```bash
make clean all     # LuaLaTeX + biber + LuaLaTeX x2
make check         # erreurs et Overfull > 10 pt du dernier log
```

**Toujours passer par le `Makefile`**, jamais `lualatex` nu. Le `Makefile`
positionne `TEXINPUTS="cls_local:"`, ce qui fait charger la copie corrigée
de la classe (`cls_local/dms.cls`) au lieu de l'originale.

`./dms.cls` (gabarit du département, v2.2 de 2019) **ne compile pas sous
LuaLaTeX** : son `\edef` sur des noms de rubriques accentués casse sous
l'encodage Unicode TU et laisse `\francais` indéfini, ce qui fait échouer
`master_thesis.tex` dès sa ligne 13 sans produire de PDF. `cls_local/dms.cls`
en est une copie portant l'unique correction `\edef` → `\protected@edef` ;
l'en-tête du fichier détaille le diagnostic. L'original reste intact et le
bogue a été signalé au département : quand une version corrigée sera
distribuée, supprimer `cls_local/` et le `TEXINPUTS` du `Makefile`.

Renommer une étiquette invalide les `.aux`/`.out` et fait échouer la passe
suivante sur `Undefined control sequence` (`r@chap:...`). Faire `make clean all`
après toute modification d'étiquette.

Les références non résolues sont normales : les `\include` correspondants
sont commentés dans `master_thesis.tex`. Sur le build courant — chapitre 4
plus annexe C, les deux `\maketitle` commentés — la liste complète est, aux
11 étiquettes près : `chap:Raman`, `chap:eph`, `sec:wannier`, `sec:PP`,
`sec:PW`, `sec:hamiltonien`, `sec:symétries`, `sec:electron_results`,
`fig:règles_Raman`, `eqn:V_NL_k` et `eqn:betar` (ces deux dernières
renommées avec le préfixe `eqn:` à la passe P20). Toute étiquette hors de cette liste
signale un vrai renvoi cassé.

`annexes/défauts` étant désormais inclus, `annexe:défauts` et `eqn_G_tau`
résolvent et ne figurent plus dans la liste ; en contrepartie
`sec:hamiltonien`, auquel l'annexe renvoie, y est apparu.

## Conventions de rédaction

- **Décimales au point** (`$2.3$`), en mode mathématique comme en mode texte,
  par cohérence avec la littérature du domaine. La virgule reste le séparateur
  de liste et prend alors une espace (`$N=5, 7, 8, 9$`, `$1, 5, 13, 29, 49$`) :
  c'est l'ambiguïté des suites d'entiers qui a motivé le changement. Ne pas
  toucher aux espaces fines de milliers (`41\,266`), aux dimensions de grilles
  (`27\times 27`), aux longueurs LaTeX (`\vspace{0.5\baselineskip}`), aux clés
  bib, aux étiquettes ni aux numéros de sections.
- Pourcentages : `X~\%`.
- Grilles : trois noms seulement — **grossière** (`N x N`), **élargie**
  (`pN x pN`), **fine** (`k_f`). « dense » est réservé à la grille de sortie
  de l'interpolation de Wannier. « matrice dense » / « inversion dense »
  (sens algébrique) sont un autre mot, à conserver.
- Étiquettes d'équations préfixées `eqn:`.
- `\braket{a}{b}` et `\matrixel{a}{V}{b}` (paquet `physics`).
- `pseudo-potentiel` (avec trait d'union), `cellule unitaire`, `c.-à-d.`,
  `N_\text{cells}`.
- `BZ` se conserve : le sigle est déclaré dans
  `pages_liminaires/sigles_abbréviations.tex` et domine dans les autres
  chapitres.

Ne jamais modifier `figures/`, `tikz/` ni les `.bib` dans le cadre d'une
passe de relecture. Une figure ne se corrige qu'en modifiant le script qui
la produit (dépôt `~/Projects/electron_defect_interaction`) puis en la
régénérant — jamais en éditant le PDF.

## Provenance des données du chapitre 4

`tab:convergence_gamma` est alimenté par **deux** sources distinctes, ce qui
n'est pas apparent à la lecture du tableau :

- colonnes `R_cut = 0` à `3`, les six tailles : `results/M/level1_summary.csv`
  (carte de niveau 1, balayage grille × eta × R_cut) ;
- colonne `R_cut = 4`, ligne `9x9` seulement (2468) : `m_rcut_resigma.csv`,
  produit par `rcut_resigma.py` (balayage R_cut 0–4, 9×9 uniquement), et non
  par `level1_summary.csv`, qui ne contient aucune ligne `R_cut = 4`.

Les deux sources concordent : sur `R_cut = 0`–`3` à `9x9`/240/0,02 eV, elles
donnent des valeurs identiques aux quatre décimales de `level1_summary.csv`
(2596,9154 / 2488,8991 / 2466,8378 / 2473,5466). `m_rcut_resigma.csv` confirme
aussi la suite des `nL` (1, 5, 13, 29, 49) et `dim = 145` à `R_cut = 3`.

Note : cette provenance appartient à `NOTES_TGAMMA.md` §6, absent de ce poste
de travail — à y reporter.

## À faire

### Chapitre 5 et calculs sur rorqual

- **Définir UNE médiane commune ch. 4 / ch. 5** (sur les états, bandes
  `pi`/`pi*`, fenêtre `±3 eV`) avant de rédiger la comparaison
  `Gamma^ed`/`Gamma^ep`. Le ch. 4 part avec `~25 meV`, cohérent avec
  `tab:convergence_gamma` (2474 meV à `N=9`, `R_cut=3`, soit 24,7 meV à
  `c=1 %`). Le « 23 meV » n'existe dans aucun texte pour l'instant.
- **Recalculer depuis les npz Γ (C.4)** : médiane sur les états, et le
  contrôle à `±1,2 eV`. Impossible localement — ni implémentation de la
  matrice T, ni fichiers Wannier dans le dépôt de calcul.
- **Recalculer la dispersion « convention intensive » (C.3)** sur les
  grilles élargies, 20 bandes. Les `.npy` locaux sont grossiers et à
  16 bandes : ils donnent 10,6 % sur les six tailles, ce qui ne reproduit
  ni le « 2 % » du texte ni le `1,1e-2` de `tab:tests_M`.
- **Produire la bande ombrée `R_cut` [6,52 ; 8,54] Å sur `fig_Ved`** (C.6),
  en remplacement de la ligne verticale unique. Aucun script générateur de
  cette figure n'existe actuellement dans le dépôt de calcul.

### Restes de la passe P20 (chap. 2 et 3)

- **Régénérer `figures/fig_phonons.pdf`** avec la chaîne `24k-24q_mv0.02`
  (mêmes IFC que `fig_epw_*`), chemin `Gamma-K-M-Gamma`, DOS de `matdyn.x`
  en états/cm^-1. Le générateur est `~/Projects/qe_pp/notebooks/phonons.ipynb`,
  mais ses données locales (`data/phonons/`) sont celles d'anciennes chaînes
  (`E_2g` à 1586 et 1566 cm^-1, pas 1550.5) : les sorties de la bonne chaîne
  sont sur rorqual. Puis remplacer, dans `chapitres/théorie.tex`, le
  `% TODO P20-C2`, la fin de la légende (b) et la phrase « grille `96 x 96`,
  `sigma = 0.01 Ry` » par la grille dense et le `DeltaE` réels de matdyn, et
  revoir la liste des pics de van Hove.
- **IBZ = 1/12** : établi par comptage de symétrie (75 points irréductibles
  pour `27 x 27`, 19 pour `12 x 12`), pas lu dans une sortie QE — aucune
  sortie SCF `27 x 27` sur ce poste. À confirmer par
  `grep 'number of k points'` sur rorqual.
- **Fiches Zotero à refaire (C19)** : le `.bib` est un export BBT, ne pas
  l'éditer à la main. Voir le rapport P20 pour la liste.

### Après le dépôt

- Renommer `eqn_G_tau` → `eqn:G_tau` (déclarée dans `annexes/défauts.tex`,
  3 renvois : annexe ×2 + `chapitres/défauts.tex`). Seule étiquette
  d'équation du mémoire qui n'a pas le préfixe `eqn:`. Impose un
  `make clean all`. Reporté après le dépôt : le renvoi actuel résout
  correctement, ce n'est qu'une dette de convention.

### Balayage transverse

- Remplacer les 3 « i.e. » résiduels des autres chapitres par « c.-à-d. »
  (le ch. 4 est déjà converti).
- Virgule manquante après `\ref{sec:M_local}` dans
  `chapitres/défauts.tex` (« Tel que mentionné à la section~\ref{sec:M_local}
  ce remplissage est *exact* »).
- Deux « plus bas » subsistent hors du paragraphe traité
  (`sec:mbt_sigma` et `sec:T_results`) : à remplacer par des renvois
  explicites.
- `fig:G_Dyson` est la seule légende de diagramme sans forme courte `[...]`
  pour la liste des figures.
