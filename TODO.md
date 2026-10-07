# TODO — mémoire de maîtrise

Liste de travail unique du dépôt.

---

## Chantier 1 : réécriture du ch. 4

- [ ] **C** — Campagne $\bm\Lambda$ (défini en T.1 `eqn:T_inv`, $\bm\Lambda=\mathbb I-\bm{\mathcal G}^{(0)}\bm M$) : T.3 l. ~200 ($\bm\Lambda_\mathcal{C}=\mathbb I-\bm{\mathcal G}^{(0)}_\mathcal{C}\bm M_\mathcal{C}$, ordre et indice $\mathcal{C}$ à corriger), T.4 Diagnostics (+ phrase « à η fini » : état lié = minimum profond + pic 2η portant un état entier ; résonance = minimum modéré + bosse > 2η), légende (d) de `fig:spectral`, boîte Born/critère de `chaine_T.tex`, entrée dans `symboles.tex`.
- [ ] **C** — Passe en gras sur tout `défauts2.tex` (dont `eqn:born` en T.2 : $\bm\Sigma^{\text{ed},\text{B}}=c[\bm M+\bm M\bm{\mathcal G}^{(0)}\bm M]$, et Contrôles : $\bm M_\mathcal{C}$, $\Gamma^\text{ed}_{n\kv}$) ; restes $N_\text{uc}$ (l. 77 $\rho=\rho_0+\delta\rho/N_\text{uc}$, l. 114, légende `fig:dyson_T` « temps intégrés »).


### Transversal : figures, scripts, données


- [ ] **G** — Données que plus aucun script ne lit depuis le tri du 2026-10-01 : `alignement/r10_a2_results.json` (`fig_levels_vs_invN`), `controles/r9_b_results.json` (`fig_resonance_vs_nkint`, la version plateau reste lue), `controles/r7_d1_results.json` (`fig_size_3m`, `fig_localized_3m`) : garder si un chiffre du texte en vient (niveaux QE, état π quasi-lié par taille), sinon retirer avec leurs lignes de `MD5SUMS`
- [ ] **G** — Instructions du projet : « huit make_figures*.py » → sept (`make_figures.py` retiré, `make_figures_memoire.py` renommé `make_figures_defaut.py`), « 47 figures » → 33 ; préciser que les figures se régénèrent par `make_all_figures.py` (seul lanceur qui passe les options de production à `make_figures_epw.py`)


## Chantier 3 : Annexe D, paramètres et convergence

Décision du 2026-10-01 : en annexe ce qui justifie seulement un paramètre numérique, dans le corps ce qui porte un résultat ou une limite. Restent dans le corps : `fig:level2`, `fig:M_locality`, `fig:epw_kohn_degauss`, `tab:gamma_ph_prod` (`fig:ks_reconstruction` passée en annexe le 2026-10-04, décision G). Vont en annexe : `fig:convergence_dft`, `fig:convergence`, `tab:convergence_gamma`, grille interne, `tab:rcut_M`, `tab:tests_M`, `tab:tests_T`, `tab:gamma_ep_conv`, `tab:gamma_ph_conv`, et (choix du 2026-10-01) `fig_offset_profiles_13`, `alignement_regions`, `fig_rcut_aligned`, `fig_resonance_vs_nkint_plateau`, `fig_kaasbjerg_sensibilites`.

Annexe D réorganisée par chaîne (DFT, DFPT, Wannier, M, T, EPW) : pour chacune, tableau des paramètres puis preuves de convergence et tests. Le corps garde les valeurs retenues et un renvoi.

- [ ] **C** — Vérifier tous les `\ref` vers les éléments déplacés (script du 2026-10-05 : 167 cibles, 0 manquante sur `memoire/`), compiler, `PROVENANCE.md` à jour — à refaire après le bloc ch. 2 / ch. 5.


## Chantier 5 (une fois tout le reste terminé) : corrections de la grammaire et orthographes. relecture complète.

## Avant le dépôt

- [ ] **C** — `calculs/` (289 fichiers, commités dans `9970ab5`) : croiser avec l'annexe D (lignes vides et points périmés relevés le 2026-10-01 : vide de 30 Bohr et troncature 2D dans `tab:param_dft` ; nombre de bandes et seuil 10⁻¹⁴ Ry des cellules unitaires dans `tab:param_M` : **faits le 2026-10-05** ; fenêtre gelée −4,5 eV des grilles grossières dans `tab:param_wannier`)
- [ ] **G/R** — Rorqual : `git pull --ff-only` de graphene-raman, `pip uninstall` + `pip install -e .`, pytest, une recette avec données, ligne dans `CLEANUP.md`
- [ ] **G** — Annexe déclaration IA (`annexes/ia.tex`, à confirmer avec Michel) ; décommenter son `\include`
- [ ] **G** — README principal (structure, « Reproduire les figures », « Données lourdes », lien vers graphene-raman) : au verrouillage du dépôt
- [ ] **G/C** — Au verrouillage : enregistrer les sommes md5 des figures finales (`figures/MD5SUMS`) et refaire une fois la recette
- [ ] **G** — Fichier `LICENSE` à la racine (absent ; nécessaire avant l'archive publique)
- [ ] **G** — Archive : release GitHub de msc- → Zenodo (DOI)
- [ ] **C** — Décommenter tous les `\include` de `master_thesis.tex`, build complet, passe finale de mise en page (débordements > 10 pt : `tikz/pp`, `tikz/pd`, amplitudes de l'annexe B)
- [ ] **C** — Grep des coquilles récurrentes (Midgal, abritraires, méchanisme, absorbtion, inversions ed/ep)
- [ ] **G** — Ménage : supprimer `~/LaTeX/msc-graphene-raman-defects` (ancien clone, vérifier d'abord `git status` et `git log origin/main..`) et `~/projects/raman-graphene` (s'il est vide) ; supprimer `.git/index.lock.orphelin-claude-2026-10-01` et `-2026-10-03` (fichiers vides laissés par Claude : `git status` crée le verrou et la VM ne peut pas le supprimer ; C utilise `GIT_OPTIONAL_LOCKS=0` depuis le 2026-10-03)



## Après le dépôt (perspective) : campagne sur l'alignement et le fond du potentiel

Décision du 2026-10-03 : le mémoire garde les chiffres actuels et dit ce qui est compris et ce qui ne l'est pas ; les tests ci-dessous sont reportés au doctorat. Contexte : item G du §4.1.4.

- [ ] Indices du 2026-10-03 (à exploiter) : le décalage du vide reste petit (−3 à −7 meV pour N ≥ 9 hors 18, 24, 27 ; −2.6 ± 1.4 meV à 21×21) alors que C_N − vide vaut encore −11.7 meV à 21×21 (attendu ~ b/N² ≈ −2.5) : le résidu est dans le plan, pas dans la référence globale. Hypothèse (2026-10-03) : au seul point Γ, la famille 3m place exactement en E_D huit états par super-cellule (K, K′, π et π*, spin), soit 8/N² par maille (0.10 à 9×9, 0.011 à 27×27), contre ~2×10⁻³ état par maille pour le vrai cône dans la fenêtre d'étalement (±0.136 eV, ħv_F ≈ 5.6 à 6.6 eV Å) : surestimation d'un facteur ~50 (9×9) à ~5 (27×27). La famille non-3m n'en a aucun (faux gap, réponse locale). À taille comparable, l'écart plan − vide est ~3 fois plus faible pour N ≠ 3m (−6.1, −6.6 meV à 10, 11 contre −18.1, −15.0 à 9, 12), sans rien dire de l'asymptote (série arrêtée à 11, ajustement mauvais). Le test suivant tranche.
- [ ] Échantillonnage en k (candidat principal) : refaire les SCF pur et avec lacune de la 9×9 avec une grille de k centrée en Γ sur la super-cellule (3×3, 4×4 ; K reste inclus pour N = 3m), puis mesurer C_9, le fond dans le plan (panneau (c) de `fig:Ved`) et le décalage du vide. Motif : la fenêtre d'étalement (0.136 eV, ~0.02 Å⁻¹ autour de K) est plus petite que l'espacement de la grille (~0.11 Å⁻¹ même à 27×27), donc la réponse de basse énergie n'est échantillonnée que par K à toutes les tailles.
- [ ] Élargissement (avec le test d'échantillonnage en k, pas seul) : au seul point Γ, l'élargissement MV de 0.01 Ry (0.136 eV) est bien inférieur à l'écart entre K et ses voisins sur la grille (ħv_F·|b|/N ≈ 2 eV à 9×9, ≈ 0.7 eV à 27×27) : seuls les états de K sont dans la fenêtre et leur occupation est fixée par la dégénérescence et le nombre d'électrons, pas par σ. Diagnostic peu coûteux : C_9 au point Γ pour σ = 0.005, 0.01, 0.02, 0.03 Ry (attendu : presque insensible). Puis convergence conjointe (grille de k, σ) sur la 9×9 avec 3×3 et 4×4, MV et Fermi-Dirac (MV peut donner des occupations négatives quand peu d'états dégénérés sont au niveau de Fermi).
- [ ] Vide mesuré sur le potentiel électrostatique seul (pp.x `plot_num = 11`, V_bare + V_H) plutôt que sur V_KS (`plot_num = 1`, qui contient V_xc, numériquement bruité là où la densité est infime) ; pp.x seulement si les `.save` existent encore. Les entrées SCF et pp.x des tailles anormales sont identiques à celles de 21×21 à la maille près (vérifié le 2026-10-03), donc la cause n'est pas dans les entrées.
- [ ] Rôle de `assume_isolated='2D'` : refaire la paire 9×9 (pur, avec lacune) sans troncature, puis avec un vide plus grand (c = 40 bohr au lieu de 30), et comparer C_9, le fond dans le plan et le vide. Montage actuel conforme (feuillet à z = 0, c = 30 bohr = 15.87 Å). Attente : C_9 inchangé à 1/N² près, puisque les effets de la troncature passent par des moyennes sur la cellule.
- [ ] Vide anormal à 18×18, 24×24, 27×27 (−30, −167, −253 meV pour |z| > 5 Å, `table_v1_final.md` k) : vérifier les sorties SCF (« convergence has been achieved », précision estimée), la grille FFT et le profil en z ; seule voie pour comparer plan et vide aux grandes tailles.
- [ ] Mesure : dépendance de C_N au rayon des sphères (0.79 Å de Kumagai–Oba, 1.0 Å, 1.2 Å) et moyenne de ΔV brut pondérée par la densité π loin de la lacune.
- [ ] Charge de la lacune : charge portée par l'état quasi localisé au point de Dirac et compensation délocalisée (terme de type Madelung en 1/N ?) ; calcul polarisé en spin.
- [ ] Ajustements de C_N avec plus de tailles 3m (30, 33) pour discriminer a + b/N² de formes qui s'annulent à l'infini.
- [ ] Variante d'alignement sur le vide (au lieu de Kumagai–Oba) dans toute la chaîne, et comparaison avec Kaasbjerg à convention égale.
- [ ] Test de la diagonale M_nn(k,k) brute et alignée contre N sur toute la zone (famille 3m).
- [ ] Troncature brut / aligné (`tab:rcut_M`, constat C du 2026-10-04) : à R_cut = 3 le brut tronque trois à quatre fois moins bien que l'aligné (9×9 : 8.8 / 7.2 % contre 2.6 / 1.7 % ; 12×12 : 12 / 10 % contre 3.3 / 3.1 %) ; ce n'est pas un effet d'étiquettes (`r10_c2_results.json` : « plateau » = « plateau_ws » à 0.1 point) ; l'écart vaut (N² − 29)|ΔV_PA|/max|M| = 5.1 % (9×9), 8.2 % (12×12). Pour que le brut tronque moins bien, la somme des blocs diagonaux brut M_W(R,R) hors des 29 mailles doit valoir ≈ −2 eV (9×9), −3 eV (12×12), alors que M̄^L(K) brut est plat en N (`tab:L_NL`) : compatible seulement si ce reste vit dans les canaux σ ou si le maximum d'erreur n'est pas en k′ = k. À mesurer sur les matrices (Rorqual) : Σ_{R hors R_cut} M_W(R,R) brut, projeté π et total, pour 9×9 et 12×12.
- [ ] Validation de la méthode sur un semi-conducteur : MoS₂ avec lacune de soufre, comparaison directe avec Kaasbjerg (2020) (états liés dans le gap, taux de diffusion, même article). Sépare « la méthode marche-t-elle » (cas gappé, sans point de Dirac) de « ce que le graphène ajoute » (états en E_D, mode zéro, écrantage de semi-métal) ; renforce la publication du paquet.
- [ ] **Convergence de Γ^ed/c en taille de super-cellule (constat du 2026-10-05)**. Diagnostic : la décroissance monotone de v1 (2524 → 2459 meV de 5×5 à 12×12, 0.56 % sur la famille 3m) était un artefact — M^L en norme super-cellule, trop petit d'un facteur N_cells (R5-A.2), donc M ≈ M^NL (3.10 eV à K, rigoureusement indépendant de N) plus un résidu local en 1/N² ; v2 porte toute la physique de taille finie de ΔV (familles N mod 3, C_N, queue du potentiel coupée) : brut 3m 3156/3133/3163 meV (1 %, sans tendance), aligné 3149/3189/3265 (+3.6 %, monotone, dérive de C_N avec N ; sensibilité mesurée ±9 meV → ±1.5 % sur la médiane, amplifiée par la résonance à −0.18 eV). Trois voies, de la moins chère à la plus structurelle : (1) extrapolation Richardson séparée de C_N et des éléments de M_C sur 6/9/12 (famille 3m) puis Γ avec la M_C extrapolée — donne l'ampleur et le lieu (sur site vs queue) de ce qui manque ; (2) 15×15 et 18×18 (famille 3m) pour trancher entre saturation et dérive en 1/N du modèle replié (niveau quasi-lié jusqu'à N ≈ 55) ; (3) sortir de la super-cellule : potentiel du défaut isolé par équation de Dyson autocohérente sur l'amas plongé dans le cristal infini (DFT en fonction de Green, voie Lu–Bernardi / paquet PW + Wannier + matrice T ; ingrédients déjà là : 𝒢⁽⁰⁾_𝒞, amas, matrice T ; manque la boucle autocohérente densité → V_Hxc sur l'amas et la condition aux limites du cristal parfait) — élimine C_N, les familles et la queue d'un coup. Physique : lacune neutre mal écrantée dans un semi-métal (ρ(E_D) = 0), queue longue et oscillations de Friedel lentes ; M^NL exact à toute taille, tout le problème est dans ΔV.

Décision du 2026-10-03 : le mémoire garde les super-cellules au seul point Γ et ses chiffres actuels. Mise à jour du même jour : les tests sont lancés sur Rorqual **en parallèle de l'écriture** (plan à faire avec Fable). Règle proposée : un résultat obtenu avant le dépôt n'entre dans le mémoire qu'en conclusion ou en perspective, sauf s'il invalide un chiffre publié. Ordre suggéré (du moins cher au plus cher) : diagnostic σ au point Γ ; vide sur le potentiel électrostatique (pp.x seul, vérifier d'abord que les `.save` existent encore sur le scratch) ; rayon des sphères et moyenne pondérée π (post-traitement) ; 9×9 en 3×3 et 4×4 (σ, MV et FD) ; 9×9 sans troncature et c = 40 bohr ; tailles 30 et 33 ; MoS₂.

## Anciens restes, statut à vérifier

Notés avant le 2026-09-25 ; peut-être déjà faits (**ambigu**, non vérifiés par C le 2026-10-03).

- [ ] Zotero : ajouter Yates 2007, Eckmann 2012, Polanco 2018, Chen 2009, Ugeda 2010, Guandalini 2025 (PRL), Perdew–Parr–Levy–Balduz 1982, Almbladh–von Barth 1985 ; doublon Ferrari 2006 / 2006a
- [ ] C7 : 75 points k pour 27×27 (IBZ 1/12), à confirmer par `grep 'number of k points'` sur Rorqual
- [ ] Normalisation de la DOS des phonons (intégrale matdyn 3.78 au lieu de 6)

