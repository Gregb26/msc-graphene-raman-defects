# PROVENANCE — d'où vient chaque figure, table et chiffre du mémoire

Registre de provenance du mémoire : une ligne par figure, table ou groupe de chiffres cités dans `memoire/`.

État : copie depuis `graphene-raman`, tag `memoire-apres-menage` (`14e8c2a`), faite le 2026-09-30
(commits `bbed6f0`, `12da2f0`, `3e2e5ad`) ; recette passée le 2026-10-01 (§0).
Tous les chemins sont relatifs à la racine de ce dépôt, sauf `GR:` = `graphene-raman` au tag ci-dessus.
`lit.` = valeur de la littérature citée dans le texte.

---

## 0. Structure et recette

```
msc-graphene-raman-defects/
├── pyproject.toml             paquet graphene_raman (identique à GR)
├── src/graphene_raman/        identique à GR:src/graphene_raman/
├── scripts/{fig,m,t,epw,validation,slurm}/   identiques à GR:scripts/
├── tests/                     identique à GR:tests/
├── config/production.json     identique à GR, sauf les chemins results/… → donnees/…
├── donnees/                   = GR:results/ sans M/ ni les produits de M2/ ; + ch4/ (voir donnees/README.md)
├── calculs/                   inputs QE / Wannier90 / EPW (à remplir)
└── memoire/                   LaTeX
```

Installation : `python -m venv .venv && .venv/bin/pip install -e ".[mpi,test]"`. Tous les scripts se lancent depuis la
racine. Les scripts de figures écrivent par défaut dans `figures/<domaine>/` ; pour le mémoire,
`--outdir memoire/figures`.

**Recette du 2026-10-01** (VM Linux, Python 3.10, NumPy 2.2.6, Matplotlib 3.10.9, MPICH 5.0.2) :

| Contrôle | Résultat |
|---|---|
| `donnees/` : `md5sum -c MD5SUMS_2026-10-01.txt` | 152 / 152 OK |
| `donnees/` contre `GR:results/` au tag, octet par octet | 151 fichiers identiques ; seul `campagnes/README.md` diffère (une note mise à jour) |
| `src/`, `scripts/`, `tests/`, `pyproject.toml` contre le tag | identiques (`diff -r` vide) |
| `config/production.json` contre le tag | seules les clés de chemins diffèrent (`results/` → `donnees/`, `results_dir_frozen` vidé) |
| `pytest tests` | 233 réussis, 5 sautés (données DFT `.save` absentes, attendu) |
| les 8 scripts de `scripts/fig/` lancés depuis ce dépôt | 47 PDF, aucune erreur, aucune lecture hors de `donnees/` et `config/` |
| mêmes scripts depuis un export du tag, même environnement | 47 / 47 PDF identiques octet par octet à ceux de ce dépôt |
| contre les PDF du tag (`GR:figures/`, générés sur le Mac) | 38 / 47 identiques ; les 9 autres (cartes en couleur) identiques au pixel près à 100 ppp, l'écart est dans l'encodage des images intégrées |

Réserves de la recette : `cm-super` absent de la VM (paquet `type1ec` remplacé par un fichier vide), PNG non
produits (pas de `dvipng`). Effet de bord : `scripts/fig/make_figures.py` réécrit `donnees/M2_plateau/level{1,2}_summary.csv`
à chaque exécution (contenu inchangé à la recette).

---

## 1. Figures incluses dans le mémoire (20)

État par rapport à `memoire/figures/` (comparaison au pixel, 100 ppp, contre les PDF du tag) :
**même contenu** = seules les métadonnées diffèrent, rien à faire ; **R10** = le mémoire a la version R6, la
version finale diffère et sera installée avec la réécriture du ch. 4 ; **ch. 2 refaite** = redessinée dans le style du
mémoire (taille et mise en page changent), à valider.

| Label | Fichier du mémoire | .tex:ligne | Producteur | Données lues | État |
|---|---|---|---|---|---|
| `fig:KB` | `KB_projectors_C.pdf` | théorie:191 | `scripts/fig/make_figures_electron.py` → `fig_kb_pseudo_C` (**nom différent**) | `donnees/electron/C.upf` | ch. 2 refaite |
| `fig:convergence_dft` | `fig_electron_convergence.pdf` | théorie:319 | `make_figures_electron.py` | `donnees/electron/{ecut,ecut_cross,kpoint,smearing}.dat` | ch. 2 refaite |
| `fig:resultats_electrons` | `fig_ebands_edos.pdf` | théorie:326 | `make_figures_electron.py` | `donnees/electron/{ebands,edos}.dat` | ch. 2 refaite |
| `fig:phonon_results` | `fig_epw_phonons.pdf` | théorie:447 | `make_figures_epw.py` (variante : `make_figures_phonons.py` → `fig_phfreq_phdos`, données `donnees/phonon/`) | `donnees/epw/{validation,phdos}_24k24q_mv0.02.npz` | même contenu |
| `fig:Ved_zoom` | `fig_Ved_zoom.pdf` | défauts:268 | `make_figures.py` | `donnees/M2_plateau/ved_analysis.npz` | même contenu |
| `fig:Ved` | `fig_Ved.pdf` | défauts:284 | `make_figures_memoire.py` | `ved_analysis.npz` + C_N de `config/production.json` | **R10** |
| `fig:M_scaling` | `fig_M_scaling_final.pdf` | défauts:297 | `make_figures_memoire.py` | `M_analysis.npz` | **R10** |
| `fig:M_map` | `fig_M_map_final.pdf` | défauts:306 | `make_figures_memoire.py` | `M_analysis.npz` | **R10** |
| `fig:M_locality` | `fig_locality_final.pdf` | défauts:360 | `make_figures_memoire.py` | `mwr_locality.npz` | **R10** |
| `fig:ks_reconstruction` | `fig_ks_reconstruction.pdf` | défauts:402 | `make_figures.py` | `ks_reconstruction.npz` | même contenu |
| `fig:convergence` | `fig_convergence.pdf` | défauts:643 | `make_figures_memoire.py` | `specwd_{5x5,6x6,7x7,8x8,9x9,12x12}_prod.npz` | **R10** |
| `fig:level2` | `fig_level2.pdf` | défauts:676 | `make_figures.py` | `specwd_*_prod.npz` | **R10** |
| `fig:spectral` | `fig_spectral_final.pdf` | défauts:722 | `make_figures_memoire.py` | `resonance_9x9.npz`, `resonance_criteria_9x9.npz` | **R10** |
| `fig:epw_validation` | `fig_epw_validation.pdf` | eph:152 | `make_figures_epw.py` (options de production ci-dessous) | `donnees/epw/validation_24k24q_mv0.02.npz` | même contenu |
| `fig:epw_g_control` | `fig_epw_g_control.pdf` | eph:158 | idem | `donnees/epw/validation_24k24q_mv0.02.npz` | même contenu |
| `fig:epw_decay` | `fig_epw_decay.pdf` | eph:168 | idem | idem | même contenu |
| `fig:epw_kohn_degauss` | `fig_epw_kohn_degauss.pdf` | eph:180 | idem | `validation_24k24q{,_mv0.02}.npz`, `dfpt_path_freq_24k24q.npz` | même contenu |
| `fig:epw_gamma` | `fig_epw_gamma.pdf` | eph:235 | idem | `selfen_{120_dg0.0{1,2,5},240_dg0.02}_mv0.02_T{10,300}.npz` | même contenu |
| `fig:epw_phonselfen` | `fig_epw_phonselfen.pdf` | eph:290 | idem | `phself_path_1200_dg0.02_mv0.02.npz` | même contenu |
| `fig:epw_vs_ed` | `fig_epw_vs_ed.pdf` | eph:304 | idem | `selfen_240_dg0.02_mv0.02_T300.npz` + `donnees/M2_plateau/resonance_9x9.npz` | **R10** |

Sauf mention, les données du ch. 4 sont dans `donnees/M2_plateau/` et les scripts dans `scripts/fig/`.
Options de production de `make_figures_epw.py` (de `scripts/slurm/submit_post.sh figures`) :
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
| `fig_kaasbjerg_{dos_c,spectral_GKM,sigma_K,sensibilites,superposition}` | ch. 4 (réécriture, décidées) | `make_figures_kaasbjerg.py` | `donnees/campagnes/R8_kaasbjerg/` |
| `alignement_regions` (si retenue) | ch. 4 | `GR:campagnes/M/ch4/ch4_chiffres.py regions` (ne tourne pas ici : lit les `scf.in` de Rorqual) | `donnees/ch4/alignement_regions.{npz,pdf}` |
| `fig_em_coupling` | §2.5 électron-photon | `make_figures_em.py` | `donnees/campagnes/EM/{M4_sigma,EM3,EM2}/` |
| contrôles du ch. 4 : `fig_{offset_profiles_13,levels_vs_invN,kaasbjerg_plateau_ws,resonance_vs_nkint{,_plateau},rcut_aligned,folded_vs_R7,size_3m,localized_3m}` | ch. 4 ou annexe, à décider | `make_figures_controles.py` | `donnees/campagnes/{R7_tailles_3m,R9_controles,R10_plateau}/` |
| figures de travail : `fig_{M_map,M_scaling,locality,spectral,plateau,rcut}`, `fig_Ved_{map,boundary,profile_mean,radial,radial_masked}` | — | `make_figures.py` | `donnees/M2_plateau/` |

---

## 2. Tables

Toutes les tables sont saisies à la main dans le `.tex`, sans `\input` de csv.

| Label | .tex:ligne | Source |
|---|---|---|
| `tab:échantillonnage` | défauts:247 | `donnees/M2_plateau/sampling_table.csv` |
| `tab:L_NL` | défauts:337 | `donnees/M2_plateau/lnl_frobenius.csv` |
| `tab:rcut_M` | défauts:370 | `donnees/M2_plateau/m_rcut_convergence.csv` (deux valeurs après décision R10) |
| `tab:tests_M` | défauts:415 | `donnees/M2_plateau/M_tests_summary.csv` |
| `tab:convergence_gamma` | défauts:653 | `donnees/M2_plateau/{level1_summary,level2_summary,level2_families}.csv` |
| `tab:tests_T` | défauts:691 | `donnees/M2_plateau/nkint_check_9x9.csv` ; `NOTES_TGAMMA.md` (**pas dans ce dépôt**, voir §4) |
| `tab:kohn_chaines` | eph:194 | `donnees/epw/d2_extract_24k24q{,_mv0.02}.npz`, `validation_24k24q{,_mv0.02}.npz` |
| `tab:gamma_ep_conv` | eph:219 | `donnees/epw/selfen_*_T300.npz` |
| `tab:gamma_ph_conv` | eph:254 | `donnees/epw/phself_path_{240,1200}_dg0.02*.npz` |
| `tab:gamma_ph_prod` | eph:275 | `donnees/epw/phself_path_1200_dg0.02_mv0.02.npz` |
| `tab:param_dft` | annexes/paramètres:10 | inputs QE (`calculs/`, à remplir) |
| `tab:param_dfpt` | paramètres:37 | inputs ph.x (`calculs/`, à remplir) |
| `tab:param_wannier` | paramètres:62 | `donnees/wannier/*/wannier.wout` |
| `tab:param_M` | paramètres:86 | `config/production.json` |
| `tab:param_T` | paramètres:117 | `config/production.json` ; `NOTES_TGAMMA.md` (**pas dans ce dépôt**) |
| `tab:param_epw` | paramètres:143 | inputs EPW (`calculs/`, à remplir) ; `NOTES_EPW.md` (**pas dans ce dépôt**) |

Les sources des quatre tables du ch. 5 sont déduites des noms de fichiers ; l'appariement valeur par valeur reste à faire.

---

## 3. Chiffres cités dans le texte (valeurs avec unité, hors paramètres d'entrée)

| Chapitre | Nb. | Provenance | Remarque |
|---|---|---|---|
| Introduction | 2 | lit. (l. 13 : 130 GPa, 97.7 %) | citées, pas de données |
| Ch. 2 théorie | 25 | §2.2 : 2.466 Å, 5.46 eV, convergence 0.1 meV → `donnees/electron/`. §2.3 : 1550.5 et 1583 cm⁻¹, écart 2 %, 468/1394/1602 cm⁻¹ → `donnees/epw/phdos_24k24q_mv0.02.npz`, `validation_24k24q_mv0.02.npz` et lit. | 100 Ry et 0.01 Ry sont des paramètres, voir `tab:param_dft` |
| Ch. 3 Raman | 8 | lit. (positions des pics G, D, 2D… ; 10 nm) | aucune donnée |
| Ch. 4 défauts | 111 | `donnees/ch4/table_v1_final.md` (source des valeurs finales, avec fichier et clé de chaque valeur) ; appariement dans `donnees/ch4/defauts_nombres.md` | **le texte cite encore les valeurs v1** : à refaire avec la réécriture ; `defauts_nombres.md` ne se régénère que dans GR |
| Ch. 5 EPW | 176 | `donnees/epw/*.npz` ; Γ^ed/Γ^ep (§5.3.5, l. 301–312) → `donnees/M2_plateau/ed_vs_ep_24k24q_mv0.02.npz` et `table_v1_final.md` | à apparier comme pour le ch. 4 ; l. 303–312 dépendent du ch. 4 (Γ^ed R6 → R10) |
| Conclusion | 5 | reprend ch. 4–5 (300 K, 1 %, 3 eV, 0.6 %, 14 cm⁻¹) | à revoir après la réécriture du ch. 4 |
| Résumé / abstract | 2 + 2 | reprend ch. 4–5 (300 K, 1 %) | idem |

Liste détaillée par ligne (hors ch. 4) : annexe A.

---

## 4. Ce qui n'est pas dans ce dépôt

| Quoi | Où | Conséquence |
|---|---|---|
| matrices *M* (`M_*.npy`), fonctions d'onde (`.save`) | Rorqual (`/project`, nearline) | les scripts `m/`, `t/` et `validation/` ne se relancent pas ici ; les figures n'en ont pas besoin |
| produits v1 et v2 (`GR:results/M/`, produits de `GR:results/M2/`) | GR | servent seulement à la colonne « v1 » de `table_v1_final.md` |
| pilotes de campagne (`ch4_chiffres.py`, `r8_driver.py`, `r10_driver.py`, EM) | `graphene-raman/campagnes/` sur le laptop, **non suivi par git dans GR** | leurs sorties sont dans `donnees/` ; le code n'est versionné nulle part |
| `NOTES_TGAMMA.md`, `NOTES_EPW.md`, `NOTES_EPW_REPERES.md` | `graphene-raman/notes/` sur le laptop, **non suivi par git dans GR** | citées comme source de `tab:tests_T`, `tab:param_T`, `tab:param_epw` |
| inputs QE / Wannier90 / EPW | Rorqual | `calculs/` à remplir |

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
