# TODO — mémoire de maîtrise

Liste de travail unique du dépôt.

Mise à jour : 2026-10-01, 15 h 20. Les items terminés sont retirés de la liste (l'historique est dans git).

---

## Chantier 1 : réécriture du ch. 4

Section par section : C propose, G tranche, C applique et compile. Tableaux : `scripts/make_tables.py` → `memoire/tables/<nom>.tex` (fait le 2026-10-01 ; valeur et source de chaque cellule dans `memoire/tables/SOURCES.md`) ; `\input{tables/<nom>}` et légende revue à la réécriture de chaque section.

Ordre : celui du chapitre (numéros et lignes de `défauts.tex` au 2026-10-01 ; les numéros de ce chantier étaient décalés d'un cran jusqu'au 2026-10-01). L'introduction, les §4.1.1–4.1.2 et les sous-sections de théorie de T (§4.2.1–4.2.3) n'ont pas d'item (§4.1 à 4.1.2 relus et retouchés par G le 2026-10-01).

### §4.1.3 Interpolation avec des fonctions de Wannier (`sec:interp_wannier_M`)

- [ ] **G** — §4.1.3 ou §4.1.4, images de Wigner-Seitz : la production prend les vecteurs **R** de la boîte pN×pN par images de Wigner-Seitz (`config/production.json` : `alignment.labels_offgrid = wigner_seitz` ; `ws_images`, `ws_phase` ; `donnees/ch4/NOTES_TGAMMA.md` l. 88), mais le texte (autour de `eqn:M_interp` et de la troncature) ne dit pas quel représentant de **R** est pris. Ce choix fixe l'abscisse de `fig:M_locality` (15.6 a, contre 22.5 a avec les étiquettes brutes) et les valeurs de `tab:rcut_M` (`r10_c2_results.json` : `plateau_ws`). Une phrase ; place à choisir : §4.1.3 avec la troncature, ou §4.1.4 avec l'alignement
- [ ] **C** — §4.1.3, renvois à repointer vers l'annexe D quand elle aura ses labels (chantier 3) : l. 192 (convergence de M en R_cut → `tab:rcut_M` ; convergence de Γ^ed en R_cut → `fig:convergence`, `tab:convergence_gamma`) et l. 194 (boucle fermée Bloch → Wannier → Bloch → `tab:tests_M`) ; la décroissance des M_ij(R′, R) (`fig:M_locality`, citée l. 194) reste au §4.1.5 ; lignes du 2026-10-01

### §4.1.4 Détails computationnels de M (`sec:M_détails`, l. 200–238)

- [ ] §4.1.4 Détails computationnels de M : introduire l'alignement de Kumagai–Oba (C_N) ; `fig_offset_profiles_13` et `alignement_regions` en annexe, une phrase de renvoi ; **retirer « sa moyenne spatiale est soustraite » (bloc « Partie locale », l. 222)** : la production n'a jamais soustrait la moyenne de ΔV (`subtract_mean=False`, `donnees/ch4/NOTES_TGAMMA.md` l. 88), elle aligne par Kumagai–Oba (confirmé par G le 2026-10-01) ; choisir le symbole de la constante d'alignement ($C_N$ ou $\Delta V_\text{PA}^{(N)}$ ; `SYM_CN` dans `make_tables.py`) ; décision du 2026-10-01 : **G** rédige le bloc « Alignement du potentiel » lui-même (C ne fait que suggérer), **sans chiffres** (méthode seulement : sites, sphère de 1 Å, région ≥ 0.75 r_max, écart-type = incertitude, soustraction sur M(R, R) des N² cellules, linéarité du remplissage) ; C_9 = −25.1 meV et l'écart-type de 9.1 meV vont au §4.1.5 avec `tab:échantillonnage` ; la comparaison des régions (Kumagai–Oba contre la nôtre) et le 0.06 meV de l'approximation (i) vont en annexe D ; à vérifier : ce que compare R9 A.2 (0.06 meV) ; Lu et al. 2019 confirmé par G (méthode « core-average » de leur réf. [39], potentiel local moyenné à l'atome le plus éloigné ; citer aussi [39] ?) ; clé bib de Kumagai–Oba présente (`kumagaiElectrostaticsbasedFinitesizeCorrections2014`) ; figure `tikz/chaine_M.tex` (`fig:chaine_M`) faite par C, à intégrer par G au début du §4.1.4

### §4.1.5 Résultats pour M (`sec:M_results`, l. 240–440)

- [ ] §4.1.5 Taille des super-cellules — `tab:échantillonnage` : V̄^L(a_CC) **aligné** (= brut − C_N) : +58.7, +68.4, +69.8 meV (6, 9, 12) ; −306.8, −373.2, −255.5, −288.4, −244.3 meV (5, 7, 8, 10, 11) ; ΔE_F inchangé ; ajouter une colonne C_N
- [ ] **G** — §4.1.5 Taille des super-cellules, convention du point K : `défauts.tex` l. 246 et `théorie.tex` l. 325 (verrouillé) écrivent $K=(1/3,1/3,0)$. Pour la maille de QE (a₁, a₂ à 60°, `calculs/ch2_electrons/bandes_dos/scf.in`), K vaut (2/3, 1/3) en coordonnées réduites ; (1/3, 1/3) tombe à |k| = 0.98 Å⁻¹ et n'est pas K (`config/production.json`, `K_note`). Vérifier si le mémoire donne a₁, a₂ quelque part ; choisir entre donner les vecteurs primitifs ou écrire K autrement, puis corriger les deux lignes ensemble (celle du ch. 2 dans le bloc ch. 2 / ch. 5 du chantier 3)
- [ ] §4.1.5 Remplissage par zéros — `fig:Ved` : cœur 115 à 116 eV au site ; |V̄| < 10⁻³ du cœur dès 1.4 à 1.8 Å ; fond loin de la lacune −0.10 eV (5×5) à −0.018 eV (12×12), égal à C_N à quelques meV près ; **le « coin positif de ~0.1 eV » de la 5×5 ne tient plus** (max −0.08 eV dans les 5 % les plus éloignés) ; l. 290 : « il subsiste même après la soustraction des moyennes spatiales » est faux (aucune moyenne n'est soustraite, voir §4.1.4) et l'explication du fond par l'écrantage incomplet du graphène est à revoir puisque le fond coïncide avec C_N (**G** tranche)
- [ ] §4.1.5 Convention intensive — `fig:M_scaling` : « < 2 % » devient 2.1 % (non-3m) et 2.3 % (3m) par famille, 7.7 % sur les six tailles ; « écart grossière / élargie pratiquement nul pour N ≥ 7 » devient ≤ 2.4 % (−2.4, 0.0, −2.2, −1.0 % pour 7, 8, 9, 12) ; légende et texte : max|M| et test intensif sur M **brut** (R10 D6), parce que l'alignement ajoute N²|C_N| aux éléments k = k′
- [ ] §4.1.5 Point de Dirac et littérature — `fig:M_map` **alignée** (**C** : `make_figures_defaut.py` → clés `map_*_aligned`) : M̃_π 114.9 eV Å² en K, 102 à 117 sur la zone ; M̃_π* 117.6 en K, 110 à 146 (max près de Γ, |k'| = 0.11 Å⁻¹) ; M^L_∥ 92.1 en K, 83 à 94 ; M^NL_∥ 19 à 23 ; l'alignement ne change que K et son voisinage (jusqu'à 7.7 eV Å², 125 des 729 points de plus de 0.5), à dire dans la légende (terme N²|C_N| à k′ = k, étalé par le facteur de forme de la boîte). Kaasbjerg (« 3 à 4 fois inférieur » ne tient plus) : `fig_kaasbjerg_plateau_ws` dans le corps, panneaux alignés (c, d) seulement, même grandeur que sa Fig. 3 ; près de K, 81.6 (π) et 82.8 (π*) eV Å² en moyenne (77 à 87), contre ~70 chez lui
- [ ] §4.1.5 Local / non local — `tab:L_NL` (**inversion** : NL/L passe de 20 à 0.25) : **brut et aligné côte à côte** (décision du 2026-10-01, = R10 D6) : fraction locale à K 0.77 à 0.79 (brut), 0.79 à 0.82 (aligné) ; 9×9 : M̄^L(K) = 11.31 (brut) et 13.34 eV (aligné), A_cell·M̄(K) = 75.9 et 86.6 eV Å² au lieu de 17.1. Une phrase : à k = k′, l'alignement ajoute exactement N²|C_N| (1.44, 1.82, 1.32, 0.92, 2.04, 2.69 eV pour 5, 6, 7, 8, 9, 12 ; corrigé le 2026-10-01 d'après `M_analysis.npz`, identité contrôlée par `make_tables.py` ; avant : 1.31, 0.93, 2.03), qui croît comme N² ; d'où la dérive en taille de la colonne alignée (3m : 13.17, 13.34, 13.91) alors que la brute est plate (10.5 à 11.4 eV) ; la matrice T ne voit pas ce terme (seules les mailles à R_cut ≤ 3 reçoivent −C_N) ; légende : pour N = 5, 7, 8, « K » est le point de grille le plus proche (0.055, 0.050, 0.043 Å⁻¹, `lnl_<S>_dK`)
- [ ] §4.1.5 Localisation Wannier — `fig:M_locality` (corps) ; `tab:rcut_M` → annexe, une phrase de renvoi. Grilles élargies : ~41 eV sur le site (35 en 12×12), ~2 eV à |R| = 1, ~0.1 eV à 3, ~0.01 eV à 5 (3.6 ordres de grandeur), plancher ~10⁻³ eV au-delà de 6 a (**pas 10⁻⁴**) ; grilles grossières : aucune décroissance (5×5 : 4.1 → 2.9 eV) ; `fig_rcut_aligned` en annexe avec `tab:rcut_M`. `tab:rcut_M` (généré) porte les valeurs **alignées** (`m_rcut_convergence.csv` = R10 « plateau ») : le dire dans la légende ; option (**G** tranche) : colonnes brutes à côté (`r10_c2_results.json`, `rcut.<S>.tel_quel`), puisque `fig_rcut_aligned` montre que l'alignement accélère la convergence en R_cut
- [ ] §4.1.5 Autres vérifications — `fig:ks_reconstruction` (corps) ; `tab:tests_M` → annexe (+ porte A.2, convention intensive par famille) ; retirer la ligne « 16 → 20 bandes » et la phrase correspondante (l. 414) ; texte l. 412 à aligner sur le tableau généré (2–32 µeV → 1.5–32 µeV, 0.2 à 10 meV → 0.21 à 10 meV) ; hermiticité donnée en maximum sur les six tailles, alors que la légende dit « 9×9 sauf mention »

### §4.2.4 Détails computationnels de T (`sec:T_détails`, l. 611–633)

- [ ] §4.2.4 Détails computationnels de T — « Évaluation pratique » (l. 629) : retirer « nous vérifions ce choix », justifier n_e = 8 par l'argument seul (g⁽⁰⁾ varie sur l'échelle de η, pas η/8) ; « Contrôles » (l. 633) : référence sur 5×5 seulement

### §4.2.5 Résultats pour T (`sec:T_results`, l. 635–742)

- [ ] §4.2.5 Convergence (**G** reformule) — `fig:convergence`, `tab:convergence_gamma` (colonne R_cut = 4 remplie pour les six tailles), grille interne (`tab:grille_interne`, généré : voir chantier 3) et `fig_resonance_vs_nkint_plateau` → annexe ; le corps garde les paramètres retenus (R_cut = 3, 240², η = 20 meV, 300²). Le texte rapporte les variations mesurées et les compare à l'incertitude de taille de `fig:level2` (2.4 %), qui domine (voir l'item suivant). R_cut (médiane de Γ N_cells, 240², η = 20 meV) : 0 → 1 **augmente** Γ, +7.7 à +9.4 % (3m) et +0.6 à +1.8 % (non-3m) ; 1 → 2 au plus 1.7 % ; 2 → 3 jusqu'à 1.2 % (et non < 0.4 %) ; 3 → 4 : 0.34 % pour 9×9, au plus 0.57 % (8×8, 12×12) au lieu de « 0.2 %, référence seulement » ; convergence non monotone en 3m (changement de signe entre 2 → 3 et 3 → 4) ; « gain marginal de 0.2 % » à corriger. Grille interne 300² → 600² : −0.09 % sur la fenêtre, +0.2 % sur la zone ±0.3 eV (v1 : 2.4 %), +4.8 % au point de Dirac (v1 : 5 %), décroissance monotone en N_k^int
- [ ] §4.2.5 Convergence — **supprimer le critère « mieux que 0.5 % »** (décision du 2026-10-01) : dernière phrase de la l. 675 (« Chacun des paramètres retenus pour la production est au-delà du point où le taux d'amortissement cesse de varier à mieux que 0.5 % ») ; il n'apparaît nulle part ailleurs dans le mémoire (le seuil de 0.1 meV par atome du ch. 2 est indépendant)
- [ ] §4.2.5 Taille de super-cellule — `fig:level2`, **reste dans le corps** (0.6 % devient 2.4 % ; médiane croissante en 3m) ; légende (l. 681) : « carrés = famille 3m, ronds = l'autre » ne correspond plus à la figure R10 (`make_figures_defaut.py` trace tout en ronds, couleur par taille) : changer la légende ou la figure
- [ ] §4.2.5 Super-cellule et défaut isolé (paragraphe neuf, place à choisir : Taille de super-cellule ou Signatures spectrales) — `fig_folded_vs_R7` dans le corps : (a) le modèle replié suit QE pour l'état π quasi-lié de 6×6 à 27×27 ; (b) le maximum de LDOS des voisins tend vers la résonance de T (−0.18 eV) quand N → ∞. Légende : la courbe alignée vient de R9 avec C = −24.65 meV (site unique) au lieu de −25.14 meV (0.5 meV d'écart)
- [ ] §4.2.5 Tests du schéma local — `tab:tests_T` → annexe, une phrase dans le corps ; retirer les lignes 6×6, 12×12 et grille d'énergie, et les phrases correspondantes (l. 690) ; ligne « Hermiticité de M_loc » retirée du tableau (décision du 2026-10-01 : déjà dans `tab:tests_M`) ; **G** : ajouter « g0 par lots » (1.2e-14) ? garder la ligne « Grille interne » maintenant que `tab:grille_interne` existe ? ; la positivité donne le minimum réel (Γ N_cells ≥ 1.96 eV sur la fenêtre)
- [ ] §4.2.5 Born — `fig:spectral` (Born/T : 3.3 → 46 en médiane, 16 → 203 au max ; pic de −1.24 à −0.18 eV)
- [ ] §4.2.5 Signatures spectrales (quasi-annulation à −2.5 eV retirée ; ∫δρ = −1.00 ; critères par bloc π / σ). À décider en rédigeant : si le texte cite plusieurs positions de la résonance (−0.15 à −0.18 eV), un petit tableau des estimateurs (pic de Γ_T, −Im T̄(K), max de LDOS des voisins, max de ρ − ρ₀ ; 9×9 et 12×12, brut et aligné) ; données prêtes : `table_2bis` de `r8_fig_results.json`
- [ ] §4.2.5 Comparaison avec la littérature — figures Kaasbjerg (script refait par C le 2026-10-01 selon le docstring de G) : corps `superposition` (spin compté, 2 panneaux), `spectral_GKM` (Kumagai–Oba, 2 panneaux), `sigma_K` (non aligné et Kumagai–Oba) ; annexe `sensibilites` ; `dos_c` (ρ − ρ₀, 2 panneaux, marquée M) : **place à décider** (corps, annexe ou rien). Chiffres dans le nouveau `tab:kaasbjerg` (item suivant). Texte : **accord qualitatif seulement** (R8 7b, « écarts rapportés, non investigués ») ; pic de ρ − ρ₀ décalé de +45 (non aligné) à +60 meV (Kumagai–Oba) vers E_D, plus étroit et plus haut (même poids à 15 % près) ; l'alignement **éloigne** de Kaasbjerg ; hauteur ×9.4 pour c ×10 ; la hauteur à 0.1 % n'est pas comparable (celle de Kaasbjerg vaut l'épaisseur d'un trait). La phrase « facteur 3–4 entre nos éléments de matrice » (l. 742) tombe : ramener Ṽ à 70 eV Å² déplacerait le pic de 10 à 15 meV seulement (R8 étape 6 et ρ − ρ₀, extrapolation linéaire) ; ni le protocole d'élargissement (η unique : pic déplacé d'au plus 2.5 meV, hauteur −20 %) ni les paramètres (`sensibilites`) n'expliquent le reste ; restent les ingrédients DFT (code, pseudopotentiel, taille 11×11), sa grille non uniforme et la lecture de sa figure (pas de 10 meV)
- [ ] **C** — §4.2.5 Comparaison avec la littérature, `tab:kaasbjerg` (corps) : tableau généré le 2026-10-01 (`tables/kaasbjerg.tex`) ; à insérer avec la comparaison (`\input`, légende ; les positions de ρ − ρ₀ sont données à quatre décimales, pas d'énergie 2.5 meV ; π / π* et K + δx̂ à dire dans la légende) ; colonnes Kaasbjerg / non aligné / Kumagai–Oba ; lignes : Ṽ = A_cell|M_k′K| près de K (~70 ; 77.0 / 78.2 ; 81.6 / 82.8 eV Å², π / π*, `r10_c2_results.json`) ; position du max de ρ − ρ₀ à 0.1 % / 1 % (−0.200 / −0.210 ; −0.1625 / −0.165 ; −0.1475 / −0.150 eV, grille 600², `r8_dos_results.json`, `r8_7a_results.json`) ; hauteur à 1 %, spin compté (0.0307 ; 0.0535 ; 0.0582) ; largeur à mi-hauteur à 1 % (0.306 ; 0.201 ; 0.187 eV) ; écart des deux maxima de A_K à 1 % (0.100 ; 0.1176 ; 0.1182 eV, `r8_spec_results.json`). Méthode de Kaasbjerg (GPAW, PAW, LDA, 11×11) en note ; paramètres de la comparaison (c_i, η_G = 15 / 25 / 50 meV selon la figure, ρ₀ sur 1 200², N_k^int 900) dans la légende ou `tab:param_T`
- [ ] §4.2.5 Deux DOS à c = 1 % dans le corps, à distinguer dans le texte et les légendes : `fig:spectral` (b) trace ρ₀ + c δρ (premier ordre en c ; T de production, grille 240², η = 20 meV) ; `fig_kaasbjerg_superposition` (b) trace la DOS moyennée sur le désordre, G_k = [(ε + iη_G) − H(k) − c T̄_k]⁻¹ (éq. 22 de Kaasbjerg ; η_G = 50 meV, ρ₀ à 1 200² et 15 meV). Leurs pics ne tombent pas forcément au même endroit (ρ − ρ₀ de R8 : −0.150 eV ; `fig:spectral` : à relever)

### §4.3 Conclusion du chapitre (l. 744–749)

- [ ] §4.3 Conclusion du chapitre

### Transversal : figures, scripts, données

- [ ] **C** — Installer les 8 figures R10 dans `memoire/figures/` (depuis `figures/electron_defect/`, produites par `scripts/make_all_figures.py`), plus les nouvelles retenues : corps `fig_kaasbjerg_{plateau_ws,superposition,spectral_GKM,sigma_K}`, `fig_folded_vs_R7` ; annexe `fig_offset_profiles_13`, `alignement_regions` (à porter, item suivant), `fig_rcut_aligned`, `fig_resonance_vs_nkint_plateau`, `fig_kaasbjerg_sensibilites`
- [ ] **G/C** — Retouches restantes dans `make_figures_controles.py` : `plateau_ws` réduite aux panneaux alignés (c, d) ; `folded_vs_R7` : étiquettes « non aligné » / « aligné » (au lieu de « site unique »), C dans la légende. (`make_figures_kaasbjerg.py` : fait par C le 2026-10-01.) Puis, sur le Mac, `python scripts/make_all_figures.py` pour écrire les PDF et PNG
- [ ] **G** — Données que plus aucun script ne lit depuis le tri du 2026-10-01 : `alignement/r10_a2_results.json` (`fig_levels_vs_invN`), `controles/r9_b_results.json` (`fig_resonance_vs_nkint`, la version plateau reste lue), `controles/r7_d1_results.json` (`fig_size_3m`, `fig_localized_3m`) : garder si un chiffre du texte en vient (niveaux QE, état π quasi-lié par taille), sinon retirer avec leurs lignes de `MD5SUMS`
- [ ] **G** — Instructions du projet : « huit make_figures*.py » → sept (`make_figures.py` retiré, `make_figures_memoire.py` renommé `make_figures_defaut.py`), « 47 figures » → 33 ; préciser que les figures se régénèrent par `make_all_figures.py` (seul lanceur qui passe les options de production à `make_figures_epw.py`)
- [ ] **C** — `PROVENANCE.md` à jour à chaque section (§0 et §4 refaits le 2026-10-01 après la réduction du dépôt)

## Chantier 2 : §2.5 couplage électron-photon. À faire avant l'annexe D car elle recoit les paramètres de 2.5.

- [ ] Rédiger le §2.5 (texte P28) avec `fig_em_coupling` et la table `em_table`
- [ ] Retirer « laissée hors du cadre » : intro l. 72, raman l. 297, et ailleurs (grep « électron-photon »)

## Chantier 3 : Annexe D, paramètres et convergence

Décision du 2026-10-01 : en annexe ce qui justifie seulement un paramètre numérique, dans le corps ce qui porte un résultat ou une limite. Restent dans le corps : `fig:level2`, `fig:M_locality`, `fig:ks_reconstruction`, `fig:epw_kohn_degauss`, `tab:gamma_ph_prod`. Vont en annexe : `fig:convergence_dft`, `fig:convergence`, `tab:convergence_gamma`, grille interne, `tab:rcut_M`, `tab:tests_M`, `tab:tests_T`, `tab:gamma_ep_conv`, `tab:gamma_ph_conv`, et (choix du 2026-10-01) `fig_offset_profiles_13`, `alignement_regions`, `fig_rcut_aligned`, `fig_resonance_vs_nkint_plateau`, `fig_kaasbjerg_sensibilites`.

Annexe D réorganisée par chaîne (DFT, DFPT, Wannier, M, T, EPW) : pour chacune, tableau des paramètres puis preuves de convergence et tests. Le corps garde les valeurs retenues et un renvoi.

- [ ] **C** — Restructurer `annexes/paramètres.tex` par chaîne (titre à revoir : « Paramètres et convergence des calculs numériques » ?)
- [ ] **C** — Ch. 4 : y placer les éléments déplacés pendant la réécriture (chantier 1 ci-dessus)
- [ ] **C** — Tableau de la grille interne `tab:grille_interne` (chaîne T, preuve de convergence) : généré le 2026-10-01 (`tables/grille_interne.tex`, depuis `M2_plateau/nkint_check_9x9.csv`) ; à placer dans l'annexe D à sa restructuration (`\input`, légende) ; E_res avait été retiré du ch. 4 par la décision R10 B.1 (argmax discret sur les états de la grille de sortie), **G** confirme qu'il revient ici ; contenu : 150², 300², 450², 600² × médiane de Γ N_cells sur la fenêtre et sur la zone ±0.3 eV, Γ au point de Dirac, E_res (−0.238 eV à 150², puis −0.175 eV dès 300²) ; remplace la prose de la l. 675
- [ ] **C** — `tab:param_M` : lignes de l'alignement (Kumagai–Oba, région d ≥ 0.75 r_max, sphères de 1.0 Å, approximation (i), C_N pour 13 tailles, valeurs dans `config/production.json`) et nombre de bandes (ligne vide) ; `tab:param_T` : paramètres de la comparaison avec Kaasbjerg si `tab:kaasbjerg` ne les porte pas
- [ ] **C** — Ch. 2 (verrouillé) : déplacer `fig:convergence_dft` et son paragraphe, une phrase de renvoi — **après le ch. 4**, en un seul bloc avec le ch. 5
- [ ] **C** — Ch. 5 (verrouillé) : déplacer `tab:gamma_ep_conv`, `tab:gamma_ph_conv` et leurs blocs « Convergence », une phrase de renvoi — même bloc
- [ ] **C** — Vérifier tous les `\ref` vers les éléments déplacés (grep sur `memoire/`), compiler, `PROVENANCE.md` à jour


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

- [ ] **C** — `calculs/` (289 fichiers, commités dans `9970ab5`) : croiser avec l'annexe D (lignes vides et points périmés relevés le 2026-10-01 : vide de 30 Bohr et troncature 2D dans `tab:param_dft` ; nombre de bandes 16 / 20 et seuil 10⁻¹⁴ Ry des cellules unitaires dans `tab:param_M` (alignement : chantier 3) ; fenêtre gelée −4,5 eV des grilles grossières dans `tab:param_wannier`)
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

