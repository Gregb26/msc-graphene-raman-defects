# donnees — données derrière les figures et les tables du mémoire

Ce dossier contient les données finales que lisent les scripts de `scripts/fig/` pour tracer les figures du mémoire.
Rien n'y est calculé : ce sont des copies figées des produits du dépôt de recherche `graphene-raman`
(dossier `results/` au commit `14e8c2a`, étiquette `memoire-apres-menage` ; `ch4/` vient de `campagnes/M/ch4/`, non suivi par git
là-bas, état du 2026-09-30), vérifiées octet par octet à la copie.

Les scripts ne lisent jamais un chemin écrit en dur. Ils demandent chaque dossier à `graphene_raman.config`,
qui le lit dans `config/production.json`. La colonne « Clé » donne la clé correspondante.

| Dossier | Contenu | Chapitre | Clé de `production.json` | Fichiers | Taille |
|---|---|---|---|---|---|
| `M2_plateau/` | produits de la chaîne matrice *M* → matrice *T* → Γ, avec l'alignement de Kumagai–Oba : cartes de convergence (`specwd_*`), résonance (`resonance_*`), localité (`mwr_locality`), potentiel de défaut (`ved_analysis`), comparaison Γ^ed / Γ^ep (`ed_vs_ep_*`), tables `.csv` | 4 et 5 | `results_dir` | 29 | 48 Mo |
| `epw/` | post-traitement des calculs EPW : validation des bandes et des phonons, auto-énergie des électrons (`selfen_*`) et des phonons (`phself_*`), dispersion DFPT directe, densité d'états des phonons | 5 | `epw_results_dir` | 23 | 4,8 Mo |
| `electron/` | convergence du calcul SCF (`ecut`, `kpoint`, `smearing`), bandes et densité d'états du graphène parfait, pseudopotentiel du carbone (`C.upf`) | 2 | `electron_results_dir` | 7 | 1,5 Mo |
| `phonon/` | dispersion et densité d'états des phonons (matdyn) | 2 | `phonon_results_dir` | 2 | 0,2 Mo |
| `wannier/<D>x<D>/` | sorties de Wannier90 pour huit grilles : hamiltonien `wannier_tb.dat`, matrices de jauge `wannier_u*.mat`, `wannier.wout`, `wannier.eig`, manifeste sha256 | 2 et 4 | `wannier_dir` | 48 | 33 Mo |
| `campagnes/<campagne>/` | données des campagnes de calcul lues par les figures de contrôle (R7, R9, R10), les figures de désordre moyenné (R8) et la figure du couplage électron-photon (EM) ; détail dans `campagnes/README.md` | 2 et 4 | `campaigns_results_dir` | 38 | 18 Mo |
| `ch4/` | chiffres du chapitre 4 : `table_v1_final.md` (chaque valeur avec son fichier source et sa clé, de l'ancienne normalisation à la production finale), `defauts_nombres.md` (les nombres cités dans `défauts.tex` appariés à cette table), `alignement_regions.*` (régions d'échantillonnage de l'alignement, 13 tailles) ; produits par `campagnes/M/ch4/ch4_chiffres.py` de `graphene-raman`, qui ne tourne pas ici | 4 | — (pas lu par les scripts) | 6 | 0,7 Mo |
| `M2/` | seulement un `README.md` et la liste des sommes md5 des matrices *M* ; les matrices elles-mêmes (`M_*.npy`, plusieurs Go) ne sont pas dans ce dépôt | 4 | `matrices_dir` | 2 | — |

Total : 155 fichiers, 107 Mo.

## Vérifier l'intégrité

`MD5SUMS_2026-10-01.txt` liste la somme md5 de chaque fichier de données (152 lignes, sans les README). Depuis ce dossier :

```bash
md5sum -c MD5SUMS_2026-10-01.txt        # Linux
md5 -r $(cut -d' ' -f2 MD5SUMS_2026-10-01.txt) | diff - MD5SUMS_2026-10-01.txt   # macOS
```

## Ce qui n'est pas ici

- Les matrices *M* (`M_*.npy`) et les fonctions d'onde (`.save`) : trop lourdes, conservées sur la grappe de calcul.
  Les figures n'en ont pas besoin, elles partent des produits de `M2_plateau/`.
- Les produits des versions antérieures de la chaîne (`results/M` et `results/M2` de `graphene-raman`) : ils ne servent
  qu'à la table de comparaison du chapitre 4, produite dans le dépôt de recherche.

## À noter

Les fichiers `README.md` des sous-dossiers et les tables de `ch4/` viennent de `graphene-raman` : ils nomment ces dossiers
`results/…` au lieu de `donnees/…`, et citent des chemins `campagnes/…` qui n'existent que dans le dépôt de recherche.
Le contenu est le même.
