#!/bin/bash
# P18 — génère les répertoires EPW de l'étape 2 de la chaîne 24k-24q_mv0.02 à partir de ceux de 24k-24q (mêmes entrées,
# mêmes ressources), liens vers ../epw1/ (jamais selecq.fmt : EPW l'écrase à travers le lien), chemins et commentaires mis à jour.
#   ./_p18_make_step2.sh 2a          : band_freq_interp, epw_g_G, epw_g_K, epw_g_ring (ne dépendent pas de E_D)
#   ./_p18_make_step2.sh 2b <E_D>    : epw2_selfen_{240_T300,240_T10,120_T300}_dg0.02, epw6_phself_K_<nkf>_dg<s> (18), _path_1200_dg0.02, _zoom_1200_dg0.02
set -e
O=/home/gregb26/links/projects/rrg-cotemich-ac/gregb26/graphene/qe/epw/24k-24q
N=/home/gregb26/links/projects/rrg-cotemich-ac/gregb26/graphene/qe/epw/24k-24q_mv0.02
LINKS="crystal.fmt dmedata.fmt epwdata.fmt graphene.epmatwp graphene.save graphene.ukk vmedata.fmt wigner.fmt"
mk() {  # mk <dir> [E_D]
  local d=$1 ed=$2; [ -e "$N/$d" ] && { echo "existe déjà : $N/$d"; return 0; }
  mkdir -p "$N/$d"; for l in $LINKS; do ln -s ../epw1/$l "$N/$d/$l"; done
  for f in "$O/$d"/*.kpt "$O/$d"/G.dat "$O/$d"/K.dat; do [ -f "$f" ] && cp "$f" "$N/$d/"; done
  sed -e '1s/^/! P18 : chaine 24k-24q_mv0.02 (degauss 0.02 Ry), entree identique a 24k-24q sauf fermi_energy = E_D de cette chaine\n/' \
      ${ed:+-e "s/fermi_energy  = -4.2389/fermi_energy  = $ed/"} "$O/$d/epw.in" > "$N/$d/epw.in"
  sed -e "s#/graphene/qe/epw/24k-24q/#/graphene/qe/epw/24k-24q_mv0.02/#g" -e 's/--job-name=\(.*\)/--job-name=\1_mv/' "$O/$d/submit.epw" > "$N/$d/submit.epw"
  echo "créé $d"
}
case "$1" in
  2a) for d in band_freq_interp epw_g_G epw_g_K epw_g_ring; do mk $d; done ;;
  2b) ED=${2:?E_D (eV)}; for d in epw2_selfen_240_T300_dg0.02 epw2_selfen_240_T10_dg0.02 epw2_selfen_120_T300_dg0.02 epw6_phself_path_1200_dg0.02 epw6_phself_zoom_1200_dg0.02; do mk $d $ED; done
      for n in 120 240 480 720 960 1200; do for s in 0.01 0.02 0.05; do mk epw6_phself_K_${n}_dg$s $ED; done; done
      echo "fermi_energy dans les entrées :"; grep -h "fermi_energy" $N/epw2_*/epw.in $N/epw6_*/epw.in | sort | uniq -c ;;
  *) echo "usage: $0 2a | 2b <E_D>"; exit 1 ;;
esac
