# PROVENANCE — d'où vient chaque figure, table et chiffre du mémoire

Registre de provenance du mémoire. Une ligne par figure, table ou groupe de chiffres cités dans `memoire/`.
État : **inventaire côté texte seulement** (2026-09-30), fait sur `main` à `e78cfac`.
Les colonnes « source » renvoient à l'état actuel de `graphene-raman`, HEAD `656c05c`
(`INVENTAIRE_2026-09-16.md`, §8, §10 et §13 étape F), avant le ménage.
Les colonnes « dans msc- » seront remplies au moment de la copie, avec le commit source exact.

Conventions :
- `GR:` = chemin dans `graphene-raman`, `QEPP:` = `~/projects/qe_pp` (hors dépôt), `lit.` = valeur de la littérature citée dans le texte.
- État figure : **R10** = identique à la production finale ; **R6** = le mémoire a encore l'ancienne version (md5 différent de `GR:figures/`, à réinstaller avec la réécriture du ch. 4).

---

## 0. Structure cible de msc- (décision du 2026-09-30)

Le dépôt reprend la forme *src layout* de graphene-raman ; les imports du paquet marchent par installation
(`pip install -e .`), pas par emplacement. Les dossiers `analyse/` et `scripts_figures/` créés le matin sont
remplacés par `src/` et `scripts/fig/`.

```
msc-graphene-raman-defects/
├── pyproject.toml              ← celui de graphene-raman
├── src/graphene_raman/         ← paquet (renommé depuis electron_defect_interaction), sans les orphelins
├── scripts/                    ← même arborescence que graphene-raman après ménage (fig/, …)
├── campagnes/                  ← ce qui sert au mémoire : M/ch4, R/R8_kaasbjerg (pilote), EM
├── config/production.json      ← results_dir = donnees/  (seule ligne à changer à la copie)
├── donnees/                    ← results/M2_plateau, results/epw, sorties R8, ch4/*.md, EM/*.npz
├── calculs/                    ← inputs QE / Wannier90 / EPW / SLURM, un dossier par calcul
├── tests/
├── notes/                      ← NOTES_TGAMMA, NOTES_EPW, NOTES_EPW_REPERES (copies figées)
└── memoire/                    ← LaTeX
```

Conditions pour que la copie soit un `cp -r` : les scripts de figures trouvent `_palette` et `memoire.mplstyle`
par rapport à `__file__` ; tout accès aux résultats passe par `config.results_dir()` ; aucun `sys.path` relatif au
cwd. `ch4_chiffres.py` reste un générateur lié à graphene-raman : on copie ses sorties, pas sa capacité à tourner.

Vérification à la copie : régénérer les 20 figures depuis msc- et comparer les md5 à `graphene-raman/figures/`
(tag d'après ménage).

---

## 1. Figures incluses (20)

| Label | Fichier | .tex:ligne | Producteur (source) | Données lues (source) | État | Dans msc- |
|---|---|---|---|---|---|---|
| `fig:KB` | `KB_projectors_C.pdf` | théorie:191 | probablement `GR:plotting/plot_psp_radial_proj.py`, sortie manuelle | pseudo-potentiel C (`.upf`/`.psp8`) | hors chaîne | |
| `fig:convergence_dft` | `fig_electron_convergence.pdf` | théorie:319 | `QEPP:plot_convergence.py` | sorties QE de convergence (qe_pp) | hors dépôt GR | |
| `fig:resultats_electrons` | `fig_ebands_edos.pdf` | théorie:326 | `QEPP:plot_ebands_edos.py` | bandes + DOS QE (qe_pp) | hors dépôt GR | |
| `fig:phonon_results` | `fig_epw_phonons.pdf` | théorie:447 | `GR:scripts/fig/make_figures_epw.py` | `GR:results/epw/*` (phdos) | R10 (identique) | |
| `fig:Ved_zoom` | `fig_Ved_zoom.pdf` | défauts:268 | `GR:scripts/fig/make_figures.py` | `ved_analysis.npz` | R10 (identique) | |
| `fig:Ved` | `fig_Ved.pdf` | défauts:284 | `GR:scripts/fig/make_figures_memoire.py` | `ved_analysis.npz` + C_N | **R6** | |
| `fig:M_scaling` | `fig_M_scaling_final.pdf` | défauts:297 | `make_figures_memoire.py` | `M_analysis` | **R6** | |
| `fig:M_map` | `fig_M_map_final.pdf` | défauts:306 | `make_figures_memoire.py` | `M_analysis` | **R6** | |
| `fig:M_locality` | `fig_locality_final.pdf` | défauts:360 | `make_figures_memoire.py` | `mwr_locality` | **R6** | |
| `fig:ks_reconstruction` | `fig_ks_reconstruction.pdf` | défauts:402 | `make_figures.py` | `ks_reconstruction.npz` | R10 (identique) | |
| `fig:convergence` | `fig_convergence.pdf` | défauts:643 | `make_figures_memoire.py` | `specwd_*_prod` (×6) | **R6** | |
| `fig:level2` | `fig_level2.pdf` | défauts:676 | `make_figures.py` | `specwd`, `level2_*.csv` | **R6** | |
| `fig:spectral` | `fig_spectral_final.pdf` | défauts:722 | `make_figures_memoire.py` | `resonance_9x9` + criteria | **R6** | |
| `fig:epw_validation` | `fig_epw_validation.pdf` | eph:152 | `make_figures_epw.py` | `GR:results/epw/*.npz` | R10 (identique) | |
| `fig:epw_g_control` | `fig_epw_g_control.pdf` | eph:158 | `make_figures_epw.py` | `results/epw/*.npz` | R10 (identique) | |
| `fig:epw_decay` | `fig_epw_decay.pdf` | eph:168 | `make_figures_epw.py` | `results/epw/*.npz` | R10 (identique) | |
| `fig:epw_kohn_degauss` | `fig_epw_kohn_degauss.pdf` | eph:180 | `make_figures_epw.py` | `results/epw/*.npz` (chaînes 0.002 et 0.02) | R10 (identique) | |
| `fig:epw_gamma` | `fig_epw_gamma.pdf` | eph:235 | `make_figures_epw.py` | `results/epw/*.npz` | R10 (identique) | |
| `fig:epw_phonselfen` | `fig_epw_phonselfen.pdf` | eph:290 | `make_figures_epw.py` | `results/epw/*.npz` | R10 (identique) | |
| `fig:epw_vs_ed` | `fig_epw_vs_ed.pdf` | eph:304 | `make_figures_epw.py` | `results/epw/*.npz` + `resonance_9x9` | **R6** | |

Les données `ved_analysis`, `M_analysis`, `mwr_locality`, `ks_reconstruction`, `specwd_*`, `resonance_*` et `*.csv` sont
dans `GR:results/M2_plateau/`, la base finale R10 (voir `MD5SUMS_2026-09-30.txt`).
Style commun : `GR:scripts/_palette.py` et `GR:figures/memoire.mplstyle`.

### Figures TikZ (aucune donnée)

`memoire/tikz/*.tex` : diagrammes dessinés à la main (cycles SCF, Dyson, matrice T, règles Raman, pp/pd, e1/h1,
échelle de Jacob). Rien à tracer. `tikz/jacob_ladder.log` est un résidu de compilation à supprimer ou à ignorer.

### Figures à venir (décidées, pas encore incluses)

| Figure | Pour | Producteur (source) | Données |
|---|---|---|---|
| `dos_c`, `spectral_GKM`, `sigma_K`, `sensibilites`, `superposition` | ch. 4 (réécriture) | `GR:campagnes/R/R8_kaasbjerg/r8_driver.py fig` (`sigeff` pour `sigma_K`) | `GR:campagnes/R/R8_kaasbjerg/out/` |
| `alignement_regions` (si retenue) | ch. 4 | `GR:campagnes/M/ch4/ch4_chiffres.py regions` (**exige Rorqual** : lit les `scf.in` des super-cellules) | `GR:campagnes/M/ch4/alignement_regions.npz` |
| `fig_em_coupling` | §2.5 électron-photon | `GR:scripts/fig/make_figures_em.py` | `GR:campagnes/EM/{M4_sigma,EM3,EM2}` |

---

## 2. Tables

Toutes les tables sont saisies à la main dans le `.tex`, sans `\input` de csv.

| Label | .tex:ligne | Source |
|---|---|---|
| `tab:échantillonnage` | défauts:247 | `sampling_table.csv` |
| `tab:L_NL` | défauts:337 | `lnl_frobenius.csv` |
| `tab:rcut_M` | défauts:370 | `m_rcut_convergence.csv` (deux valeurs après décision R10) |
| `tab:tests_M` | défauts:415 | `M_tests_summary.csv` |
| `tab:convergence_gamma` | défauts:653 | `level1_summary.csv`, `level2_*.csv` |
| `tab:tests_T` | défauts:691 | `nkint_check_9x9.csv`, `GR:notes/NOTES_TGAMMA.md` |
| `tab:kohn_chaines` | eph:194 | `GR:results/epw/*.npz` via `epw_*_post.py` |
| `tab:gamma_ep_conv` | eph:219 | idem |
| `tab:gamma_ph_conv` | eph:254 | idem |
| `tab:gamma_ph_prod` | eph:275 | idem |
| `tab:param_dft` | annexes/paramètres:10 | inputs QE (`calculs/`) |
| `tab:param_dfpt` | paramètres:37 | inputs ph.x (`calculs/`) |
| `tab:param_wannier` | paramètres:62 | `GR:wannier/*/wannier.wout` |
| `tab:param_M` | paramètres:86 | `GR:config/production.json` |
| `tab:param_T` | paramètres:117 | `production.json`, `GR:notes/NOTES_TGAMMA.md` |
| `tab:param_epw` | paramètres:143 | inputs EPW, `GR:notes/NOTES_EPW.md` |

---

## 3. Chiffres cités dans le texte (valeurs avec unité, hors paramètres d'entrée)

| Chapitre | Nb. | Provenance | Remarque |
|---|---|---|---|
| Introduction | 2 | lit. (l. 13 : 130 GPa, 97.7 %) | citées, pas de données |
| Ch. 2 théorie | 25 | §2.2 : 2.466 Å, 5.46 eV, convergence 0.1 meV → `QEPP`. §2.3 : 1550.5 et 1583 cm⁻¹, écart 2 %, 468/1394/1602 cm⁻¹ → `GR:results/epw` (phdos) et lit. | 100 Ry et 0.01 Ry sont des paramètres, voir `tab:param_dft` |
| Ch. 3 Raman | 8 | lit. (positions des pics G, D, 2D… ; 10 nm) | aucune donnée |
| Ch. 4 défauts | 111 | `GR:campagnes/M/ch4/table_v1_final.md` (source des valeurs finales) ; appariement ligne par ligne dans `GR:campagnes/M/ch4/defauts_nombres.md` | **le texte cite encore les valeurs v1** : à refaire avec la réécriture ; régénérer `defauts_nombres.md` après |
| Ch. 5 EPW | 176 | `GR:results/epw/*.npz`, `GR:notes/NOTES_EPW.md` §1c–§1g ; Γ^ed/Γ^ep (§5.3.5, l. 301–312) → `table_v1_final.md` | à apparier comme pour le ch. 4 ; l. 303–312 dépendent du ch. 4 (Γ^ed R6 → R10) |
| Conclusion | 5 | reprend ch. 4–5 (300 K, 1 %, 3 eV, 0.6 %, 14 cm⁻¹) | à revoir après la réécriture du ch. 4 |
| Résumé / abstract | 2 + 2 | reprend ch. 4–5 (300 K, 1 %) | idem |

Liste détaillée par ligne (hors ch. 4) : voir l'annexe A ci-dessous.

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
