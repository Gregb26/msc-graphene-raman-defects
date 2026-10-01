# TODO — mémoire de maîtrise

Liste de travail unique du dépôt.

Mise à jour : 2026-10-01, 11 h 45. Les items terminés sont retirés de la liste (l'historique est dans git).

---

## Chantier 1 : réécriture du ch. 4

Section par section : C propose, G tranche, C applique et compile. Un tableau généré par section (`scripts/make_tables.py` → `memoire/tables/`).

- [ ] **C** — Créer `scripts/make_tables.py` et `memoire/tables/` (les scripts sont à la racine de `scripts/` depuis le 2026-10-01)
- [ ] §4.1.5 Détails computationnels de M : introduire l'alignement de Kumagai–Oba (C_N) ; `fig_offset_profiles_13` et `alignement_regions` en annexe, une phrase de renvoi
- [ ] §4.1.6 Taille des super-cellules — `tab:échantillonnage` : V̄^L(a_CC) **aligné** (= brut − C_N) : +58.7, +68.4, +69.8 meV (6, 9, 12) ; −306.8, −373.2, −255.5, −288.4, −244.3 meV (5, 7, 8, 10, 11) ; ΔE_F inchangé ; ajouter une colonne C_N
- [ ] §4.1.6 Remplissage par zéros — `fig:Ved` : cœur 115 à 116 eV au site ; |V̄| < 10⁻³ du cœur dès 1.4 à 1.8 Å ; fond loin de la lacune −0.10 eV (5×5) à −0.018 eV (12×12), égal à C_N à quelques meV près ; **le « coin positif de ~0.1 eV » de la 5×5 ne tient plus** (max −0.08 eV dans les 5 % les plus éloignés)
- [ ] §4.1.6 Convention intensive — `fig:M_scaling` : « < 2 % » devient 2.1 % (non-3m) et 2.3 % (3m) par famille, 7.7 % sur les six tailles ; « écart grossière / élargie pratiquement nul pour N ≥ 7 » devient ≤ 2.4 % (−2.4, 0.0, −2.2, −1.0 % pour 7, 8, 9, 12) ; légende et texte : max|M| et test intensif sur M **brut** (R10 D6), parce que l'alignement ajoute N²|C_N| aux éléments k = k′
- [ ] §4.1.6 Point de Dirac et littérature — `fig:M_map` **alignée** (**C** : `make_figures_memoire.py` → clés `map_*_aligned`) : M̃_π 114.9 eV Å² en K, 102 à 117 sur la zone ; M̃_π* 117.6 en K, 110 à 146 (max près de Γ, |k'| = 0.11 Å⁻¹) ; M^L_∥ 92.1 en K, 83 à 94 ; M^NL_∥ 19 à 23 ; l'alignement ne change que K et son voisinage (jusqu'à 7.7 eV Å², 125 des 729 points de plus de 0.5), à dire dans la légende (terme N²|C_N| à k′ = k, étalé par le facteur de forme de la boîte). Kaasbjerg (« 3 à 4 fois inférieur » ne tient plus) : `fig_kaasbjerg_plateau_ws` dans le corps, panneaux alignés (c, d) seulement, même grandeur que sa Fig. 3 ; près de K, 81.6 (π) et 82.8 (π*) eV Å² en moyenne (77 à 87), contre ~70 chez lui
- [ ] §4.1.6 Local / non local — `tab:L_NL` (**inversion** : NL/L passe de 20 à 0.25) : **brut et aligné côte à côte** (décision du 2026-10-01, = R10 D6) : fraction locale à K 0.77 à 0.79 (brut), 0.79 à 0.82 (aligné) ; 9×9 : M̄^L(K) = 11.31 (brut) et 13.34 eV (aligné), A_cell·M̄(K) = 75.9 et 86.6 eV Å² au lieu de 17.1. Une phrase : à k = k′, l'alignement ajoute exactement N²|C_N| (1.44, 1.82, 1.31, 0.93, 2.03, 2.69 eV pour 5, 6, 7, 8, 9, 12), qui croît comme N² ; d'où la dérive en taille de la colonne alignée (3m : 13.17, 13.34, 13.91) alors que la brute est plate (10.5 à 11.4 eV) ; la matrice T ne voit pas ce terme (seules les mailles à R_cut ≤ 3 reçoivent −C_N)
- [ ] §4.1.6 Localisation Wannier — `fig:M_locality` (corps) ; `tab:rcut_M` → annexe, une phrase de renvoi. Grilles élargies : ~41 eV sur le site (35 en 12×12), ~2 eV à |R| = 1, ~0.1 eV à 3, ~0.01 eV à 5 (3.6 ordres de grandeur), plancher ~10⁻³ eV au-delà de 6 a (**pas 10⁻⁴**) ; grilles grossières : aucune décroissance (5×5 : 4.1 → 2.9 eV) ; `fig_rcut_aligned` en annexe avec `tab:rcut_M`
- [ ] §4.1.6 Autres vérifications — `fig:ks_reconstruction` (corps) ; `tab:tests_M` → annexe (+ porte A.2, convention intensive par famille) ; retirer la ligne « 16 → 20 bandes » et la phrase correspondante (l. 414)
- [ ] §4.3.4 Détails computationnels de T — « Évaluation pratique » (l. 629) : retirer « nous vérifions ce choix », justifier n_e = 8 par l'argument seul (g⁽⁰⁾ varie sur l'échelle de η, pas η/8) ; « Contrôles » (l. 633) : référence sur 5×5 seulement
- [ ] §4.3.5 Convergence (**G** reformule) — `fig:convergence`, `tab:convergence_gamma` (colonne R_cut = 4 remplie pour les six tailles), grille interne et `fig_resonance_vs_nkint_plateau` → annexe ; le corps garde les paramètres retenus (R_cut = 3, 240², η = 20 meV, 300²). Le texte rapporte les variations mesurées et les compare à l'incertitude de taille de `fig:level2` (2.4 %), qui domine (voir l'item suivant). R_cut (médiane de Γ N_cells, 240², η = 20 meV) : 0 → 1 **augmente** Γ, +7.7 à +9.4 % (3m) et +0.6 à +1.8 % (non-3m) ; 1 → 2 au plus 1.7 % ; 2 → 3 jusqu'à 1.2 % (et non < 0.4 %) ; 3 → 4 : 0.34 % pour 9×9, au plus 0.57 % (8×8, 12×12) au lieu de « 0.2 %, référence seulement » ; convergence non monotone en 3m (changement de signe entre 2 → 3 et 3 → 4) ; « gain marginal de 0.2 % » à corriger. Grille interne 300² → 600² : −0.09 % sur la fenêtre, +0.2 % sur la zone ±0.3 eV (v1 : 2.4 %), +4.8 % au point de Dirac (v1 : 5 %), décroissance monotone en N_k^int
- [ ] §4.3.5 Convergence — **supprimer le critère « mieux que 0.5 % »** (décision du 2026-10-01) : dernière phrase de la l. 675 (« Chacun des paramètres retenus pour la production est au-delà du point où le taux d'amortissement cesse de varier à mieux que 0.5 % ») ; il n'apparaît nulle part ailleurs dans le mémoire (le seuil de 0.1 meV par atome du ch. 2 est indépendant)
- [ ] §4.3.5 Taille de super-cellule — `fig:level2`, **reste dans le corps** (0.6 % devient 2.4 % ; médiane croissante en 3m)
- [ ] §4.3.5 Super-cellule et défaut isolé (paragraphe neuf, place à choisir : Taille de super-cellule ou Signatures spectrales) — `fig_folded_vs_R7` dans le corps : (a) le modèle replié suit QE pour l'état π quasi-lié de 6×6 à 27×27 ; (b) le maximum de LDOS des voisins tend vers la résonance de T (−0.18 eV) quand N → ∞. Légende : la courbe alignée vient de R9 avec C = −24.65 meV (site unique) au lieu de −25.14 meV (0.5 meV d'écart)
- [ ] §4.3.5 Tests du schéma local — `tab:tests_T` → annexe, une phrase dans le corps ; retirer les lignes 6×6, 12×12 et grille d'énergie, et les phrases correspondantes (l. 690)
- [ ] §4.3.5 Born — `fig:spectral` (Born/T : 3.3 → 46 en médiane, 16 → 203 au max ; pic de −1.24 à −0.18 eV)
- [ ] §4.3.5 Signatures spectrales (quasi-annulation à −2.5 eV retirée ; ∫δρ = −1.00 ; critères par bloc π / σ)
- [ ] §4.3.5 Comparaison avec la littérature — figures Kaasbjerg dans le corps : `superposition` (c, d), `spectral_GKM`, `sigma_K` (courbe de production seulement) ; `sensibilites` et les variantes (non aligné, η_I = η_G) en annexe
- [ ] §4.4 Conclusion du chapitre
- [ ] **C** — Installer les 8 figures R10 dans `memoire/figures/` (depuis `figures/electron_defect/`, produites par `scripts/make_all_figures.py`), plus les nouvelles retenues : corps `fig_kaasbjerg_{plateau_ws,superposition,spectral_GKM,sigma_K}`, `fig_folded_vs_R7` ; annexe `fig_offset_profiles_13`, `alignement_regions` (à porter, item suivant), `fig_rcut_aligned`, `fig_resonance_vs_nkint_plateau`, `fig_kaasbjerg_sensibilites`
- [ ] **C** — Tracer `alignement_regions` depuis msc- : les données y sont déjà (`donnees/ch4/alignement_regions.{npz,md,pdf,png}`, identiques à GR) mais aucun script de msc- ne trace la figure. Porter `make_regions_figure` de `GR:campagnes/M/ch4/ch4_chiffres.py` (≈ 30 lignes, lit seulement le npz) dans `make_figures_controles.py` sous le nom `fig_alignement_regions` → `figures/electron_defect/` ; le calcul des statistiques reste dans GR (il lit les `scf.in` de Rorqual). **Après le commit de tes retouches de ce fichier.** `PROVENANCE.md` (l. 153), recette
- [ ] **G** — Retouches des figures retenues (décision du 2026-10-01) : `plateau_ws` réduite aux panneaux alignés (c, d) ; `dos_c` fusionnée dans `superposition` (c, d) ; `spectral_GKM` (6 → 2 panneaux) et `sigma_K` (2 → 1) réduites à la courbe de production, les variantes passent dans `sensibilites` (annexe) ; `folded_vs_R7` : étiquettes « non aligné » / « aligné » (au lieu de « site unique »), C dans la légende
- [ ] **C** — Après les retouches : écarts de `make_figures_{kaasbjerg,controles}.py` avec graphene-raman dans `PROVENANCE.md` §0 ; retirer les figures écartées (`fig_levels_vs_invN`, `fig_resonance_vs_nkint`, `fig_size_3m`, `fig_localized_3m`, `fig_kaasbjerg_dos_c`) de `make_figures_*.py`, de `figures/electron_defect/` et de `PROVENANCE.md`, et leurs données si plus rien ne les lit (liste à valider par **G**) ; recette
- [ ] **C** — `PROVENANCE.md` à jour à chaque section (§0 et §4 refaits le 2026-10-01 après la réduction du dépôt)

## Chantier 2 : Annexe D, paramètres et convergence

Décision du 2026-10-01 : en annexe ce qui justifie seulement un paramètre numérique, dans le corps ce qui porte un résultat ou une limite. Restent dans le corps : `fig:level2`, `fig:M_locality`, `fig:ks_reconstruction`, `fig:epw_kohn_degauss`, `tab:gamma_ph_prod`. Vont en annexe : `fig:convergence_dft`, `fig:convergence`, `tab:convergence_gamma`, grille interne, `tab:rcut_M`, `tab:tests_M`, `tab:tests_T`, `tab:gamma_ep_conv`, `tab:gamma_ph_conv`, et (choix du 2026-10-01) `fig_offset_profiles_13`, `alignement_regions`, `fig_rcut_aligned`, `fig_resonance_vs_nkint_plateau`, `fig_kaasbjerg_sensibilites`.

Annexe D réorganisée par chaîne (DFT, DFPT, Wannier, M, T, EPW) : pour chacune, tableau des paramètres puis preuves de convergence et tests. Le corps garde les valeurs retenues et un renvoi.

- [ ] **C** — Restructurer `annexes/paramètres.tex` par chaîne (titre à revoir : « Paramètres et convergence des calculs numériques » ?)
- [ ] **C** — Ch. 4 : y placer les éléments déplacés pendant la réécriture (§4 ci-dessus)
- [ ] **C** — Ch. 2 (verrouillé) : déplacer `fig:convergence_dft` et son paragraphe, une phrase de renvoi — **après le ch. 4**, en un seul bloc avec le ch. 5
- [ ] **C** — Ch. 5 (verrouillé) : déplacer `tab:gamma_ep_conv`, `tab:gamma_ph_conv` et leurs blocs « Convergence », une phrase de renvoi — même bloc
- [ ] **C** — Vérifier tous les `\ref` vers les éléments déplacés (grep sur `memoire/`), compiler, `PROVENANCE.md` à jour

## Chantier 3 : §2.5 couplage électron-photon

- [ ] Rédiger le §2.5 (texte P28) avec `fig_em_coupling` et la table `em_table`
- [ ] Retirer « laissée hors du cadre » : intro l. 72, raman l. 297, et ailleurs (grep « électron-photon »)


## Chantier 4 : répercussions hors du ch. 4

- [ ] **C** — Ch. 2 (verrouillé) : installer les figures validées le 2026-10-01 dans `memoire/figures/` (`fig_kb_pseudo_C` remplace `KB_projectors_C` l. 193, `fig_ebands_edos` l. 328, `fig_electron_convergence` l. 321, c.-à-d. `fig:convergence_dft`, qui part ensuite en annexe D avec le bloc ch. 2 / ch. 5) et `fig_phfreq_phdos` pour `fig:phonon_results` (remplace `fig_epw_phonons`, l. 449) ; ajuster `\includegraphics`, proposer les légendes si le contenu diffère, compiler ; pour `fig_phfreq_phdos`, voir le reste « normalisation de la DOS des phonons » en bas de liste
- [ ] Ch. 5 §5.3.5 (l. 301–312) : Γ^ed/Γ^ep (médiane 0.361 → 0.554, max 2.0 → 34.8 à −0.18 eV, croisements) et `fig_epw_vs_ed` R10
- [ ] Intro l. 74 (« état quasi-lié sous la singularité de van Hove »)
- [ ] Conclusion générale l. 8–16 (non local dominant, van Hove, 0.6 %, Kaasbjerg)
- [ ] Résumé et abstract (non local dominant, facteur 3.3, van Hove)
- [ ] **C** — Apparier les 176 chiffres du ch. 5 à `donnees/epw/` (comme `defauts_nombres.md` pour le ch. 4)
- [ ] **C** — `tab:gamma_ph_conv` (eph:254, 18 valeurs) n'a aucun fichier de données : extraire un csv de `donnees/epw/NOTES_EPW.md` (table de convergence de γ(A₁′, K), l. 295 ; grilles 120² à 1200², σ = 0.01 / 0.02 / 0.05 eV, 10 K et 300 K) → `donnees/epw/phself_K_convergence.csv`, vérifier contre la table du `.tex`, mettre `MD5SUMS` et `PROVENANCE.md` à jour

## Chantier 5 (une fois tout le reste terminé) : corrections de la grammaire et orthographes. relecture complète.

## Avant le dépôt

- [ ] **C** — `calculs/` (289 fichiers, commités dans `9970ab5`) : croiser avec l'annexe D (lignes vides et points périmés relevés le 2026-10-01 : vide de 30 Bohr et troncature 2D dans `tab:param_dft` ; nombre de bandes 16 / 20, 13 tailles pour l'alignement, seuil 10⁻¹⁴ Ry des cellules unitaires dans `tab:param_M` ; fenêtre gelée −4,5 eV des grilles grossières dans `tab:param_wannier`)
- [ ] **G/R** — Rorqual : `git pull --ff-only` de graphene-raman, `pip uninstall` + `pip install -e .`, pytest, une recette avec données, ligne dans `CLEANUP.md`
- [ ] **G** — Annexe déclaration IA (`annexes/ia.tex`, à confirmer avec Michel) ; décommenter son `\include`
- [ ] **G** — README principal (structure, « Reproduire les figures », « Données lourdes », lien vers graphene-raman) : au verrouillage du dépôt
- [ ] **G/C** — Au verrouillage : enregistrer les sommes md5 des figures finales (`figures/MD5SUMS`) et refaire une fois la recette
- [ ] **G** — Fichier `LICENSE` à la racine (absent ; nécessaire avant l'archive publique)
- [ ] **G** — Archive : release GitHub de msc- → Zenodo (DOI)
- [ ] **C** — Décommenter tous les `\include` de `master_thesis.tex`, build complet, passe finale de mise en page (débordements > 10 pt : `tikz/pp`, `tikz/pd`, amplitudes de l'annexe B)
- [ ] **C** — Grep des coquilles récurrentes (Midgal, abritraires, méchanisme, absorbtion, inversions ed/ep)
- [ ] **G** — Ménage : supprimer `~/LaTeX/msc-graphene-raman-defects` (ancien clone, vérifier d'abord `git status` et `git log origin/main..`) et `~/projects/raman-graphene` (s'il est vide) ; supprimer `.git/index.lock.orphelin-claude-2026-10-01` (fichier vide laissé par Claude)



## Anciens restes, statut à vérifier

Notés avant le 2026-09-25 ; peut-être déjà faits.

- [ ] Zotero : ajouter Yates 2007, Eckmann 2012, Polanco 2018, Chen 2009, Ugeda 2010, Guandalini 2025 (PRL), Perdew–Parr–Levy–Balduz 1982, Almbladh–von Barth 1985 ; doublon Ferrari 2006 / 2006a
- [ ] C7 : 75 points k pour 27×27 (IBZ 1/12), à confirmer par `grep 'number of k points'` sur Rorqual
- [ ] Normalisation de la DOS des phonons (intégrale matdyn 3.78 au lieu de 6)

