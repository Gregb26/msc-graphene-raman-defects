# TODO — mémoire de maîtrise

Liste de travail unique du dépôt. Claude la met à jour à la fin de chaque session (cocher, ajouter, déplacer) ;
Greg la commite avec le reste. Dépôt du mémoire : **31 décembre 2026**.

Qui : **G** = Greg, **C** = Claude, **R** = demande Rorqual. Détails des figures, tables et chiffres : `PROVENANCE.md`.

Mise à jour : 2026-10-01, 10 h 30.

---

## 1. Urgent : sauvegarde et versionnement

- [x] 2026-10-01 — `graphene-raman/campagnes/` versionné (GR `3305f58`, 647 fichiers) ; `notes/` reste gitignoré dans GR mais ses trois fichiers sont copiés ici
- [x] 2026-10-01 — Notes copiées : `donnees/ch4/NOTES_TGAMMA.md`, `donnees/epw/NOTES_EPW.md`, `donnees/epw/NOTES_EPW_REPERES.md` (sources de `tab:tests_T`, `tab:param_T`, `tab:param_epw`)
- [x] 2026-10-01 — `c2_results.json` copié dans `donnees/campagnes/R10_plateau/c/` (comparaison Kaasbjerg, 77 à 83 eV Å²) ; `MD5SUMS` et `campagnes/README.md` à jour
- [x] 2026-10-01 — `make_figures.py` ne réécrit plus `level{1,2}_summary.csv` (option `--write-summaries`) : corrigé dans graphene-raman et recopié ici
- [x] 2026-10-01 — Commité dans graphene-raman (`3305f58`, après le tag) : `make_figures.py --write-summaries`, documentation
- [x] 2026-10-01 — `TODO.md`, `calculs/`, réduction du dépôt commités (`9970ab5`, `d83a8e7`)
- [ ] **G** — Pousser : msc- a 1 commit d'avance sur `origin/main` (`d83a8e7`)
- [ ] **G** — Coller les nouvelles instructions du projet : seule la ligne `TODO.md` a été ajoutée ; le reste cite encore `analyse/`, `scripts_figures/` et CLAUDE.md, et le texte du 2026-10-01 est périmé depuis la réduction du dépôt → **C** fournit une version à jour
- [ ] **G** — Copier dans `donnees/campagnes/` (mêmes chemins relatifs que dans GR, ~0.4 Mo, tous versionnés dans GR `3305f58`) les sources des chiffres nouveaux du ch. 4 encore absentes ; leurs valeurs sont déjà recopiées dans `donnees/ch4/table_v1_final.md`, mais pas les fichiers : `R10_plateau/b/b_results.json` (familles : gap à Γ, ΔE_F, occupations ; table §g), `R10_plateau/c/c3_results.json` (convention intensive par famille), `R10_plateau/c/c6_results.json` (⟨ΔV⟩_3D, §k), `R8_kaasbjerg/out/dos/dos_results.json` et `out/spec/spec_results.json` (chiffres du texte des 5 figures Kaasbjerg, §h), `R6_production_corrigee/etape2/b3/b3_results_M2.json` (convergence en bandes, §c), `R6_production_corrigee/etape2/d4/d4_results.json` (escalier D4, §b) ; puis `MD5SUMS` et `campagnes/README.md`

## 2. Chiffres manquants du ch. 4 (à trancher avant la réécriture)

Aucune valeur finale nulle part. **Décision du 2026-10-01 : les trois tests sont retirés du mémoire, rien n'est relancé.** Les retraits dans le texte sont faits pendant la réécriture (§4).

- [x] **G** — Retiré : `tab:tests_M`, « 16 → 20 bandes » (v1 : 1.2×10⁻⁷) : marqué « non rejouable » dans `M_tests_summary.csv`
- [x] **G** — Retiré : `tab:tests_T`, références 6×6 et 12×12 contre l'inversion dense (v1 : 6.1×10⁻⁹, 3.7×10⁻⁹) ; seul le 5×5 est refait (1.80×10⁻¹³)
- [x] **G** — Retiré : `tab:tests_T`, grille d'énergie n_e = 8 contre 32 (v1 : 8×10⁻⁴ / 5×10⁻³ / 1.5×10⁻² ; 3×10⁻⁴ sur la médiane)

À calculer ici, données dans `donnees/` :

- [ ] **C** — `fig:M_map` sur toute la zone : max de M̃_π*, plages de M^NL_∥ et M^L_∥ (`M_analysis.npz` : clés `map_Vpi*`, `map_Lpar*`, `map_Npar*`, brutes et `_aligned`, présentes)
- [ ] **C** — Grille interne : écart sur la zone ±0.3 eV et au point de Dirac (`nkint_check_9x9.csv` : colonnes `z_n`, `z_medG`, `z_medRe`, présentes)
- [ ] **C** — Ordres de grandeur lus sur `fig_Ved` et `fig_locality_final` R10 (cœur, fond, coin 5×5, plancher)

## 3. Choix à trancher (G)

- [ ] M^L à K **brut ou aligné** dans `tab:L_NL` et `fig:M_map` (9×9 : 11.31 ou 13.34 eV ; M̃_π(K) : 107.2 ou 114.9 eV Å²)
- [ ] V̄^L(a_CC) **brut ou aligné** dans `tab:échantillonnage` (9×9 : +43 ou +68 meV)
- [ ] Colonne R_cut = 4 pour les six tailles dans `tab:convergence_gamma`
- [ ] Figures à ajouter au ch. 4 : les 5 `fig_kaasbjerg_*` (décidées), `alignement_regions` (?), figures de contrôle (`fig_offset_profiles_13`, `fig_levels_vs_invN`…) dans le corps, en annexe ou nulle part
- [ ] Ch. 2 : valider les 3 figures redessinées (`fig_kb_pseudo_C` remplace `KB_projectors_C`, `fig_ebands_edos`, `fig_electron_convergence`)
- [ ] Ch. 2 : `fig:phonon_results` = `fig_epw_phonons` (actuel) ou `fig_phfreq_phdos`
- [x] 2026-10-01 — **Convergence et tests en annexe** (adopté). Critère : en annexe ce qui justifie seulement un paramètre numérique ; dans le corps ce qui porte un résultat ou une limite. Restent dans le corps : `fig:level2` (non-convergence en taille), `fig:M_locality`, `fig:ks_reconstruction`, `fig:epw_kohn_degauss`, `tab:gamma_ph_prod`. Vont en annexe : `fig:convergence_dft`, `fig:convergence`, `tab:convergence_gamma`, grille interne, `tab:rcut_M`, `tab:tests_M`, `tab:tests_T`, `tab:gamma_ep_conv`, `tab:gamma_ph_conv`. Voir §4 bis.

## 4. Chantier 2a : réécriture du ch. 4

Section par section : C propose, G tranche, C applique et compile. Un tableau généré par section (`scripts/make_tables.py` → `memoire/tables/`).

- [ ] **C** — Créer `scripts/make_tables.py` et `memoire/tables/` (les scripts sont à la racine de `scripts/` depuis le 2026-10-01)
- [ ] §4.1.5 Détails computationnels de M : introduire l'alignement de Kumagai–Oba (C_N)
- [ ] §4.1.6 Taille des super-cellules — `tab:échantillonnage`
- [ ] §4.1.6 Remplissage par zéros — `fig:Ved`
- [ ] §4.1.6 Convention intensive — `fig:M_scaling` (« < 2 % » devient 2.1 à 2.3 %)
- [ ] §4.1.6 Point de Dirac et littérature — `fig:M_map`, Kaasbjerg (« 3 à 4 fois inférieur » ne tient plus)
- [ ] §4.1.6 Local / non local — `tab:L_NL` (**inversion** : NL/L passe de 20 à 0.25)
- [ ] §4.1.6 Localisation Wannier — `fig:M_locality` (corps) ; `tab:rcut_M` → annexe, une phrase de renvoi
- [ ] §4.1.6 Autres vérifications — `fig:ks_reconstruction` (corps) ; `tab:tests_M` → annexe (+ porte A.2, convention intensive par famille) ; retirer la ligne « 16 → 20 bandes » et la phrase correspondante (l. 414)
- [ ] §4.3.4 Détails computationnels de T — « Évaluation pratique » (l. 629) : retirer « nous vérifions ce choix », justifier n_e = 8 par l'argument seul (g⁽⁰⁾ varie sur l'échelle de η, pas η/8) ; « Contrôles » (l. 633) : référence sur 5×5 seulement
- [ ] §4.3.5 Convergence — `fig:convergence`, `tab:convergence_gamma`, grille interne → annexe ; le corps garde les paramètres retenus et le critère « < 0.5 % » (R_cut 0 → 1 augmente maintenant Γ)
- [ ] §4.3.5 Taille de super-cellule — `fig:level2`, **reste dans le corps** (0.6 % devient 2.4 % ; médiane croissante en 3m)
- [ ] §4.3.5 Tests du schéma local — `tab:tests_T` → annexe, une phrase dans le corps ; retirer les lignes 6×6, 12×12 et grille d'énergie, et les phrases correspondantes (l. 690)
- [ ] §4.3.5 Born — `fig:spectral` (Born/T : 3.3 → 46 en médiane, 16 → 203 au max ; pic de −1.24 à −0.18 eV)
- [ ] §4.3.5 Signatures spectrales (quasi-annulation à −2.5 eV retirée ; ∫δρ = −1.00 ; critères par bloc π / σ)
- [ ] §4.3.5 Comparaison avec la littérature
- [ ] §4.4 Conclusion du chapitre
- [ ] **C** — Installer les 8 figures R10 dans `memoire/figures/` (depuis `figures/electron_defect/`, produites par `scripts/make_all_figures.py`), plus les nouvelles retenues
- [ ] **C** — `PROVENANCE.md` à jour à chaque section (§0 et §4 refaits le 2026-10-01 après la réduction du dépôt)

## 4 bis. Annexe D : paramètres et convergence

Annexe D réorganisée par chaîne (DFT, DFPT, Wannier, M, T, EPW) : pour chacune, tableau des paramètres puis preuves de convergence et tests. Le corps garde les valeurs retenues et un renvoi.

- [ ] **C** — Restructurer `annexes/paramètres.tex` par chaîne (titre à revoir : « Paramètres et convergence des calculs numériques » ?)
- [ ] **C** — Ch. 4 : y placer les éléments déplacés pendant la réécriture (§4 ci-dessus)
- [ ] **C** — Ch. 2 (verrouillé) : déplacer `fig:convergence_dft` et son paragraphe, une phrase de renvoi — **après le ch. 4**, en un seul bloc avec le ch. 5
- [ ] **C** — Ch. 5 (verrouillé) : déplacer `tab:gamma_ep_conv`, `tab:gamma_ph_conv` et leurs blocs « Convergence », une phrase de renvoi — même bloc
- [ ] **C** — Vérifier tous les `\ref` vers les éléments déplacés (grep sur `memoire/`), compiler, `PROVENANCE.md` à jour

## 5. Répercussions hors du ch. 4

- [ ] Ch. 5 §5.3.5 (l. 301–312) : Γ^ed/Γ^ep (médiane 0.361 → 0.554, max 2.0 → 34.8 à −0.18 eV, croisements) et `fig_epw_vs_ed` R10
- [ ] Intro l. 74 (« état quasi-lié sous la singularité de van Hove »)
- [ ] Conclusion générale l. 8–16 (non local dominant, van Hove, 0.6 %, Kaasbjerg)
- [ ] Résumé et abstract (non local dominant, facteur 3.3, van Hove)
- [ ] **C** — Apparier les 176 chiffres du ch. 5 à `donnees/epw/` (comme `defauts_nombres.md` pour le ch. 4)
- [ ] **C** — `tab:gamma_ph_conv` (eph:254, 18 valeurs) n'a aucun fichier de données : extraire un csv de `donnees/epw/NOTES_EPW.md` (table de convergence de γ(A₁′, K), l. 295 ; grilles 120² à 1200², σ = 0.01 / 0.02 / 0.05 eV, 10 K et 300 K) → `donnees/epw/phself_K_convergence.csv`, vérifier contre la table du `.tex`, mettre `MD5SUMS` et `PROVENANCE.md` à jour

## 6. Chantier 2b : §2.5 couplage électron-photon

- [ ] Rédiger le §2.5 (texte P28) avec `fig_em_coupling` et la table `em_table`
- [ ] Retirer « laissée hors du cadre » : intro l. 72, raman l. 297, et ailleurs (grep « électron-photon »)

## 7. Avant le dépôt

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

## 8. Anciens restes, statut à vérifier

Notés avant le 2026-09-25 ; peut-être déjà faits.

- [ ] Zotero : ajouter Yates 2007, Eckmann 2012, Polanco 2018, Chen 2009, Ugeda 2010, Guandalini 2025 (PRL), Perdew–Parr–Levy–Balduz 1982, Almbladh–von Barth 1985 ; doublon Ferrari 2006 / 2006a
- [ ] C7 : 75 points k pour 27×27 (IBZ 1/12), à confirmer par `grep 'number of k points'` sur Rorqual
- [ ] Normalisation de la DOS des phonons (intégrale matdyn 3.78 au lieu de 6)

---

## Fait

- [x] 2026-09-30 — Tag `memoire-avant-menage` (656c05c) sur graphene-raman
- [x] 2026-09-30 — Inventaire côté texte (`PROVENANCE.md`) ; skill `thesis-section-pass` mis à jour
- [x] 2026-10-01 — Ménage de graphene-raman, tag `memoire-apres-menage` (14e8c2a)
- [x] 2026-10-01 — Copie vers msc- (`bbed6f0`, `12da2f0`, `3e2e5ad`) ; recette passée (§0 de `PROVENANCE.md`, commit `ec61841`)
- [x] 2026-10-01 — Inventaire des chiffres du ch. 4 : trous et choix listés aux §2 et §3
- [x] 2026-10-01 — Réduction du dépôt à ce qui trace les figures (code de production laissé dans graphene-raman au tag) ; `scripts/make_all_figures.py` ; `requirements.txt` figé ; 47 figures identiques au bit à celles du tag
- [x] 2026-10-01 — `calculs/` rempli depuis Rorqual (entrées QE, Wannier90, EPW, listes de points)
- [x] 2026-10-01 — Audit « que manque-t-il ? » : 20 figures régénérables, sources des tables présentes ; ajoutés à `donnees/campagnes/` les chiffres de R8 (`*_results.json`) et de la série EM (`em_table.*`, `em_ring_stats.json`)
- [x] 2026-10-01, 10 h 20 — Recette refaite après réduction, VM Linux : 8 scripts ok, 47 PDF identiques à ceux de la recette du matin, 109 md5 de `donnees/` OK
