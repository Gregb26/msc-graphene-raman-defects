# PROVENANCE — d'où vient chaque figure, table et chiffre du mémoire

Registre de provenance du mémoire : une ligne par figure, table ou groupe de chiffres cités dans `memoire/`.

État au 2026-10-01 : ce dépôt contient le texte du mémoire, ce qui trace ses figures (`scripts/`, `donnees/`), et les fichiers
d'entrée des calculs (`calculs/`). Le code qui a **produit** les données (chaînes des matrices *M* et *T*, post-traitement d'EPW,
tests) n'est pas ici : il est dans le dépôt `graphene-raman`, étiquette `memoire-apres-menage` (commit `14e8c2a`).
Tous les chemins sont relatifs à la racine de ce dépôt, sauf `GR:` = `graphene-raman` à cette étiquette.
`lit.` = valeur de la littérature citée dans le texte.

---

## 0. Structure, installation et recette

```
msc-graphene-raman-defects/
├── memoire/                   LaTeX ; memoire/tables/ : tableaux générés (un tabular par fichier) et leur index SOURCES.md
├── scripts/                   make_all_figures.py (lanceur) + les sept make_figures_*.py ; chiffres_ch4.py (chiffres complémentaires du ch. 4) ;
│                              make_tables.py (les huit tableaux du ch. 4 → memoire/tables/)
├── src/graphene_raman/        sous-ensemble du paquet de GR, réduit à ce que les scripts importent :
│                              config.py, plotting/ (style, palette, sauvegarde), io/pseudo_io.py, electron_phonon/phself.py
├── config/production.json     paramètres de production et emplacement des données (identique à GR, sauf results/… → donnees/…)
├── donnees/                   données derrière les figures, les tables et les chiffres (121 fichiers + MD5SUMS_2026-10-01.txt) ;
│                              un dossier plat par sujet, voir « Dossiers de donnees/ » ci-dessous
├── calculs/                   fichiers d'entrée QE / Wannier90 / EPW (289 fichiers), rangés par chapitre
├── figures/<chapitre>/        sortie des scripts (PDF + PNG), 32 figures (47 avant le tri du 2026-10-01, `fig_M_map_final` retirée le 2026-10-05)
├── requirements.txt           versions exactes de l'environnement (matplotlib 3.10.5, numpy 2.3.5, scipy 1.16.1, pillow 11.3.0)
└── pyproject.toml             paquet graphene_raman (numpy, scipy, matplotlib)
```

### Dossiers de `donnees/`

| Dossier | Contenu | Clé de `production.json` |
|---|---|---|
| `M2_plateau/` | produits finaux de la chaîne M → T → Γ (R10, alignement de Kumagai–Oba) : npz et csv | `results_dir` |
| `M2/` | sommes md5 des matrices M brutes (les `.npy` restent sur Rorqual) | `matrices_dir` |
| `electron/`, `phonon/`, `epw/` | ch. 2 (convergence, bandes, DOS, phonons) et ch. 5 (EPW) ; `epw/NOTES_EPW*.md` | `electron_results_dir`, `phonon_results_dir`, `epw_results_dir` |
| `wannier/27x27/` | `wannier.wout` seulement (étalements cités dans l'annexe) | `wannier_dir` |
| `alignement/` | alignement du potentiel de défaut (Kumagai–Oba) : profils des 13 tailles, niveaux QE, ⟨ΔV⟩_3D | `campaigns_results_dir` (= `donnees`) + `"alignement"` |
| `kaasbjerg/` | comparaison à Kaasbjerg : DOS, A_k, sensibilités, Σ^eff (R8), cartes et métriques de la Fig. 3 (R10 c2) | id. + `"kaasbjerg"` |
| `controles/` | contrôles du ch. 4 : tailles 3m (R7), N_k^int, R_cut et chaîne repliée (R9), familles N mod 3 et convention intensive (R10 b, c3), escalier D4 (R6) | id. + `"controles"` |
| `electron_photon/` | §2.5 : σ(ω) des trois variantes, anneau de 2.33 eV, références DFT et `postw90`, tables `em_table` | id. + `"electron_photon"` |
| `ch4/` | `alignement_regions.npz` (lu par `make_figures_controles.py`, `fig_alignement_regions`) ; `table_v1_final.md`, `defauts_nombres.md`, `alignement_regions.md`, `NOTES_TGAMMA.md` (lus par aucun script ; PDF et PNG de GR retirés le 2026-10-01) | id. + `"ch4"` |

Les quatre dossiers `alignement/`, `kaasbjerg/`, `controles/` et `electron_photon/` remplacent le 2026-10-01 l'arborescence
`donnees/campagnes/<campagne>/<étape>/` (copie conforme de `GR:campagnes/`). Les fichiers y sont à plat ; ceux dont le nom était
générique portent le préfixe de leur campagne. Correspondance avec GR (commit `3305f58`, contenu identique octet par octet) :

| Ici (`donnees/`) | `GR:campagnes/` |
|---|---|
| `alignement/r10_a1_results.json`, `r10_a2_results.json`, `profiles_<S>.npz` (13) | `R/R10_plateau/a/{a1_results.json,a2_results.json,profiles_<S>.npz}` |
| `alignement/r10_c6_results.json` | `R/R10_plateau/c/c6_results.json` |
| `kaasbjerg/r10_c2_results.json`, `r10_c2_kaasbjerg_maps.npz` | `R/R10_plateau/c/{c2_results.json,c2_kaasbjerg_maps.npz}` |
| `kaasbjerg/r8_<nom>` (`7a_results.json`, `fig13_VA_interp_1meV.csv`, `dos_9x9.npz`, `dos_results.json`, `fig_results.json`, `gate_results.json`, `sens_results.json`, `sigeff_results.json`, `sigma_K_9x9.npz`, `spec_results.json`, `spectral_GKM_9x9.npz`) | `R/R8_kaasbjerg/out/<étape>/<nom>` |
| `controles/r7_d1_results.json` | `R/R7_tailles_3m/d1_8pts/d1_results.json` |
| `controles/r9_a3_results{,_plateau}.json`, `r9_b_results{,_plateau}.json`, `r9_c_results.json` | `R/R9_controles/{a,b,c}/…` |
| `controles/r10_b_results.json`, `r10_c3_results.json` | `R/R10_plateau/b/b_results.json`, `R/R10_plateau/c/c3_results.json` |
| `controles/r6_d4_results.json` | `R/R6_production_corrigee/etape2/d4/d4_results.json` |
| `electron_photon/em2_A.npz` | `EM/EM2/em2_A.npz` |
| `electron_photon/em2_postw90_sigma_ti.npz`, `em3_ring_2p33.npz`, `em3_table.{csv,md}` | `EM/EM3/{em2_postw90_sigma_ti.npz,em3_ring_2p33.npz,em_table.csv,em_table.md}` |
| `electron_photon/em_scalars.json`, `em_ring_stats.json`, `em_sigma_<variante>_N1200_eta0.04.npz` (3), `em_table.{csv,tex}` | `EM/M4_sigma/…` (mêmes noms) |

Installation (depuis la racine) :

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install -e . --no-deps
.venv/bin/python scripts/make_all_figures.py        # les 32 figures, ~25 s ; --only, --list
.venv/bin/python scripts/make_tables.py             # les huit tableaux du ch. 4 et leur index ; --only, --list, --check
```

LaTeX est requis (le texte des figures est composé par `text.usetex`). Les scripts écrivent dans `figures/<chapitre>/` ;
`--outdir` de chaque script change le dossier. `memoire/figures/` contient encore les versions incluses dans le PDF actuel :
elles sont remplacées chapitre par chapitre à la réécriture.

### Historique de la copie

1. **2026-09-30, copie complète** depuis `GR:` au tag (commits `bbed6f0`, `12da2f0`, `3e2e5ad`) : `src/`, `scripts/{fig,m,t,epw,validation,slurm}/`,
   `tests/`, `GR:results/` → `donnees/`. Recette sur une VM Linux (Python 3.10, NumPy 2.2.6, Matplotlib 3.10.9) : `donnees/` identique au
   tag octet par octet (un README mis à jour excepté), `src/`, `scripts/`, `tests/` identiques (`diff -r` vide), `pytest` 233 réussis et
   5 sautés, 47 PDF sans erreur ni lecture hors de `donnees/` et `config/`, 38 / 47 identiques au bit aux PDF du tag et les 9 autres
   (cartes en couleur) identiques au pixel à 100 ppp.
2. **2026-10-01, réduction** à ce qui trace les figures (décision : le code de production reste dans GR, on n'entretient pas deux copies).
   Retirés : `src/graphene_raman/` hors des quatre modules ci-dessus (34 fichiers), `tests/`, `scripts/{m,t,epw,validation,slurm}/`,
   `donnees/wannier/` sauf `27x27/wannier.wout` (33 Mo). Tout reste lisible dans le commit `bbed6f0` de ce dépôt et dans GR au tag.
3. **2026-10-01, ajouts** : `calculs/` (entrées rapatriées de Rorqual) ; `donnees/ch4/NOTES_TGAMMA.md`, `donnees/epw/NOTES_EPW{,_REPERES}.md`
   (copies des notes de GR, non suivies par git là-bas) ; sources de chiffres du texte, lues par aucune figure : `c2_results.json` (R10),
   `{dos,gate,spec,fig}_results.json` (R8), `em_table.*` et `em_ring_stats.json` (EM), puis `b_results.json`, `c3_results.json`, `c6_results.json` (R10) et `d4_results.json` (R6) ; `scripts/make_all_figures.py` ;
   scripts de figures remontés de `scripts/fig/` à `scripts/`.
4. **2026-10-01, `donnees/campagnes/` aplati** en `alignement/`, `kaasbjerg/`, `controles/`, `electron_photon/` (tableau ci-dessus) ;
   `campaigns_results_dir` = `donnees` ; chemins ajustés dans `make_figures_{controles,em,kaasbjerg}.py`. Recette (VM Linux) : 47 PDF
   identiques octet par octet à ceux d'avant le changement, aucune lecture hors de `donnees/` et `config/`, 121 md5 OK, chaque fichier
   déplacé de même md5 qu'avant.
5. **2026-10-01, `scripts/chiffres_ch4.py`** (propre à ce dépôt, absent de GR) : lectures et statistiques sur `donnees/M2_plateau/` et `config/`, sortie `donnees/ch4/chiffres_complementaires.{md,csv}` (159 lignes, chaque valeur avec son fichier et sa clé) ; `MD5SUMS_2026-10-01.txt` : 123 fichiers.
6. **2026-10-01, `scripts/make_tables.py`** (propre à ce dépôt) : couche d'organisation par tableau du mémoire (décision : on ne réorganise pas
   `donnees/`). Une fonction par tableau déclare la valeur et la source de chaque cellule, contrôle la cohérence entre fichiers
   (C_N de la config = C_N des produits M ; `level2_families.csv` = `M_analysis.npz` ; M̄^L aligné − brut = N²|C_N| ; `m_rcut_convergence.csv`
   = `r10_c2_results.json` plateau_ws ; niveau 1 R_cut 3 = `level2_summary.csv` ; grille interne 300² = production) et écrit
   `memoire/tables/<nom>.tex` (tabular seul, légende et `\label` dans le chapitre) et `memoire/tables/SOURCES.md` (index). Sortie déterministe.
   Deux tableaux nouveaux le même jour : `tab:kaasbjerg` (corps, §4.2.5) et `tab:grille_interne` (annexe D, chaîne T).

**Recette après réduction (2026-10-01, Mac, Python 3.12.1, environnement de `requirements.txt`)** : `scripts/make_all_figures.py`
→ 47 figures, 94 fichiers PDF et PNG **identiques octet par octet** à `GR:figures/` au tag. Cette comparaison ne sera pas entretenue ;
elle sera refaite une fois, au verrouillage du mémoire, contre des sommes md5 enregistrées dans ce dépôt.

Écarts volontaires avec GR au tag : `config/production.json` (chemins, dont `campaigns_results_dir` = `donnees`) ; `scripts/make_figures.py` **retiré le 2026-10-01** :
ses trois figures du mémoire (`fig_Ved_zoom`, `fig_ks_reconstruction`, `fig_level2`) sont tracées par `make_figures_defaut.py`, code repris
à l'identique (9 PDF identiques au bit avant / après dans la VM) ; ses onze figures de travail sont retirées de `figures/` ; `level{1,2}_summary.csv`
restent produits par `GR:scripts/fig/make_figures.py --write-summaries` ; dans les huit scripts, la racine du dépôt est `parents[1]` au lieu de `parents[2]` ; `make_figures_{controles,em,kaasbjerg}.py`
lisent les dossiers plats de `donnees/` (noms de fichiers préfixés, voir ci-dessus) ; `make_figures_controles.py` : quatre figures écartées
retirées le 2026-10-01 (`fig_{levels_vs_invN,resonance_vs_nkint,size_3m,localized_3m}`, d9f821f) et `fig_alignement_regions` ajoutée (tracé porté de
`GR:campagnes/M/ch4/ch4_chiffres.py`, `make_regions_figure` : lit `donnees/ch4/alignement_regions.npz` au lieu de recalculer les statistiques,
point décimal dans la légende, marqueurs de famille en `MUTED` au lieu de `gray`) ; `fig_offset_profiles_13` au point décimal (1.0 Å, 1.42 Å, 0.75 r_max).
`make_figures_kaasbjerg.py` (2026-10-01, docstring de Greg) : variante η_t = η_G retirée de toutes les figures ; `dos_c` réduite à ρ − ρ₀ (grille 600²,
non aligné et Kumagai–Oba, 2 panneaux ; ρ total et grille 300² retirés) ; `spectral_GKM` réduite à Kumagai–Oba (6 → 2 panneaux), seuil d'affichage des maxima 1 → 2 % (retire cinq points isolés de la résonance à −0.17 eV) ; `superposition`
réduite au spin compté (4 → 2 panneaux) ; `sensibilites` : ordonnée « position du max » et ligne de Kaasbjerg dans la légende ; point décimal partout.

**2026-10-05** : vocabulaire « brut » / « aligné » (décision G du 2026-10-04) appliqué aux étiquettes de `make_figures_controles.py` (`FIG_LABEL`,
`fig_rcut_aligned`, `fig_folded_vs_R7`, `fig_kaasbjerg_plateau_ws`), `make_figures_kaasbjerg.py` (`lab`, titres de `sigma_K`) et `make_tables.py`
(`tab:kaasbjerg`) ; axe « Rayon de coupure $R_\mathrm{cut}$ (indices réduits) » au lieu de « (mailles) » (`make_figures_defaut.py`, `make_figures_controles.py`) ;
`tab:tests_T` ramené à trois lignes (référence 5×5, $\mathcal{G}^{(0)}_\mathcal{C}$ par lots, positivité ; grille interne retirée, doublon de `tab:grille_interne`) ;
notation de l'amas $M_\mathcal{C}$, $\mathcal{G}^{(0)}_\mathcal{C}$, $T_\mathcal{C}$ (G). **Les PDF de `memoire/figures/` et `figures/electron_defect/` n'ont pas encore été
régénérés avec ces étiquettes** (à faire sur le Mac : `python scripts/make_all_figures.py`, puis copie dans `memoire/figures/`). `fig_M_map_final` retirée (bloc du script et PDF/PNG).

---

## 1. Figures incluses dans le mémoire (32 ; ch. 4 → ch. M `défauts.tex` et ch. T `défauts2.tex` depuis la scission du 2026-10-04, annexe D = `annexes/Convergence et paramètres de calcul.tex`, lignes du 2026-10-05)

État par rapport à `memoire/figures/` (comparaison au pixel, 100 ppp, contre les PDF du tag) :
**même contenu** = seules les métadonnées diffèrent, rien à faire ; **R10** = le mémoire a la version R6, la
version finale diffère et sera installée avec la réécriture du ch. 4 ; **ch. 2 refaite** = redessinée dans le style du
mémoire (taille et mise en page changent), à valider.

| Label | Fichier du mémoire | .tex:ligne | Producteur | Données lues | État |
|---|---|---|---|---|---|
| `fig:KB` | `KB_projectors_C.pdf` | théorie:191 | `make_figures_electron.py` → `fig_kb_pseudo_C` (**nom différent**) | `donnees/electron/C.upf` | ch. 2 refaite |
| `fig:convergence_dft` | `fig_electron_convergence.pdf` | théorie:319 | `make_figures_electron.py` | `donnees/electron/{ecut,ecut_cross,kpoint,smearing}.dat` | ch. 2 refaite |
| `fig:resultats_electrons` | `fig_ebands_edos.pdf` | théorie:326 | `make_figures_electron.py` | `donnees/electron/{ebands,edos}.dat` | ch. 2 refaite |
| `fig:phonon_results` | `fig_epw_phonons.pdf` | théorie:447 | `make_figures_epw.py` (variante : `make_figures_phonons.py` → `fig_phfreq_phdos`, données `donnees/phonon/`) | `donnees/epw/{validation,phdos}_24k24q_mv0.02.npz` | même contenu |
| `fig:Ved_zoom` | `fig_Ved_zoom.pdf` | défauts:307 | `make_figures_defaut.py` | `donnees/M2_plateau/ved_analysis.npz` | même contenu |
| `fig:Ved` | `fig_Ved.pdf` | défauts:322 | `make_figures_defaut.py` | `ved_analysis.npz` + C_N de `config/production.json` | **R10** |
| `fig:M_scaling` | `fig_M_scaling_final.pdf` | défauts:370 | `make_figures_defaut.py` | `M_analysis.npz` | **R10** |
| `fig:kaasbjerg_M` | `fig_kaasbjerg_plateau_ws.pdf` | défauts:390 | `make_figures_controles.py` (quatre panneaux : brut (a, b), aligné (c, d)) | `kaasbjerg/r10_c2_kaasbjerg_maps.npz` | installée le 2026-10-03 |
| `fig:M_locality` | `fig_locality_final.pdf` | défauts:405 | `make_figures_defaut.py` | `mwr_locality.npz` | **R10** |
| `fig:ks_reconstruction` | `fig_ks_reconstruction.pdf` | annexe D:46 | `make_figures_defaut.py` | `ks_reconstruction.npz` | même contenu |
| `fig:rcut_aligned` | `fig_rcut_aligned.pdf` | annexe D:35 | `make_figures_controles.py` | `controles/r9_a3_results{,_plateau}.json` | installée le 2026-10-05 |
| `fig:offset_profiles_13` | `fig_offset_profiles_13.pdf` | annexe D (chaîne M) | `make_figures_controles.py` | `alignement/r10_a1_results.json`, `alignement/profiles_<S>.npz` | installée le 2026-10-05 |
| `fig:alignement_regions` | `fig_alignement_regions.pdf` | annexe D (chaîne M) | `make_figures_controles.py` (tracé seulement) | `donnees/ch4/alignement_regions.npz` | installée le 2026-10-05 |
| `fig:convergence` | `fig_convergence.pdf` | annexe D:74 (depuis le 2026-10-04) | `make_figures_defaut.py` | `specwd_{5x5,6x6,7x7,8x8,9x9,12x12}_prod.npz` | **R10** |
| `fig:level2` | `fig_level2.pdf` | défauts2:217 | `make_figures_defaut.py` | `specwd_*_prod.npz` | **R10** |
| `fig:spectral` | `fig_spectral_final.pdf` | défauts2:246 | `make_figures_defaut.py` | `resonance_9x9.npz`, `resonance_criteria_9x9.npz` | **R10** |
| `fig:folded_vs_R7` | `fig_folded_vs_R7.pdf` | défauts2:230 | `make_figures_controles.py` | `controles/r9_c_results.json` | installée le 2026-10-05 |
| `fig:resonance_vs_nkint_plateau` | `fig_resonance_vs_nkint_plateau.pdf` | annexe D:98 | `make_figures_controles.py` | `controles/r9_b_results_plateau.json` | installée le 2026-10-04 |
| `fig:kaasbjerg_superposition` | `fig_kaasbjerg_superposition.pdf` | défauts2:274 | `make_figures_kaasbjerg.py` | `kaasbjerg/r8_dos_9x9.npz`, `r8_fig13_VA_interp_1meV.csv` | installée le 2026-10-05 |
| `fig:kaasbjerg_spectral_GKM` | `fig_kaasbjerg_spectral_GKM.pdf` | défauts2:281 | idem | `kaasbjerg/r8_spectral_GKM_9x9.npz` | installée le 2026-10-05 |
| `fig:kaasbjerg_sigma_K` | `fig_kaasbjerg_sigma_K.pdf` | défauts2:288 | idem | `kaasbjerg/r8_sigma_K_9x9.npz`, `r8_sigeff_results.json` | installée le 2026-10-05 |
| `fig:kaasbjerg_sensibilites` | `fig_kaasbjerg_sensibilites.pdf` | annexe D:119 | idem | `kaasbjerg/r8_sens_results.json`, `r8_7a_results.json` | installée le 2026-10-05 |
| `fig:kaasbjerg_dos_c` | `fig_kaasbjerg_dos_c.pdf` | annexe D:126 | idem | `kaasbjerg/r8_dos_9x9.npz` | installée le 2026-10-05 |
| `fig:epw_validation` | `fig_epw_validation.pdf` | eph:152 | `make_figures_epw.py` (options de production ci-dessous) | `donnees/epw/validation_24k24q_mv0.02.npz` | même contenu |
| `fig:epw_g_control` | `fig_epw_g_control.pdf` | eph:158 | idem | `donnees/epw/validation_24k24q_mv0.02.npz` | même contenu |
| `fig:epw_decay` | `fig_epw_decay.pdf` | eph:168 | idem | idem | même contenu |
| `fig:epw_kohn_degauss` | `fig_epw_kohn_degauss.pdf` | eph:180 | idem | `validation_24k24q{,_mv0.02}.npz`, `dfpt_path_freq_24k24q.npz` | même contenu |
| `fig:epw_gamma` | `fig_epw_gamma.pdf` | eph:235 | idem | `selfen_{120_dg0.0{1,2,5},240_dg0.02}_mv0.02_T{10,300}.npz` | même contenu |
| `fig:epw_phonselfen` | `fig_epw_phonselfen.pdf` | eph:290 | idem | `phself_path_1200_dg0.02_mv0.02.npz` | même contenu |
| `fig:epw_vs_ed` | `fig_epw_vs_ed.pdf` | eph:304 | idem | `selfen_240_dg0.02_mv0.02_T300.npz` + `donnees/M2_plateau/resonance_9x9.npz` | **R10** |

Sauf mention, les données du ch. 4 sont dans `donnees/M2_plateau/` et les scripts dans `scripts/`.
Options de production de `make_figures_epw.py` (passées par `scripts/make_all_figures.py`) :
`--prod-tag 240_dg0.02_mv0.02 --phself-tag path_1200_dg0.02_mv0.02 --val-tag 24k24q_mv0.02 --sel-suffix _mv0.02 --control --kohn-val-tags 24k24q,24k24q_mv0.02 --dfpt-tag 24k24q`.
Sans elles, les valeurs par défaut tracent l'ancienne chaîne (degauss 0.002) et ne produisent pas `fig_epw_vs_ed`.
Style commun : `src/graphene_raman/plotting/{palette.py,memoire.mplstyle}` ; `palette.save` retire les métadonnées
de date, d'où des PDF reproductibles octet par octet sur une même machine.

### Figures TikZ (aucune donnée)

`memoire/tikz/*.tex` : diagrammes dessinés à la main (cycles SCF, Dyson, matrice T, règles Raman, pp/pd, e1/h1,
échelle de Jacob). `tikz/jacob_ladder.log` est un résidu de compilation.

### Figures disponibles, pas encore incluses

| Figure | Pour | Producteur | Données |
|---|---|---|---|
| `fig_em_coupling` | §2.5 électron-photon | `make_figures_em.py` | `donnees/electron_photon/` |
| table `em_table` (pas une figure) | §2.5 électron-photon | — (produite dans GR par `campagnes/EM/M4_sigma/make_table.py` et `EM3/make_em3_data.py`) | `donnees/electron_photon/em_table.{csv,tex}`, `em_ring_stats.json`, `em3_table.{csv,md}` |
| `fig_M_map_final` retirée le 2026-10-05 (figure supprimée du chapitre, décision G du 2026-10-04 ; bloc retiré de `make_figures_defaut.py`, PDF/PNG supprimés) ; tous les contrôles du ch. 4 retenus le 2026-10-01 sont installés le 2026-10-05 (voir §1). | — | — | — |

---

## 2. Tables

Les dix tableaux des ch. M et T sont générés par `scripts/make_tables.py` dans `memoire/tables/` et entrent dans `défauts.tex`, `défauts2.tex` ou l'annexe D par `\input{tables/<nom>}` (tous installés au 2026-10-05 ; `make_tables.py --check` : 10/10 à jour). Valeur et source de chaque cellule :
`memoire/tables/SOURCES.md`. Les tableaux du ch. 5 et de l'annexe D restent saisis à la main.

| Label | .tex:ligne | Source |
|---|---|---|
| `tab:échantillonnage` | défauts:299 | `make_tables.py` → `tables/echantillonnage.tex` : `M2_plateau/sampling_table.csv` ; C_N : `config/production.json` |
| `tab:L_NL` | défauts:360 (bloc Convention intensive, cinq colonnes) | `make_tables.py` → `tables/L_NL.tex` : `M2_plateau/M_analysis.npz` (lnl_*), `M2_plateau/lnl_frobenius.csv` |
| `tab:alignement` | défauts:337 (nouveau, 2026-10-04) | `make_tables.py` → `tables/alignement.tex` : `donnees/ch4/alignement_regions.npz` ; décalage du vide : `alignement/r10_c6_results.json` |
| `tab:rcut_M` | annexe D:27 (depuis le 2026-10-03) | `make_tables.py` → `tables/rcut_M.tex` : aligné `M2_plateau/m_rcut_convergence.csv` (= `kaasbjerg/r10_c2_results.json`, plateau_ws), brut `kaasbjerg/r10_c2_results.json` (tel_quel) |
| `tab:tests_M` | annexe D:58 (depuis le 2026-10-03) | `make_tables.py` → `tables/tests_M.tex` : `M2_plateau/M_tests_summary.csv`, `M2_plateau/ks_reconstruction.npz` |
| `tab:convergence_gamma` | annexe D:83 (depuis le 2026-10-04) | `make_tables.py` → `tables/convergence_gamma.tex` : `M2_plateau/level1_summary.csv` |
| `tab:tests_T` | annexe D:111 (depuis le 2026-10-05 ; trois lignes : référence 5×5, g0 par lots, positivité) | `make_tables.py` → `tables/tests_T.tex` : `M2_plateau/{M_tests_summary.csv,resonance_9x9.npz}` ; seuil de positivité : `ch4/NOTES_TGAMMA.md` |
| `tab:kaasbjerg` | défauts2:266 (colonnes brut / aligné depuis le 2026-10-05) | `make_tables.py` → `tables/kaasbjerg.tex` : `kaasbjerg/r8_{dos,spec,7a}_results.json`, `kaasbjerg/r10_c2_results.json` ; A_cell\|M\| ~70 eV Å² de Kaasbjerg : lit. (sa Fig. 3, non numérisée) |
| `tab:grille_interne` | annexe D:90 | `make_tables.py` → `tables/grille_interne.tex` : `M2_plateau/nkint_check_9x9.csv` |
| `tab:kohn_chaines` | eph:194 | `donnees/epw/d2_extract_24k24q{,_mv0.02}.npz`, `validation_24k24q{,_mv0.02}.npz` |
| `tab:gamma_ep_conv` | eph:219 | `donnees/epw/selfen_*_T300.npz` |
| `tab:gamma_ph_conv` | eph:254 | `donnees/epw/NOTES_EPW.md` (table de convergence de γ(A₁′, K), l. 295) : **aucun fichier de données** ne porte ces 18 valeurs, tirées des `epw.out` des runs `calculs/ch5_epw/24k-24q_mv0.02/epw6_phself_K_*` restés sur Rorqual ; un csv est à extraire des notes (TODO) |
| `tab:gamma_ph_prod` | eph:275 | `donnees/epw/phself_path_1200_dg0.02_mv0.02.npz` |
| `tab:param_dft` | annexes/paramètres:10 | `calculs/ch2_electrons/bandes_dos/{scf,nscf,dos}.in` ; convergence : `calculs/ch2_electrons/convergence/` |
| `tab:param_dfpt` | paramètres:37 | `calculs/ch2_phonons/{scf,ph,q2r,matdyn,matdyn.dos}.in` |
| `tab:param_wannier` | paramètres:62 | chaîne *M* : `calculs/ch4_mailles/27x27/wannier.win`, étalements dans `donnees/wannier/27x27/wannier.wout` ; chaîne *g* : `calculs/ch5_epw/24k-24q_mv0.02/epw1/{epw1.in,graphene.win}` (étalements : sortie d'EPW, sur Rorqual) |
| `tab:param_M` | annexe D:215 (lignes alignement, constantes et nombre de bandes ajoutées le 2026-10-05) | `config/production.json` ; `calculs/ch4_supercellules/<N>x<N>/{pristine,defective}/scf.in` ; `calculs/ch4_mailles/<N>x<N>/{scf,nscf}.in` |
| `tab:param_T` | annexe D:248 (ligne comparaison Kaasbjerg ajoutée le 2026-10-05) | `config/production.json` ; `donnees/ch4/NOTES_TGAMMA.md` |
| `tab:param_epw` | paramètres:143 | `calculs/ch5_epw/24k-24q_mv0.02/` (`phonons/`, `epw1/`, `epw2_selfen_*/`, `epw6_phself_*/`) ; `donnees/epw/NOTES_EPW.md` |

Les sources des quatre tables du ch. 5 sont déduites des noms de fichiers ; l'appariement valeur par valeur reste à faire.

---

## 3. Chiffres cités dans le texte (valeurs avec unité, hors paramètres d'entrée)

| Chapitre | Nb. | Provenance | Remarque |
|---|---|---|---|
| Introduction | 2 | lit. (l. 13 : 130 GPa, 97.7 %) | citées, pas de données |
| Ch. 2 théorie | 25 | §2.2 : 2.466 Å, 5.46 eV, convergence 0.1 meV → `donnees/electron/`. §2.3 : 1550.5 et 1583 cm⁻¹, écart 2 %, 468/1394/1602 cm⁻¹ → `donnees/epw/phdos_24k24q_mv0.02.npz`, `validation_24k24q_mv0.02.npz` et lit. | 100 Ry et 0.01 Ry sont des paramètres, voir `tab:param_dft` |
| Ch. 3 Raman | 8 | lit. (positions des pics G, D, 2D… ; 10 nm) | aucune donnée |
| Ch. M et T (défauts, défauts2) | 111 (v1) | `donnees/ch4/table_v1_final.md` (source des valeurs finales, avec fichier et clé de chaque valeur) ; valeurs absentes de la table (grille interne, ordres de grandeur de `fig:Ved` et `fig:M_locality`, fraction locale et A_cell·M̄(K), dispersion de max\|M\|) : `donnees/ch4/chiffres_complementaires.{md,csv}`, produit par `scripts/chiffres_ch4.py` (propre à ce dépôt) ; appariement dans `donnees/ch4/defauts_nombres.md` | ch. M réécrit par G (2026-10-01 → 04) et ch. T par C (2026-10-05) sur les valeurs R10 ; `defauts_nombres.md` (appariement v1) est périmé et ne se régénère que dans GR : à refaire au verrouillage |
| Ch. 5 EPW | 176 | `donnees/epw/*.npz` ; Γ^ed/Γ^ep (§5.3.5, l. 301–312) → `donnees/M2_plateau/ed_vs_ep_24k24q_mv0.02.npz` et `table_v1_final.md` | à apparier comme pour le ch. 4 ; l. 303–312 dépendent du ch. 4 (Γ^ed R6 → R10) |
| Conclusion | 5 | reprend ch. 4–5 (300 K, 1 %, 3 eV, 0.6 %, 14 cm⁻¹) | à revoir après la réécriture du ch. 4 |
| Résumé / abstract | 2 + 2 | reprend ch. 4–5 (300 K, 1 %) | idem |

Liste détaillée par ligne (hors ch. 4) : annexe A.

---

## 4. Ce qui n'est pas dans ce dépôt

| Quoi | Où | Conséquence |
|---|---|---|
| code de production : chaînes des matrices *M* et *T*, post-traitement d'EPW, module électron-photon, tests | `GR:src/`, `GR:scripts/{m,t,epw,validation,slurm}/`, `GR:tests/` ; aussi dans le commit `bbed6f0` de ce dépôt | aucune donnée de `donnees/` ne se recalcule ici ; les figures n'en ont pas besoin |
| matrices *M* (`M_*.npy`), fonctions d'onde (`.save`) | Rorqual (`/project`, nearline) ; sommes md5 dans `donnees/M2/` | nécessaires pour recalculer, pas pour tracer |
| sorties de Wannier90 (hamiltonien, matrices de jauge, huit grilles) | `GR:results/wannier/` | seul `27x27/wannier.wout` est gardé (étalements cités dans l'annexe) |
| produits v1 et v2 non alignés (`GR:results/M/`, produits de `GR:results/M2/`) | GR | servent seulement à la colonne « v1 » de `donnees/ch4/table_v1_final.md` |
| pilotes de campagne (`ch4_chiffres.py`, `r8_driver.py`, `r10_driver.py`, EM) et leurs rapports | `GR:campagnes/` (versionné depuis `3305f58`) | leurs sorties utiles sont dans `donnees/` |
| sorties des calculs (`*.out`, potentiels, matrices dynamiques) et lanceurs SLURM simples | Rorqual | `calculs/` ne garde que les entrées, les listes de points et les scripts qui génèrent des entrées |
| chaîne EPW à 0,002 Ry au-delà des phonons ; grilles EPW d'essai ; relaxations de la lacune ; convergence des phonons en grille **q** | Rorqual | n'alimentent aucune figure ni table ; `calculs/ch5_epw/24k-24q/` est réduit à `phonons/` et `dfpt_g_K/` |

### Contenu de `calculs/`

| Dossier | Calcul | Alimente |
|---|---|---|
| `ch2_electrons/convergence/{ecut,ecut_cross,kpoint,smearing}/` | énergie totale en fonction de la coupure (grilles 12×12 et 24×24), de la grille **k** (9 à 42) et de l'élargissement (grille 27×27) | `donnees/electron/{ecut,ecut_cross,kpoint,smearing}.dat` |
| `ch2_electrons/bandes_dos/` | SCF 27×27, NSCF 96×96, bandes, densité d'états | `donnees/electron/{ebands,edos}.dat` |
| `ch2_phonons/` | SCF 24×24, DFPT 24×24, `q2r`, `matdyn` (dispersion et DOS) | `donnees/phonon/` |
| `ch2_electron_photon/{EM1_tb,EM2}/` | éléments de position de Wannier (27×27) ; bandes DFT aux anneaux, `postw90` | `donnees/electron_photon/` |
| `ch4_supercellules/<N>x<N>/{pristine,defective}/` | SCF au point Γ et `pp.x`, 13 tailles (5 à 12, 15, 18, 21, 24, 27) | potentiel de défaut, constantes d'alignement (`donnees/M2_plateau/`, `donnees/alignement/`) |
| `ch4_mailles/<N>x<N>/` | cellule unitaire sur la grille complète : SCF, NSCF, `pw2wannier90`, Wannier90 ; grilles 5 à 12 et 24, 25, 27, 28, 32 | matrices *M* ; `donnees/wannier/27x27/wannier.wout` |
| `ch5_epw/24k-24q_mv0.02/` | chaîne EPW de production (0,02 Ry) : phonons, `epw1`, auto-énergies, contrôles de *g* | `donnees/epw/*_mv0.02*.npz` |
| `ch5_epw/24k-24q/{phonons,dfpt_g_K}/` | phonons et DFPT directe à 0,002 Ry | `donnees/epw/{validation,dfpt_path_freq}_24k24q.npz` (`fig_epw_kohn_degauss`) |

Les entrées sont copiées telles qu'elles ont tourné : `outdir` et `pseudo_dir` pointent vers l'arborescence de Rorqual.

---

## Annexe A — chiffres avec unité, ligne par ligne (hors ch. 4)

Extraction automatique : chiffre suivi d'une unité (eV, meV, Å, Ry, K, cm⁻¹, %, GPa, nm, Bohr). Elle inclut
des paramètres d'entrée, qu'on laisse de côté pour la provenance. `[table]` ou `[figure]` indique une ligne dans un
flottant.

```
introduction.tex:13: 130$~GPa | 97.7$~\%
théorie.tex:316: 0.1 meV | 2.466$~\AA | 0.006\,\AA | 2.46\,\AA
théorie.tex:322 [figure]: 100$ Ry | 100$ Ry | 0.1 meV
théorie.tex:325: 100$ Ry | 0.01$ Ry | 100$ Ry | 0.01$ Ry
théorie.tex:329 [figure]: 0.01$ Ry
théorie.tex:333: 5.46$ eV
théorie.tex:337: 0.01$ Ry
théorie.tex:446: 0.02$ Ry | 1550.5$ cm$^{-1 | 2~\% | 1583$ cm$^{-1
théorie.tex:450 [figure]: 0.02$ Ry | 3$ cm$^{-1
théorie.tex:458: 3$ cm$^{-1 | 468 cm$^{-1 | 1394 cm$^{-1 | 1602 cm$^{-1
théorie.tex:613: 0.1 meV
raman.tex:45: 10$ nm
raman.tex:65: 1582$ cm$^{-1
raman.tex:67: 1350$ cm$^{-1 | 1600$ cm$^{-1 | 1100$ cm$^{-1
raman.tex:68: 2700$ cm$^{-1 | 2450$ cm$^{-1 | 3200$ cm$^{-1
eph.tex:129: 2.466$~\AA | 30$~Bohr | 100$~Ry | 0.02$~Ry | 4.2389$~eV | 0.01$~meV
eph.tex:133: 25$~eV | 15$~eV | 2.5$~eV | 0.6106$~\AA | 0.9655$~\AA | 3.7627$~\AA | 0.1~\%
eph.tex:137: 0.018$~\AA | 0.014$~\AA | 0.012$~\AA | 5.46$~eV | 0.02$~eV | 0.002$~\AA
eph.tex:141: 4.2389$~eV | 3.5$~eV | 300$~K | 10$~K | 0.02$~eV | 0.02$~eV
eph.tex:149: 3$~eV | 0.81$~meV | 4.1$~meV | 20$~meV | 2.5$~eV | 4.7$~cm$^{-1 | 0.6$~meV | 0.09$~meV
eph.tex:151: 0.2~\% | 0.4~\%
eph.tex:155 [figure]: 2.5$~eV
eph.tex:161 [figure]: 0.2\,\% | 0.4\,\%
eph.tex:167: 15$~eV | 2\times10^{-5}$~eV | 5\times 10^{-4}$~eV | 17$~eV | 6\times 10^{-4}$~eV
eph.tex:175: 0.002$~Ry | 0.02$~Ry | 2.0\times 10^{-3}$~eV
eph.tex:179: 0.002$~Ry | 27$~meV | 1312$~cm$^{-1 | 972$~cm$^{-1 | 0.02$~Ry | 1274.8$~cm$^{-1 | 1289.2$~cm$^{-1 | 0.02$~Ry | 17$~cm$^{-1 | 14$~cm$^{-1 | 2~\% | 1303$~cm$^{-1
eph.tex:183 [figure]: 0.002$~Ry | 0.02$~Ry | 0.002$~Ry | 120.5$~meV
eph.tex:189: 18~\text{eV
eph.tex:191: 5.46$~eV | 5.27$~\AA | 0.002$~Ry | 0.02$~Ry | 0.002$~Ry
eph.tex:193: 1~\% | 30~\% | 1~\% | 2~\%
eph.tex:201 [table]: 2$\,\AA | 2$\,\AA
eph.tex:203 [table]: 0.002$~Ry
eph.tex:205 [table]: 0.02$~Ry
eph.tex:214: 300$~K | 10$~K | 300$~K
eph.tex:218: 3$~eV | 1.2$~eV | 0.3~\% | 0.01$~eV | 2.2~\% | 0.05$~eV | 0.02$~eV | 2.8~\% | 3$~eV | 1.7~\% | 1.2$~eV | 5~\% | 0.02$~eV
eph.tex:221 [table]: 300$~K
eph.tex:225 [table]: 3$~eV | 1.2$~eV
eph.tex:227 [table]: 3.0~\% | 3.5~\%
eph.tex:228 [table]: 2.8~\% | 1.7~\%
eph.tex:229 [table]: 0.6~\% | 0.6~\%
eph.tex:231 [table]: 3.5~\% | 4.1~\%
eph.tex:238 [figure]: 0.02$~eV | 300$~K | 10$~K | 300$~K | 0.02$~eV
eph.tex:244: 3$~eV | 300$~K | 57.0$~meV | 21.7$~meV | 1.2$~eV | 1.88$~eV | 10$~K | 3.5~\% | 19$~meV | 0.19$~eV | 1$~meV | 300$~K | 0.6$~eV
eph.tex:253: 0.02$~eV | 37~\% | 0.4~\% | 0.05$~eV | 2.798$~meV | 0.01$~eV | 5~\% | 0.02$~eV
eph.tex:256 [table]: 10$~K | 0.02$~eV
eph.tex:260 [table]: 0.01$~eV | 0.02$~eV | 0.05$~eV
eph.tex:263 [table]: 37~\%
eph.tex:264 [table]: 31~\%
eph.tex:265 [table]: 6.8~\%
eph.tex:266 [table]: 0.4~\%
eph.tex:267 [table]: 4.7~\% | 0.01~\%
eph.tex:274: 11.1$~cm$^{-1 | 22.6$~cm$^{-1 | 10$~K | 22$~cm$^{-1 | 9~\% | 300$~K | 158$~meV
eph.tex:277 [table]: 0.02$~eV
eph.tex:293 [figure]: 300$~K | 0.02$~eV | 300$~K | 10$~K
eph.tex:299: 5.46$~eV | 0.691$~meV | 1.402$~meV | 2.798$~meV | 0.2~\% | 1~\%
eph.tex:303: 300$~K | 1~\% | 0.02$~eV | 3$~eV
eph.tex:307 [figure]: 300$~K | 0.02$~eV | 1~\% | 0.02$~eV
eph.tex:310: 0.215$~eV | 0.1~\%
eph.tex:312: 300$~K | 3.5~\% | 10$~K
eph.tex:319: 1~\% | 300$~K
eph.tex:321: 1~\% | 0.02$~Ry | 14$~cm$^{-1
conclusion.tex:12: 300$~K | 1~\% | 3$~eV
conclusion.tex:16: 0.6~\% | 14$~cm$^{-1
résumé.tex:7: 300$~K | 1~\%
abstract.tex:6: 300$~K | 1$\%
```
