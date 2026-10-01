# Sources des tableaux du mémoire

Généré par `scripts/make_tables.py` (ne pas éditer). Une ligne par valeur affichée : texte LaTeX, valeur lue et source (`fichier : clé [sélection]`, chemins relatifs à `donnees/`, sauf `config/`). Les remarques de chaque tableau notent les choix de présentation et les cellules sans source lisible par machine.

## `tab:échantillonnage` — `tables/echantillonnage.tex` (§4.1.5, corps)

- Toutes les valeurs en meV. V̄^L(a_CC) **aligné** = brut − C_N (décision du TODO, chantier 1) ; la colonne brute n'est plus affichée (brut = aligné + C_N). ΔE_F ne dépend pas de l'alignement.
- N = 10 et 11 : SCF de super-cellules seulement (pas de matrice M) ; leurs C_N viennent de la même source.

| ligne | colonne | affiché | valeur lue | source |
|---|---|---|---|---|
| 6 | ΔE_F (meV) | $-20.5$ | -20.5 | `M2_plateau/sampling_table.csv : dE_F_meV [N = 6]` |
| 6 | C_N (meV) | $-50.5$ | -50.50914517629934 | `config/production.json : alignment.C_N_eV [6x6] × 10³` |
| 6 | V̄^L(a_CC) aligné (meV) | $+58.7$ | 58.709145176299344 | `M2_plateau/sampling_table.csv : Ved_radial_1.42A_meV [N = 6] − config/production.json : alignment.C_N_eV [6x6] × 10³` |
| 9 | ΔE_F (meV) | $-2.4$ | -2.4 | `M2_plateau/sampling_table.csv : dE_F_meV [N = 9]` |
| 9 | C_N (meV) | $-25.1$ | -25.14371002267805 | `config/production.json : alignment.C_N_eV [9x9] × 10³` |
| 9 | V̄^L(a_CC) aligné (meV) | $+68.4$ | 68.44371002267805 | `M2_plateau/sampling_table.csv : Ved_radial_1.42A_meV [N = 9] − config/production.json : alignment.C_N_eV [9x9] × 10³` |
| 12 | ΔE_F (meV) | $+2.5$ | 2.5 | `M2_plateau/sampling_table.csv : dE_F_meV [N = 12]` |
| 12 | C_N (meV) | $-18.7$ | -18.689593100831818 | `config/production.json : alignment.C_N_eV [12x12] × 10³` |
| 12 | V̄^L(a_CC) aligné (meV) | $+69.8$ | 69.78959310083182 | `M2_plateau/sampling_table.csv : Ved_radial_1.42A_meV [N = 12] − config/production.json : alignment.C_N_eV [12x12] × 10³` |
| 5 | ΔE_F (meV) | $-235.8$ | -235.8 | `M2_plateau/sampling_table.csv : dE_F_meV [N = 5]` |
| 5 | C_N (meV) | $-57.6$ | -57.562606201523394 | `config/production.json : alignment.C_N_eV [5x5] × 10³` |
| 5 | V̄^L(a_CC) aligné (meV) | $-306.8$ | -306.83739379847657 | `M2_plateau/sampling_table.csv : Ved_radial_1.42A_meV [N = 5] − config/production.json : alignment.C_N_eV [5x5] × 10³` |
| 7 | ΔE_F (meV) | $-866.1$ | -866.1 | `M2_plateau/sampling_table.csv : dE_F_meV [N = 7]` |
| 7 | C_N (meV) | $-26.9$ | -26.914294254341268 | `config/production.json : alignment.C_N_eV [7x7] × 10³` |
| 7 | V̄^L(a_CC) aligné (meV) | $-373.2$ | -373.18570574565877 | `M2_plateau/sampling_table.csv : Ved_radial_1.42A_meV [N = 7] − config/production.json : alignment.C_N_eV [7x7] × 10³` |
| 8 | ΔE_F (meV) | $-583.3$ | -583.3 | `M2_plateau/sampling_table.csv : dE_F_meV [N = 8]` |
| 8 | C_N (meV) | $-14.4$ | -14.410274533323342 | `config/production.json : alignment.C_N_eV [8x8] × 10³` |
| 8 | V̄^L(a_CC) aligné (meV) | $-255.5$ | -255.48972546667665 | `M2_plateau/sampling_table.csv : Ved_radial_1.42A_meV [N = 8] − config/production.json : alignment.C_N_eV [8x8] × 10³` |
| 10 | ΔE_F (meV) | $-508.7$ | -508.7 | `M2_plateau/sampling_table.csv : dE_F_meV [N = 10]` |
| 10 | C_N (meV) | $-9.3$ | -9.341716029942202 | `config/production.json : alignment.C_N_eV [10x10] × 10³` |
| 10 | V̄^L(a_CC) aligné (meV) | $-288.4$ | -288.3582839700578 | `M2_plateau/sampling_table.csv : Ved_radial_1.42A_meV [N = 10] − config/production.json : alignment.C_N_eV [10x10] × 10³` |
| 11 | ΔE_F (meV) | $-209.3$ | -209.3 | `M2_plateau/sampling_table.csv : dE_F_meV [N = 11]` |
| 11 | C_N (meV) | $-9.6$ | -9.550651557225422 | `config/production.json : alignment.C_N_eV [11x11] × 10³` |
| 11 | V̄^L(a_CC) aligné (meV) | $-244.3$ | -244.34934844277458 | `M2_plateau/sampling_table.csv : Ved_radial_1.42A_meV [N = 11] − config/production.json : alignment.C_N_eV [11x11] × 10³` |

## `tab:L_NL` — `tables/L_NL.tex` (§4.1.5, corps)

- Brut et aligné côte à côte (décision du 2026-10-01, R10 D6). M̄^NL ne dépend pas de l'alignement.
- Contrôles : `level2_families.csv` = `M_analysis.npz` (ReML_K, ReML_K_aligned, ReMNL_K) ; aligné − brut = N²|C_N| à 1e-8 eV près pour les six tailles.
- N = 5, 7, 8 : grilles élargies 25², 28², 32² sans K ; « K » y est le point de grille le plus proche (`lnl_<S>_dK` = 0.055, 0.050, 0.043 Å⁻¹) — à dire dans la légende.

| ligne | colonne | affiché | valeur lue | source |
|---|---|---|---|---|
| 5 | M̄^L(K) brut (eV) | $10.534$ | 10.534251736351404 | `M2_plateau/M_analysis.npz : lnl_5x5_ReL` |
| 5 | M̄^L(K) aligné (eV) | $11.973$ | 11.973316891523073 | `M2_plateau/M_analysis.npz : lnl_5x5_ReL_aligned` |
| 5 | M̄^NL(K) (eV) | $3.100$ | 3.1004099575437367 | `M2_plateau/M_analysis.npz : lnl_5x5_ReNL` |
| 5 | NL/L BZ brut | $0.258$ | 0.2578052049536437 | `M2_plateau/lnl_frobenius.csv : ratio_full [5x5]` |
| 5 | NL/L BZ aligné | $0.257$ | 0.2572153016716182 | `M2_plateau/lnl_frobenius.csv : ratio_full_aligned [5x5]` |
| 6 | M̄^L(K) brut (eV) | $11.356$ | 11.356081037016198 | `M2_plateau/M_analysis.npz : lnl_6x6_ReL` |
| 6 | M̄^L(K) aligné (eV) | $13.174$ | 13.17441026340056 | `M2_plateau/M_analysis.npz : lnl_6x6_ReL_aligned` |
| 6 | M̄^NL(K) (eV) | $3.103$ | 3.102988706968697 | `M2_plateau/M_analysis.npz : lnl_6x6_ReNL` |
| 6 | NL/L BZ brut | $0.252$ | 0.25244414666487575 | `M2_plateau/lnl_frobenius.csv : ratio_full [6x6]` |
| 6 | NL/L BZ aligné | $0.252$ | 0.2519315893483562 | `M2_plateau/lnl_frobenius.csv : ratio_full_aligned [6x6]` |
| 7 | M̄^L(K) brut (eV) | $10.486$ | 10.485717569026498 | `M2_plateau/M_analysis.npz : lnl_7x7_ReL` |
| 7 | M̄^L(K) aligné (eV) | $11.805$ | 11.804517987545477 | `M2_plateau/M_analysis.npz : lnl_7x7_ReL_aligned` |
| 7 | M̄^NL(K) (eV) | $3.101$ | 3.1008823454051875 | `M2_plateau/M_analysis.npz : lnl_7x7_ReNL` |
| 7 | NL/L BZ brut | $0.258$ | 0.25829922711993497 | `M2_plateau/lnl_frobenius.csv : ratio_full [7x7]` |
| 7 | NL/L BZ aligné | $0.258$ | 0.25802354135325317 | `M2_plateau/lnl_frobenius.csv : ratio_full_aligned [7x7]` |
| 8 | M̄^L(K) brut (eV) | $10.734$ | 10.734266871804461 | `M2_plateau/M_analysis.npz : lnl_8x8_ReL` |
| 8 | M̄^L(K) aligné (eV) | $11.657$ | 11.656524441943947 | `M2_plateau/M_analysis.npz : lnl_8x8_ReL_aligned` |
| 8 | M̄^NL(K) (eV) | $3.101$ | 3.1008536668855924 | `M2_plateau/M_analysis.npz : lnl_8x8_ReNL` |
| 8 | NL/L BZ brut | $0.257$ | 0.25666358087334196 | `M2_plateau/lnl_frobenius.csv : ratio_full [8x8]` |
| 8 | NL/L BZ aligné | $0.257$ | 0.2565179816585835 | `M2_plateau/lnl_frobenius.csv : ratio_full_aligned [8x8]` |
| 9 | M̄^L(K) brut (eV) | $11.305$ | 11.305093784928658 | `M2_plateau/M_analysis.npz : lnl_9x9_ReL` |
| 9 | M̄^L(K) aligné (eV) | $13.342$ | 13.341734296784253 | `M2_plateau/M_analysis.npz : lnl_9x9_ReL_aligned` |
| 9 | M̄^NL(K) (eV) | $3.103$ | 3.102990131127166 | `M2_plateau/M_analysis.npz : lnl_9x9_ReNL` |
| 9 | NL/L BZ brut | $0.252$ | 0.25238026362236965 | `M2_plateau/lnl_frobenius.csv : ratio_full [9x9]` |
| 9 | NL/L BZ aligné | $0.252$ | 0.2521218195055461 | `M2_plateau/lnl_frobenius.csv : ratio_full_aligned [9x9]` |
| 12 | M̄^L(K) brut (eV) | $11.222$ | 11.222042955604584 | `M2_plateau/M_analysis.npz : lnl_12x12_ReL` |
| 12 | M̄^L(K) aligné (eV) | $13.913$ | 13.913344362179998 | `M2_plateau/M_analysis.npz : lnl_12x12_ReL_aligned` |
| 12 | M̄^NL(K) (eV) | $3.103$ | 3.1029887069686977 | `M2_plateau/M_analysis.npz : lnl_12x12_ReNL` |
| 12 | NL/L BZ brut | $0.252$ | 0.2521472662877427 | `M2_plateau/lnl_frobenius.csv : ratio_full [12x12]` |
| 12 | NL/L BZ aligné | $0.252$ | 0.25195367625385306 | `M2_plateau/lnl_frobenius.csv : ratio_full_aligned [12x12]` |

## `tab:rcut_M` — `tables/rcut_M.tex` (§4.1.5 → annexe D)

- Production finale : alignement de Kumagai–Oba et étiquettes de Wigner-Seitz ; contrôle : le csv = `kaasbjerg/r10_c2_results.json` : rcut.<S>.plateau_ws à 1e-4 près. Grille fine 60² (colonne `fine_grid`).
- Deux chiffres significatifs.

| ligne | colonne | affiché | valeur lue | source |
|---|---|---|---|---|
| 0 | cellules | 1 | 1 | `M2_plateau/m_rcut_convergence.csv : n_sites [R_cut = 0]` |
| 0 | 9x9 π–π* | 32~\% | 0.31708 | `M2_plateau/m_rcut_convergence.csv : sv_mismatch_pi_blocks [9x9, R_cut = 0]` |
| 0 | 9x9 diag. | 32~\% | 0.31708 | `M2_plateau/m_rcut_convergence.csv : diag_max_dM_over_max [9x9, R_cut = 0]` |
| 0 | 12x12 π–π* | 99~\% | 0.99271 | `M2_plateau/m_rcut_convergence.csv : sv_mismatch_pi_blocks [12x12, R_cut = 0]` |
| 0 | 12x12 diag. | 87~\% | 0.86782 | `M2_plateau/m_rcut_convergence.csv : diag_max_dM_over_max [12x12, R_cut = 0]` |
| 1 | cellules | 5 | 5 | `M2_plateau/m_rcut_convergence.csv : n_sites [R_cut = 1]` |
| 1 | 9x9 π–π* | 19~\% | 0.18508 | `M2_plateau/m_rcut_convergence.csv : sv_mismatch_pi_blocks [9x9, R_cut = 1]` |
| 1 | 9x9 diag. | 15~\% | 0.15005 | `M2_plateau/m_rcut_convergence.csv : diag_max_dM_over_max [9x9, R_cut = 1]` |
| 1 | 12x12 π–π* | 19~\% | 0.18948 | `M2_plateau/m_rcut_convergence.csv : sv_mismatch_pi_blocks [12x12, R_cut = 1]` |
| 1 | 12x12 diag. | 19~\% | 0.18925 | `M2_plateau/m_rcut_convergence.csv : diag_max_dM_over_max [12x12, R_cut = 1]` |
| 2 | cellules | 13 | 13 | `M2_plateau/m_rcut_convergence.csv : n_sites [R_cut = 2]` |
| 2 | 9x9 π–π* | 6.6~\% | 0.066075 | `M2_plateau/m_rcut_convergence.csv : sv_mismatch_pi_blocks [9x9, R_cut = 2]` |
| 2 | 9x9 diag. | 4.6~\% | 0.0462 | `M2_plateau/m_rcut_convergence.csv : diag_max_dM_over_max [9x9, R_cut = 2]` |
| 2 | 12x12 π–π* | 13~\% | 0.12521 | `M2_plateau/m_rcut_convergence.csv : sv_mismatch_pi_blocks [12x12, R_cut = 2]` |
| 2 | 12x12 diag. | 13~\% | 0.12506 | `M2_plateau/m_rcut_convergence.csv : diag_max_dM_over_max [12x12, R_cut = 2]` |
| 3 | cellules | 29 | 29 | `M2_plateau/m_rcut_convergence.csv : n_sites [R_cut = 3]` |
| 3 | 9x9 π–π* | 2.6~\% | 0.025737 | `M2_plateau/m_rcut_convergence.csv : sv_mismatch_pi_blocks [9x9, R_cut = 3]` |
| 3 | 9x9 diag. | 1.7~\% | 0.017074 | `M2_plateau/m_rcut_convergence.csv : diag_max_dM_over_max [9x9, R_cut = 3]` |
| 3 | 12x12 π–π* | 3.3~\% | 0.032908 | `M2_plateau/m_rcut_convergence.csv : sv_mismatch_pi_blocks [12x12, R_cut = 3]` |
| 3 | 12x12 diag. | 3.1~\% | 0.030979 | `M2_plateau/m_rcut_convergence.csv : diag_max_dM_over_max [12x12, R_cut = 3]` |
| 4 | cellules | 49 | 49 | `M2_plateau/m_rcut_convergence.csv : n_sites [R_cut = 4]` |
| 4 | 9x9 π–π* | 2.0~\% | 0.019846 | `M2_plateau/m_rcut_convergence.csv : sv_mismatch_pi_blocks [9x9, R_cut = 4]` |
| 4 | 9x9 diag. | 1.4~\% | 0.014106 | `M2_plateau/m_rcut_convergence.csv : diag_max_dM_over_max [9x9, R_cut = 4]` |
| 4 | 12x12 π–π* | 2.5~\% | 0.025296 | `M2_plateau/m_rcut_convergence.csv : sv_mismatch_pi_blocks [12x12, R_cut = 4]` |
| 4 | 12x12 diag. | 1.5~\% | 0.015291 | `M2_plateau/m_rcut_convergence.csv : diag_max_dM_over_max [12x12, R_cut = 4]` |
| 5 | cellules | 81 | 81 | `M2_plateau/m_rcut_convergence.csv : n_sites [R_cut = 5]` |
| 5 | 9x9 π–π* | 1.1~\% | 0.01104 | `M2_plateau/m_rcut_convergence.csv : sv_mismatch_pi_blocks [9x9, R_cut = 5]` |
| 5 | 9x9 diag. | 1.2~\% | 0.011945 | `M2_plateau/m_rcut_convergence.csv : diag_max_dM_over_max [9x9, R_cut = 5]` |
| 5 | 12x12 π–π* | 1.6~\% | 0.016202 | `M2_plateau/m_rcut_convergence.csv : sv_mismatch_pi_blocks [12x12, R_cut = 5]` |
| 5 | 12x12 diag. | 0.85~\% | 0.0085068 | `M2_plateau/m_rcut_convergence.csv : diag_max_dM_over_max [12x12, R_cut = 5]` |
| 6 | cellules | 113 | 113 | `M2_plateau/m_rcut_convergence.csv : n_sites [R_cut = 6]` |
| 6 | 9x9 π–π* | 0.92~\% | 0.0091728 | `M2_plateau/m_rcut_convergence.csv : sv_mismatch_pi_blocks [9x9, R_cut = 6]` |
| 6 | 9x9 diag. | 1.0~\% | 0.010052 | `M2_plateau/m_rcut_convergence.csv : diag_max_dM_over_max [9x9, R_cut = 6]` |
| 6 | 12x12 π–π* | 1.1~\% | 0.011178 | `M2_plateau/m_rcut_convergence.csv : sv_mismatch_pi_blocks [12x12, R_cut = 6]` |
| 6 | 12x12 diag. | 0.87~\% | 0.0086769 | `M2_plateau/m_rcut_convergence.csv : diag_max_dM_over_max [12x12, R_cut = 6]` |

## `tab:tests_M` — `tables/tests_M.tex` (§4.1.5 → annexe D)

- Ligne « 16 → 20 bandes » retirée (non rejouable avec M2 ; TODO). Ajouts : application directe de V_ed (porte A.2, toutes les tailles ; valeur affichée = le plus grand des écarts L et NL) et convention intensive par famille (remplace la ligne sur six tailles).
- Hermiticité : maximum sur les six tailles (la légende actuelle dit « valeur de la 9×9 sauf mention »). Reconstruction KS : fourchette sur les six tailles. Deux chiffres significatifs.
- Non repris (à trancher) : « g0 par lots vs référence » (1.2e-14) et « test d'or » (1.8e-13), qui sont des tests de la chaîne T (le second est dans `tab:tests_T`) ; portes D6 de l'alignement (`M_analysis.npz` : align_gate_*).

| ligne | colonne | affiché | valeur lue | source |
|---|---|---|---|---|
| Reconstruction KS, grille $N\times N$ | valeur | 1.5--32~$\mu$eV | 1.533–32.04 µeV | `M2_plateau/ks_reconstruction.npz : <S>_coarse_max_meV, six tailles (min–max, × 10³)` |
| \quad éléments hors diagonaux | valeur | $\le 1.3\times10^{-6}$ | 1.3198895695999441e-06 | `M2_plateau/ks_reconstruction.npz : <S>_coarse_offdiag_rel, six tailles (max)` |
| Reconstruction KS, grille élargie | valeur | 0.21--10~meV | 0.2052–9.988 meV | `M2_plateau/ks_reconstruction.npz : <S>_dense_max_meV, six tailles (min–max)` |
| Hermiticité ($M$ élargi, six tailles) | valeur | $\le 2.3\times10^{-14}$ | 2.29e-14 | `M2_plateau/M_tests_summary.csv : valeur [hermiticité M dense <S>, six tailles] (max)` |
| Hermiticité ($M$ élargi, six tailles) | seuil | $10^{-12}$ | 1e-12 | `M2_plateau/M_tests_summary.csv : seuil` |
| Application directe de $V_\text{ed}$, $N\times N$ | valeur | $\le 3.3\times10^{-14}$~eV | L 3.3e-14 ; NL 8.1e-15 | `M2_plateau/M_tests_summary.csv : valeur [porte A.2 : ΔV appliqué aux états de Bloch purs contre M2/N_cells, 8 fichiers grossiers (N = 5x5, 6x6, 7x7, 8x8, 9x9, 9x9 (128 b), 10x10, 12x12)] (max de L et NL)` |
| Application directe de $V_\text{ed}$, $N\times N$ | seuil | $10^{-6}$~eV | 1e-6 eV | `M2_plateau/M_tests_summary.csv : seuil` |
| \quad grilles élargies | valeur | $\le 1.2\times10^{-8}$~eV | L 1.2e-08 ; NL 4.0e-09 | `M2_plateau/M_tests_summary.csv : valeur [porte A.2 : ΔV appliqué aux états de Bloch purs contre M2/N_cells, 6 fichiers denses (N = 5x5, 6x6, 7x7, 8x8, 9x9, 12x12)] (max de L et NL)` |
| \quad grilles élargies | seuil | $10^{-6}$~eV | 1e-6 eV | `M2_plateau/M_tests_summary.csv : seuil` |
| Remplissage, coefficients coïncidents | valeur | $1.3\times10^{-15}$ | 1.3e-15 | `M2_plateau/M_tests_summary.csv : valeur [padding : noyau dense à p=1 vs noyau N×N, 9x9]` |
| Remplissage, coefficients coïncidents | seuil | $10^{-10}$ | 1e-10 | `M2_plateau/M_tests_summary.csv : seuil [padding : noyau dense à p=1 vs noyau N×N, 9x9]` |
| Remplissage, points $\kv$ communs | valeur | $1.3\times10^{-3}$ | 0.0013 | `M2_plateau/M_tests_summary.csv : valeur [padding : k coïncidents, bandes 1–15, 9x9]` |
| Remplissage, points $\kv$ communs | seuil | $2\times10^{-3}$ | 2e-3 (tolérance nscf) | `M2_plateau/M_tests_summary.csv : seuil [padding : k coïncidents, bandes 1–15, 9x9]` |
| Fourier $\kv\to\Rv\to\kv$ | valeur | $2.4\times10^{-14}$ | 2.4e-14 | `M2_plateau/M_tests_summary.csv : valeur [fermeture Fourier Wannier (k → R → k), 9x9]` |
| Fourier $\kv\to\Rv\to\kv$ | seuil | $10^{-12}$ | 1e-12 | `M2_plateau/M_tests_summary.csv : seuil [fermeture Fourier Wannier (k → R → k), 9x9]` |
| Bloch$\to$Wannier$\to$Bloch | valeur | $1.3\times10^{-15}$ | 1.3e-15 | `M2_plateau/M_tests_summary.csv : valeur [fermeture Bloch → Wannier → Bloch (5 bandes), 9x9]` |
| Bloch$\to$Wannier$\to$Bloch | seuil | $10^{-12}$ | 1e-12 | `M2_plateau/M_tests_summary.csv : seuil [fermeture Bloch → Wannier → Bloch (5 bandes), 9x9]` |
| Convention intensive, $N = 6, 9, 12$ | valeur | $2.3\times10^{-2}$ | 0.023 | `M2_plateau/M_tests_summary.csv : valeur [convention intensive (cellule unitaire), famille 3m (N = 6, 9, 12)]` |
| Convention intensive, $N = 6, 9, 12$ | seuil | $5\times10^{-2}$ | 5e-2 | `M2_plateau/M_tests_summary.csv : seuil` |
| \quad $N = 5, 7, 8$ | valeur | $2.1\times10^{-2}$ | 0.021 | `M2_plateau/M_tests_summary.csv : valeur [convention intensive (cellule unitaire), famille non-3m (N = 5, 7, 8)]` |
| \quad $N = 5, 7, 8$ | seuil | $5\times10^{-2}$ | 5e-2 | `M2_plateau/M_tests_summary.csv : seuil` |

## `tab:convergence_gamma` — `tables/convergence_gamma.tex` (§4.2.5 → annexe D)

- Médiane de Γ N_cells (meV), grille de sortie 240², η = 0.02 eV, grille interne 300², fenêtre ±3 eV ; colonne R_cut = 4 remplie pour les six tailles (TODO). Contrôle : R_cut 3 = `level2_summary.csv`.

| ligne | colonne | affiché | valeur lue | source |
|---|---|---|---|---|
| 6 | R_cut 0 | 3011 | 3011.1803 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [6x6, R_cut = 0, 240, 0.02]` |
| 6 | R_cut 1 | 3243 | 3242.6703 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [6x6, R_cut = 1, 240, 0.02]` |
| 6 | R_cut 2 | 3186 | 3186.3363 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [6x6, R_cut = 2, 240, 0.02]` |
| 6 | R_cut 3 | 3149 | 3149.15 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [6x6, R_cut = 3, 240, 0.02]` |
| 6 | R_cut 4 | 3161 | 3161.1535 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [6x6, R_cut = 4, 240, 0.02]` |
| 9 | R_cut 0 | 3014 | 3013.9562 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [9x9, R_cut = 0, 240, 0.02]` |
| 9 | R_cut 1 | 3273 | 3273.2515 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [9x9, R_cut = 1, 240, 0.02]` |
| 9 | R_cut 2 | 3222 | 3222.0766 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [9x9, R_cut = 2, 240, 0.02]` |
| 9 | R_cut 3 | 3189 | 3189.0136 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [9x9, R_cut = 3, 240, 0.02]` |
| 9 | R_cut 4 | 3200 | 3199.9967 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [9x9, R_cut = 4, 240, 0.02]` |
| 12 | R_cut 0 | 3017 | 3016.8913 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [12x12, R_cut = 0, 240, 0.02]` |
| 12 | R_cut 1 | 3299 | 3299.453 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [12x12, R_cut = 1, 240, 0.02]` |
| 12 | R_cut 2 | 3269 | 3268.5115 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [12x12, R_cut = 2, 240, 0.02]` |
| 12 | R_cut 3 | 3265 | 3264.506 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [12x12, R_cut = 3, 240, 0.02]` |
| 12 | R_cut 4 | 3283 | 3283.1683 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [12x12, R_cut = 4, 240, 0.02]` |
| 5 | R_cut 0 | 2936 | 2936.1437 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [5x5, R_cut = 0, 240, 0.02]` |
| 5 | R_cut 1 | 2966 | 2966.1883 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [5x5, R_cut = 1, 240, 0.02]` |
| 5 | R_cut 2 | 2968 | 2967.5634 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [5x5, R_cut = 2, 240, 0.02]` |
| 5 | R_cut 3 | 2997 | 2997.1354 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [5x5, R_cut = 3, 240, 0.02]` |
| 5 | R_cut 4 | 2997 | 2997.073 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [5x5, R_cut = 4, 240, 0.02]` |
| 7 | R_cut 0 | 2929 | 2929.2014 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [7x7, R_cut = 0, 240, 0.02]` |
| 7 | R_cut 1 | 2948 | 2947.951 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [7x7, R_cut = 1, 240, 0.02]` |
| 7 | R_cut 2 | 2946 | 2946.2803 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [7x7, R_cut = 2, 240, 0.02]` |
| 7 | R_cut 3 | 2943 | 2942.8454 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [7x7, R_cut = 3, 240, 0.02]` |
| 7 | R_cut 4 | 2953 | 2953.2845 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [7x7, R_cut = 4, 240, 0.02]` |
| 8 | R_cut 0 | 2939 | 2939.0479 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [8x8, R_cut = 0, 240, 0.02]` |
| 8 | R_cut 1 | 2991 | 2991.2716 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [8x8, R_cut = 1, 240, 0.02]` |
| 8 | R_cut 2 | 2976 | 2976.2448 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [8x8, R_cut = 2, 240, 0.02]` |
| 8 | R_cut 3 | 2974 | 2974.1813 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [8x8, R_cut = 3, 240, 0.02]` |
| 8 | R_cut 4 | 2991 | 2991.2441 | `M2_plateau/level1_summary.csv : median_Gamma_Ncells_meV [8x8, R_cut = 4, 240, 0.02]` |

## `tab:tests_T` — `tables/tests_T.tex` (§4.2.5 → annexe D)

- Lignes 6×6, 12×12 (non rejoués avec M2) et grille d'énergie (v1 seulement) retirées (TODO).
- Ligne « Hermiticité de M_loc » retirée (décision du 2026-10-01) : l'hermiticité de M est déjà dans tab:tests_M et aucune valeur de la 9×9 de production n'existe hors des journaux.
- Positivité : minimum réel sur les 41 266 états de la fenêtre (9×9 de production) au lieu de « ≥ 0 ».

| ligne | colonne | affiché | valeur lue | source |
|---|---|---|---|---|
| Référence, $5\times5$ | valeur | $1.8\times10^{-13}$ | 1.8e-13 | `M2_plateau/M_tests_summary.csv : valeur [test d'or (local vs compute_T), 5×5 dense]` |
| Référence, $5\times5$ | seuil | $10^{-8}$ | 1e-08 | `M2_plateau/M_tests_summary.csv : seuil` |
| Grille interne, $300^2\to600^2$ | valeur | $9.1\times10^{-4}$ | 0.0009144248278094638 | `M2_plateau/nkint_check_9x9.csv : \|medG[300] − medG[600]\| / medG[600]` |
| Positivité | valeur | $1.96$~eV | 1.955186878025845 | `M2_plateau/resonance_9x9.npz : min de G_T sur \|E_out − E_D\| ≤ 3.0 eV (eV)` |
| Positivité | seuil | $-10^{-8}$~eV | -1e-8 | `ch4/NOTES_TGAMMA.md : l. 122 (C7)` |

## `tab:kaasbjerg` — `tables/kaasbjerg.tex` (§4.2.5, corps)

- Colonne Kaasbjerg : Fig. 13 et 14 de l'article numérisées dans `r8_7a_results.json` (Fig. 13 : courbes vectorielles du PDF interpolées au meV ; Fig. 14 : points sur des cellules de 10 meV). Seule cellule sans source lisible par machine : A_cell|M| ~70 eV Å², lu sur sa Fig. 3.
- Nos colonnes (9×9, R_cut 3, η_t = 20 meV, N_k^int = 900) : ρ − ρ₀ sur la grille 600² avec η_G = 50 meV (`r8_dos_results.json`) ; A_K avec η_G = 25 meV (`r8_spec_results.json`) ; A_cell|M_nn| = moyenne sur un disque de 0.147 Å⁻¹ autour de K, état initial K + δx̂ (δ = 0.029 Å⁻¹), 512 points (`r10_c2_results.json` : kaasbjerg.meta). Nos DOS sont par spin : hauteur × 2 (spin compté, comme Kaasbjerg) ; unité : états/eV/maille. c = défauts par maille (convention de Kaasbjerg). A_cell|M_nn| : π / π* (valence / conduction), à dire dans la légende.
- Nos positions tombent sur la grille d'énergie de pas 2.5 meV : quatre décimales (−0.1625 arrondi à trois décimales est ambigu). Kaasbjerg : trois décimales (lecture au meV).
- Contrôles : positions de `r8_fig_results.json` (superposition_7b) = `r8_dos_results.json` ; pos_K = `r8_7a_results.json` ; C_N, η_t, η_G et N_k^int attendus.

| ligne | colonne | affiché | valeur lue | source |
|---|---|---|---|---|
| $A_\text{cell}\|M_{nn}\|$ près de $K$ (eV\,\AA$^2$) | Kaasbjerg | ${\sim}70$ | ~70 | `lit. : Kaasbjerg 2020 (PRB 101, 045433), Fig. 3, lu sur la figure (défauts.tex l. 327), aucune donnée numérisée` |
| $A_\text{cell}\|M_{nn}\|$ près de $K$ (eV\,\AA$^2$) | non aligné | 77 / 78 | 76.956 / 78.168 | `kaasbjerg/r10_c2_results.json : kaasbjerg.D1.tel quel.{valence, conduction} \| K.mean` |
| $A_\text{cell}\|M_{nn}\|$ près de $K$ (eV\,\AA$^2$) | Kumagai–Oba | 82 / 83 | 81.605 / 82.821 | `kaasbjerg/r10_c2_results.json : kaasbjerg.D1.plateau.{valence, conduction} \| K.mean` |
| Maximum de $\rho-\rho_0$ (eV), $c = 0.1~\%$ | Kaasbjerg | $-0.200$ | -0.2 | `kaasbjerg/r8_7a_results.json : fig13_metrics.0.1.drho_max_pos_eV` |
| Maximum de $\rho-\rho_0$ (eV), $c = 0.1~\%$ | non aligné | $-0.1625$ | -0.1624999999995529 | `kaasbjerg/r8_dos_results.json : metrics.tel_quel_600_c0.001.drho_max_pos_eV` |
| Maximum de $\rho-\rho_0$ (eV), $c = 0.1~\%$ | Kumagai–Oba | $-0.1475$ | -0.14749999999955055 | `kaasbjerg/r8_dos_results.json : metrics.aligne_600_c0.001.drho_max_pos_eV` |
| \quad $c = 1~\%$ | Kaasbjerg | $-0.210$ | -0.21 | `kaasbjerg/r8_7a_results.json : fig13_metrics.1.0.drho_max_pos_eV` |
| \quad $c = 1~\%$ | non aligné | $-0.1650$ | -0.16499999999955328 | `kaasbjerg/r8_dos_results.json : metrics.tel_quel_600_c0.01.drho_max_pos_eV` |
| \quad $c = 1~\%$ | Kumagai–Oba | $-0.1500$ | -0.14999999999955094 | `kaasbjerg/r8_dos_results.json : metrics.aligne_600_c0.01.drho_max_pos_eV` |
| Hauteur, $c = 1~\%$ (eV$^{-1}$) | Kaasbjerg | $0.031$ | 0.030746893024432773 | `kaasbjerg/r8_7a_results.json : fig13_metrics.1.0.drho_max` |
| Hauteur, $c = 1~\%$ (eV$^{-1}$) | non aligné | $0.054$ | 0.05352573830058177 | `kaasbjerg/r8_dos_results.json : metrics.tel_quel_600_c0.01.drho_max × 2 (spin)` |
| Hauteur, $c = 1~\%$ (eV$^{-1}$) | Kumagai–Oba | $0.058$ | 0.05817516839179859 | `kaasbjerg/r8_dos_results.json : metrics.aligne_600_c0.01.drho_max × 2 (spin)` |
| Largeur à mi-hauteur, $c = 1~\%$ (eV) | Kaasbjerg | $0.31$ | 0.30635758813655406 | `kaasbjerg/r8_7a_results.json : fig13_metrics.1.0.drho_fwhm_eV` |
| Largeur à mi-hauteur, $c = 1~\%$ (eV) | non aligné | $0.20$ | 0.20124621847661056 | `kaasbjerg/r8_dos_results.json : metrics.tel_quel_600_c0.01.drho_fwhm_eV` |
| Largeur à mi-hauteur, $c = 1~\%$ (eV) | Kumagai–Oba | $0.19$ | 0.1870328301810967 | `kaasbjerg/r8_dos_results.json : metrics.aligne_600_c0.01.drho_fwhm_eV` |
| Écart des maxima de $A_K$, $c = 1~\%$ (eV) | Kaasbjerg | $0.100$ | 0.10000404720303457 | `kaasbjerg/r8_7a_results.json : fig14.1.0.K_gap_eV` |
| Écart des maxima de $A_K$, $c = 1~\%$ (eV) | non aligné | $0.118$ | 0.11762346994893341 | `kaasbjerg/r8_spec_results.json : runs.tel_quel_c0.01.K_gap_eV` |
| Écart des maxima de $A_K$, $c = 1~\%$ (eV) | Kumagai–Oba | $0.118$ | 0.11824139676128233 | `kaasbjerg/r8_spec_results.json : runs.aligne_c0.01.K_gap_eV` |

## `tab:grille_interne` — `tables/grille_interne.tex` (§4.2.5 → annexe D (chaîne T))

- 9×9 de production (Kumagai–Oba), R_cut 3, grille de sortie 240², η = 20 meV. Fenêtre ±3 eV : 41 266 états ; zone |ε − E_D| ≤ 0.3 eV : 280 états (`z_n`) ; Γ(E_D) : les 4 états au point de Dirac (`n_ED`). Contrôle : 300² = production (`level1_summary.csv`).
- E_res = argmax de Γ sur les états à ±1.5 eV : grandeur **retirée du ch. 4 par la décision R10 B.1** (argmax discret sur les états de la grille de sortie), remise ici à la demande de G (2026-10-01) ; à confirmer à la rédaction de l'annexe D. E_res = z_E_res dans le csv.

| ligne | colonne | affiché | valeur lue | source |
|---|---|---|---|---|
| $150^2$ | médiane ±3 eV (meV) | 3210 | 3210.0181762526818 | `M2_plateau/nkint_check_9x9.csv : medG [nk_int = 150]` |
| $150^2$ | médiane ±0.3 eV (meV) | 4289 | 4288.842027638511 | `M2_plateau/nkint_check_9x9.csv : z_medG [nk_int = 150]` |
| $150^2$ | Γ N_cells(E_D) (meV) | 5662 | 5662.157507923787 | `M2_plateau/nkint_check_9x9.csv : G_ED [nk_int = 150]` |
| $150^2$ | E_res − E_D (eV) | $-0.238$ | -0.23822954795906082 | `M2_plateau/nkint_check_9x9.csv : E_res [nk_int = 150]` |
| $300^2$ | médiane ±3 eV (meV) | 3189 | 3189.013588325133 | `M2_plateau/nkint_check_9x9.csv : medG [nk_int = 300]` |
| $300^2$ | médiane ±0.3 eV (meV) | 3045 | 3045.276268611333 | `M2_plateau/nkint_check_9x9.csv : z_medG [nk_int = 300]` |
| $300^2$ | Γ N_cells(E_D) (meV) | 4287 | 4287.112828533603 | `M2_plateau/nkint_check_9x9.csv : G_ED [nk_int = 300]` |
| $300^2$ | E_res − E_D (eV) | $-0.175$ | -0.17484882850105077 | `M2_plateau/nkint_check_9x9.csv : E_res [nk_int = 300]` |
| $450^2$ | médiane ±3 eV (meV) | 3196 | 3196.1099873995636 | `M2_plateau/nkint_check_9x9.csv : medG [nk_int = 450]` |
| $450^2$ | médiane ±0.3 eV (meV) | 3080 | 3079.7507187061265 | `M2_plateau/nkint_check_9x9.csv : z_medG [nk_int = 450]` |
| $450^2$ | Γ N_cells(E_D) (meV) | 4120 | 4120.384973749112 | `M2_plateau/nkint_check_9x9.csv : G_ED [nk_int = 450]` |
| $450^2$ | E_res − E_D (eV) | $-0.175$ | -0.17484882850105077 | `M2_plateau/nkint_check_9x9.csv : E_res [nk_int = 450]` |
| $600^2$ | médiane ±3 eV (meV) | 3192 | 3191.9323705334373 | `M2_plateau/nkint_check_9x9.csv : medG [nk_int = 600]` |
| $600^2$ | médiane ±0.3 eV (meV) | 3039 | 3039.0595886407905 | `M2_plateau/nkint_check_9x9.csv : z_medG [nk_int = 600]` |
| $600^2$ | Γ N_cells(E_D) (meV) | 4090 | 4090.1124522968867 | `M2_plateau/nkint_check_9x9.csv : G_ED [nk_int = 600]` |
| $600^2$ | E_res − E_D (eV) | $-0.175$ | -0.17484882850105077 | `M2_plateau/nkint_check_9x9.csv : E_res [nk_int = 600]` |
