# TODO — mémoire de maîtrise

Liste de travail unique du dépôt. Claude la met à jour à la fin de chaque session (cocher, ajouter, déplacer) ;
Greg la commite avec le reste. Dépôt du mémoire : **31 décembre 2026**.

Qui : **G** = Greg, **C** = Claude, **R** = demande Rorqual. Détails des figures, tables et chiffres : `PROVENANCE.md`.

Mise à jour : 2026-10-01, 11 h 15. Les items terminés sont retirés de la liste (l'historique est dans git).

---

## Choix à trancher (G)

- [ ] M^L à K **brut ou aligné** dans `tab:L_NL` et `fig:M_map` (9×9 : 11.31 ou 13.34 eV ; M̃_π(K) : 107.2 ou 114.9 eV Å²). L'alignement change la carte en K et autour (jusqu'à 7.7 eV Å², 125 des 729 points de plus de 0.5), pas ses extrêmes ; `fig_M_map_final` trace aujourd'hui la carte **brute** (`map_Vpi`) : si « aligné », changer `make_figures_memoire.py` (`map_*_aligned`)
- [ ] V̄^L(a_CC) **brut ou aligné** dans `tab:échantillonnage` (9×9 : +43 ou +68 meV)
- [ ] Colonne R_cut = 4 pour les six tailles dans `tab:convergence_gamma`
- [ ] Figures à ajouter au ch. 4 : les 5 `fig_kaasbjerg_*` (décidées), `alignement_regions` (?), figures de contrôle (`fig_offset_profiles_13`, `fig_levels_vs_invN`…) dans le corps, en annexe ou nulle part
- [ ] Ch. 2 : valider les 3 figures redessinées (`fig_kb_pseudo_C` remplace `KB_projectors_C`, `fig_ebands_edos`, `fig_electron_convergence`)
- [ ] Ch. 2 : `fig:phonon_results` = `fig_epw_phonons` (actuel) ou `fig_phfreq_phdos`

## Chantier 1 : réécriture du ch. 4

Section par section : C propose, G tranche, C applique et compile. Un tableau généré par section (`scripts/make_tables.py` → `memoire/tables/`).

- [ ] **C** — Créer `scripts/make_tables.py` et `memoire/tables/` (les scripts sont à la racine de `scripts/` depuis le 2026-10-01)
- [ ] §4.1.5 Détails computationnels de M : introduire l'alignement de Kumagai–Oba (C_N)
- [ ] §4.1.6 Taille des super-cellules — `tab:échantillonnage`
- [ ] §4.1.6 Remplissage par zéros — `fig:Ved` : cœur 115 à 116 eV au site ; |V̄| < 10⁻³ du cœur dès 1.4 à 1.8 Å ; fond loin de la lacune −0.10 eV (5×5) à −0.018 eV (12×12), égal à C_N à quelques meV près ; **le « coin positif de ~0.1 eV » de la 5×5 ne tient plus** (max −0.08 eV dans les 5 % les plus éloignés)
- [ ] §4.1.6 Convention intensive — `fig:M_scaling` : « < 2 % » devient 2.1 % (non-3m) et 2.3 % (3m) par famille, 7.7 % sur les six tailles ; « écart grossière / élargie pratiquement nul pour N ≥ 7 » devient ≤ 2.4 % (−2.4, 0.0, −2.2, −1.0 % pour 7, 8, 9, 12)
- [ ] §4.1.6 Point de Dirac et littérature — `fig:M_map`, Kaasbjerg (« 3 à 4 fois inférieur » ne tient plus) : sur la zone (brut), M̃_π 102 à 117 eV Å², M̃_π* 110 à 146 (max près de Γ, |k'| = 0.11 Å⁻¹), M^L_∥ 83 à 94, M^NL_∥ 19 à 23
- [ ] §4.1.6 Local / non local — `tab:L_NL` (**inversion** : NL/L passe de 20 à 0.25) : fraction locale à K 0.77 à 0.79 (brut), 0.79 à 0.82 (aligné) ; A_cell·M̄(K) pour 9×9 : 75.9 (brut) ou 86.6 (aligné) eV Å², au lieu de 17.1
- [ ] §4.1.6 Localisation Wannier — `fig:M_locality` (corps) ; `tab:rcut_M` → annexe, une phrase de renvoi. Grilles élargies : ~41 eV sur le site (35 en 12×12), ~2 eV à |R| = 1, ~0.1 eV à 3, ~0.01 eV à 5 (3.6 ordres de grandeur), plancher ~10⁻³ eV au-delà de 6 a (**pas 10⁻⁴**) ; grilles grossières : aucune décroissance (5×5 : 4.1 → 2.9 eV)
- [ ] §4.1.6 Autres vérifications — `fig:ks_reconstruction` (corps) ; `tab:tests_M` → annexe (+ porte A.2, convention intensive par famille) ; retirer la ligne « 16 → 20 bandes » et la phrase correspondante (l. 414)
- [ ] §4.3.4 Détails computationnels de T — « Évaluation pratique » (l. 629) : retirer « nous vérifions ce choix », justifier n_e = 8 par l'argument seul (g⁽⁰⁾ varie sur l'échelle de η, pas η/8) ; « Contrôles » (l. 633) : référence sur 5×5 seulement
- [ ] §4.3.5 Convergence — `fig:convergence`, `tab:convergence_gamma`, grille interne → annexe ; le corps garde les paramètres retenus et le critère « < 0.5 % » (R_cut 0 → 1 augmente maintenant Γ). Grille interne 300² → 600² : −0.09 % sur la fenêtre, +0.2 % sur la zone ±0.3 eV (v1 : 2.4 %), +4.8 % au point de Dirac (v1 : 5 %), décroissance monotone en N_k^int
- [ ] §4.3.5 Taille de super-cellule — `fig:level2`, **reste dans le corps** (0.6 % devient 2.4 % ; médiane croissante en 3m)
- [ ] §4.3.5 Tests du schéma local — `tab:tests_T` → annexe, une phrase dans le corps ; retirer les lignes 6×6, 12×12 et grille d'énergie, et les phrases correspondantes (l. 690)
- [ ] §4.3.5 Born — `fig:spectral` (Born/T : 3.3 → 46 en médiane, 16 → 203 au max ; pic de −1.24 à −0.18 eV)
- [ ] §4.3.5 Signatures spectrales (quasi-annulation à −2.5 eV retirée ; ∫δρ = −1.00 ; critères par bloc π / σ)
- [ ] §4.3.5 Comparaison avec la littérature
- [ ] §4.4 Conclusion du chapitre
- [ ] **C** — Installer les 8 figures R10 dans `memoire/figures/` (depuis `figures/electron_defect/`, produites par `scripts/make_all_figures.py`), plus les nouvelles retenues
- [ ] **C** — `PROVENANCE.md` à jour à chaque section (§0 et §4 refaits le 2026-10-01 après la réduction du dépôt)

## Chantier 2 : Annexe D, paramètres et convergence

Décision du 2026-10-01 : en annexe ce qui justifie seulement un paramètre numérique, dans le corps ce qui porte un résultat ou une limite. Restent dans le corps : `fig:level2`, `fig:M_locality`, `fig:ks_reconstruction`, `fig:epw_kohn_degauss`, `tab:gamma_ph_prod`. Vont en annexe : `fig:convergence_dft`, `fig:convergence`, `tab:convergence_gamma`, grille interne, `tab:rcut_M`, `tab:tests_M`, `tab:tests_T`, `tab:gamma_ep_conv`, `tab:gamma_ph_conv`.

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

