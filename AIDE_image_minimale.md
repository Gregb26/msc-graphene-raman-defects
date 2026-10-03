# Aide-mémoire : image minimale, recentrage, troncature (§4.1.4)

Notes de travail (C, 2026-10-02), d'après le code de production (`local_tmatrix.recenter_mwr`, `defect_mwr`,
`wannier_interpolation.ws_images` / `ws_phase`). Pas une source de chiffres : ceux-ci restent dans `donnees/`.

## 1. L'idée commune

Objet physiquement **localisé** (potentiel de la lacune, puis M) représenté dans un espace **périodique**
→ une distance « au défaut » n'a de sens qu'avec l'image du défaut la plus proche.

## 2. Deux usages, deux périodes

| | Alignement | Étiquettes R de Wannier |
|---|---|---|
| Objets | atomes du calcul DFT | vecteurs R de la double TF |
| Période | super-cellule N×N | boîte élargie pN×pN |
| Règle | r_α, r_max, donc la région « loin » | la phase e^{ik·R} hors de la grille |
| Sans elle | atome au bord jugé loin alors qu'il touche l'image voisine de la lacune | R et R + pN s donnent des phases différentes hors grille → interpolation arbitraire |

## 3. Pourquoi des images minimales dans l'interpolation (trois rôles distincts)

- **Cause : la périodicité de la TF discrète.** Sur la grille pN×pN, R n'est défini que modulo pN.
  Toujours vrai, recentrage ou pas (Lu 2020 l'a aussi, défaut à l'origine).
- **Centre : le recentrage.** « Le plus proche » = le plus proche de la lacune ; le recentrage la met à l'origine.
  Il ne brouille rien, il fixe le point de référence.
- **Géométrie : le réseau hexagonal.** Replier dans [−pN/2, pN/2) donne un parallélogramme (a₁, a₂ à 60°),
  dont les coins sur la grande diagonale sont trop loin. Il faut la vraie cellule de Wigner-Seitz.
  9×9 dense (D = 27) : abscisse max 22.5 a (parallélogramme, 13√3) contre 15.6 a (Wigner-Seitz, 27/√3).
  Exemple D = 20 : l'étiquette (9, 9) est à 15.6 a ; ses images (−11, 9) et (9, −11) sont à 10.1 a, à égalité → poids 1/2 chacune.
- **Égalités** : images équidistantes gardées toutes, poids 1/n (comme `ndegen` de Wannier90 pour H(R)).
- Sur la grille elle-même : aucun effet (e^{ik·pN s} = 1). Hors grille : effet réel (ex. K pour la famille non-3m).

## 4. Recentrage

- `recenter_mwr` : R_d = maille du bloc sur site ‖M(R, R)‖ **maximal** (lu dans les données, pas dans la géométrie) ;
  étiquettes R → (R − R_d) **modulo pN**, repliées dans [−pN/2, pN/2). Seules les étiquettes bougent, pas les données.
- **Équivalent** à tronquer avec |R − R_d| ≤ R_cut, à condition de prendre R − R_d modulo pN
  (une maille juste de l'autre côté du bord est physiquement voisine). Ici le modulo ne sert jamais
  (lacune vers (N/2, N/2), pN/2 ≥ N), mais la formule générale en a besoin.
- **Pas obligatoire, mais souhaitable** (en clair : **tenue de livres** ; aucune observable ne dépend de R_d ; dans le texte, une phrase suffit) :
  1. (convention d'écriture seulement) §4.2 écrit Σ = c T₀ avec T₀ pour un défaut à l'origine ; mais T(k, k) est invariant
     par translation du défaut (g⁽⁰⁾ local ne dépend que de R − R′, et la phase e^{ik·R_d} des φ_nk s'annule dans φ†tφ),
     donc Γ serait identique avec l'amas centré en R_d : ce n'est PAS une exigence ;
  2. un défaut en R_d multiplie M(k′, k) et T(k′, k) par e^{i(k−k′)·R_d} (simple translation) : Γ (diagonal) n'y voit rien,
     ni |M(k′, k)| (cartes, Kaasbjerg), ni les amplitudes Raman (phase e^{−iq·R_d} commune à tous les termes à q fixé) : seule la phase
     complexe des éléments hors diagonale bouge (cosmétique, R_d change avec N et p) ;
  3. (commodité) distances = |R| au lieu de |R − R_d| mod pN ; `ws_images` accepte R_center = R_d pour les étiquettes brutes,
     donc faisable sans recentrage ; le garde-fou `mwr_locality` (‖M(R, 0)‖ maximal en R = 0) teste la localisation
     autour de la maille choisie, il n'identifie pas la lacune (c'est `recenter_mwr` qui choisit R_d = argmax ‖M(R, R)‖) ;
  4. le « modulo pN » fait une seule fois, au lieu d'être répété dans chaque fonction (amas, phases, distances, figures).
- **Ordre** : après l'alignement (qui repère les N² mailles de la super-cellule par leurs étiquettes brutes), avant la troncature.

## 5. Troncature

- Production : `R_local = Rn[‖Rn‖ ≤ R_cut]`, **norme euclidienne des indices réduits** √(n₁² + n₂²) des étiquettes recentrées.
  **Pas** d'images de Wigner-Seitz.
- **Pourquoi pas d'images minimales pour la troncature** : après recentrage, toutes les mailles retenues sont **strictement
  à l'intérieur** de la cellule de Wigner-Seitz de la boîte centrée sur la lacune.
  - Super-réseau hexagonal de paramètre L = pN a → cercle inscrit de la cellule de Wigner-Seitz de rayon pN a / 2 ≥ 12 a (pN ≥ 24).
  - Amas de 29 mailles : au plus 3.46 a de l'origine (maille (2, 2)) → marge de plus d'un facteur 3.
  - Donc chaque étiquette recentrée **est** son image minimale (repliement et Wigner-Seitz coïncident près de l'origine),
    et aucune égalité n'est possible (elles n'existent que sur le bord) → même amas, mêmes phases, même Γ.
  - Condition générale : rayon de troncature cartésien < pN a / 2. Avant recentrage, vrai aussi, mais en mesurant depuis R_d modulo pN.
  - À écrire : « cohérent avec la convention ».
- **La vraie question est la métrique** : norme réduite ≤ 3 → 29 mailles, non invariantes par rotation de 60°
  ((2, 2) à 3.46 a retenue, (3, −3) à 3 a exclue) ; disque cartésien de 3 a → 37 mailles, invariant.
  Effet couvert par la convergence en R_cut (Γ : < 0.4 % de 2 à 3, 0.2 % de 3 à 4). Une demi-phrase dans le texte.

## 6. Où Wigner-Seitz compte, où il ne compte pas

- **Compte** : interpolation de M **complète** (tous les R) hors grille → référence « toutes les mailles » de `tab:rcut_M`,
  comparaison Kaasbjerg à K + δx̂, abscisse de `fig:M_locality`.
- **Ne compte pas** : matrice T, Γ, DOS (amas près de l'origine).

## 7. Littérature

- **Lu, Zhou, Bernardi 2020** (npj) : une phrase — R « in a Wigner–Seitz supercell centered at the origin », défaut à l'origine,
  taille = grille grossière, pas de remplissage par zéros → rien à recentrer ; poids des égalités non précisés.
- **Kaasbjerg 2020** : éléments ⟨φ_μ|V|φ_ν⟩ calculés directement en espace réel (LCAO), défaut au centre,
  coupure |R − R₀| > r_cut → positions physiques, pas de TF k → R, donc pas d'ambiguïté modulo la boîte.
- **Nous** : TF (comme Lu) + défaut au centre et boîte élargie (à cause du remplissage par zéros) → recentrage explicite
  + Wigner-Seitz de période pN. Avec le remplissage, centrer le défaut est inévitable : avant (décalage circulaire du potentiel)
  ou après (recentrage des étiquettes). Wigner-Seitz est inévitable pour toute interpolation par TF.

## 8. Plan du texte (structure de G)

Partie non locale → **Convention de l'image minimale** (principe + alignement, période N ; annonce des étiquettes)
→ **Alignement du potentiel** → **Recentrage et troncature** (recentrage ; troncature, norme réduite, remarque de symétrie ;
Wigner-Seitz de période pN pour l'interpolation de M complète, sans effet sur l'amas ; citer Lu) → **Normalisation**
(+ phrase Hartree → eV, renvoyée par la l. 644).

## 9. Perspective (doctorat)

Amas défini par les distances cartésiennes **depuis la lacune** (pas depuis l'origine de la maille), idéalement orbitale par
orbitale : garder (i, R) si le centre de Wannier R + τ_i est à moins de r_cut de la lacune → symétrie D₃h respectée.
Ce n'est pas une affaire d'images minimales (déjà satisfaites), mais de métrique et de centre.

Autre piste (2026-10-02) : **remplissage par zéros avec un masque de Wigner-Seitz.** Aujourd'hui le potentiel est gardé sur le
losange N×N ; ses coins aigus sont plus proches des images voisines, donc on y garde surtout leurs queues. Garder seulement les
points plus proches de la lacune centrale que de toute image (cellule de Wigner-Seitz, frontière à mi-chemin), ou une fenêtre
douce, serait la coupure la plus fidèle au défaut isolé. Effet petit ici (remplissage validé pour N ≥ 7).
(Une cellule DFT en forme de Wigner-Seitz est impossible en ondes planes — il faut un parallélépipède — et inutile :
le système périodique est le même, et l'image minimale fait ce choix après coup.)

## 10. Alignement et composante k′ = k (2026-10-02, après-midi)

- Identité exacte (états normalisés sur la maille, `make_tables.py`) : M^L_nn(k,k) = Σ_mailles ∫ ΔV |u_nk|², chaque maille donne ∫|u|² = 1
  → une constante c sur N² mailles ajoute exactement N² c.
- **Données** (`level2_families.csv`, Re M^L à K) : brut 3m 11.36, 11.31, 11.22 eV (plat) ; aligné 13.17, 13.34, 13.91 eV (dérive de N²|C_N|).
  C_N ne décroît pas en 1/N² : 3m N ≥ 9, C_N ≈ −11.6 − 1083/N² meV (asymptote non nulle ; ajustement fait en conversation, pas encore dans `donnees/`).
- **Conclusion** : la matrice brute est intensive à k′ = k, l'alignée ne l'est pas ; c'est l'alignement qui introduit le terme.
  Hypothèse (non vérifiée) : la moyenne de site (sphères de 1 Å, région du cœur) ne mesure pas le décalage vu par les états π.
  Décision ouverte (TODO, fin de §4.1.4) : tests = moyenne de ΔV_brut pondérée par la densité π, dépendance au rayon des sphères, profil hors du plan.
- **Noyau de Dirichlet** : en base de Bloch, le terme vaut −C · S(q) · [V†(k′)V(k)]_mn, q = k′ − k, S(q) = Π_j sin(Nθ_j/2)/sin(θ_j/2), θ_j = q·a_j.
  S(0) = N² ; S = 0 aux points de la grille grossière (q ≠ 0) ; ~2/θ entre eux (décroissance en 1/q).
  Le long de b₁ ou b₂ (q·a₂ = 0 ou q·a₁ = 0), un facteur vaut N → |S| ~ N·2/θ : croît comme N à q fixé. Ailleurs : borné.
  Sur la grille grossière (p = 1) on retrouve N² δ_kk′ (la boîte est tout l'espace périodique).
- **Troncature** : la matrice T ne voit que −C_N sur les 29 mailles retenues → borné, mais dépendant de N via C_N.
- Le test max|M| (`fig:M_scaling`) ne sonde pas cette région (max atteint loin de la diagonale).
