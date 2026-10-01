#!/usr/bin/env bash
#SBATCH --job-name=smearing_conv
#SBATCH --account=rrg-cotemich-ac
#SBATCH --ntasks=64
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --time=3:00:00
#SBATCH --output=smearing_conv_%j.log

set -euo pipefail
module restore qe

NCPUS=64

PSEUDO_DIR="/home/gregb26/links/projects/rrg-cotemich-ac/gregb26/abinit_processing/pseudo"
PSEUDO="C.upf"
OUTBASE="/home/gregb26/links/scratch/qe_conv/smearing"

mkdir -p "$OUTBASE"

ECUT=100         # utiliser ecut optimal
ECUTRHO=400      # utiliser 4*ecut
K=27             # utiliser k optimal

echo "smearing    degaus    Etot(Ry)    ACC(Ry)" > smearing.dat

for SMEARING in gaussian mp mv fd; do
    for DEGAUSS in 0.005 0.01 0.02 0.03 0.04 0.05; do

        RUN="smearing_${SMEARING}_dg${DEGAUSS}_e${ECUT}_k${K}"
        OUTDIR="$OUTBASE/$RUN"
        mkdir -p "$OUTDIR"

        cat > ${RUN}.in << EOF

&CONTROL
  calculation = 'scf'
  prefix      = '${SMEARING}_${DEGAUSS}'
  outdir      = '$OUTDIR'
  pseudo_dir  = '$PSEUDO_DIR'
/
&SYSTEM
  ibrav       = 0
  nat         = 2
  ntyp        = 1
  ecutwfc     = $ECUT
  ecutrho     = $ECUTRHO
  occupations = 'smearing'
  smearing    = '$SMEARING'
  degauss     = $DEGAUSS
/
&ELECTRONS
  conv_thr    = 1.d-10
  mixing_beta = 0.3
/
ATOMIC_SPECIES
  C 12.011 $PSEUDO
CELL_PARAMETERS bohr
  4.0354919061  -2.3298923383   0.0
  4.0354919061   2.3298923383   0.0
  0.0            0.0           30.0
ATOMIC_POSITIONS crystal
  C  0.3333333333  0.3333333333  0.0
  C  0.6666666667  0.6666666667  0.0
K_POINTS automatic
  $K $K 1  0 0 0
EOF

        srun -n $NCPUS --cpus-per-task=1 pw.x < ${RUN}.in > ${RUN}.out

        E=$(grep -m1 -E "!\s+total energy" ${RUN}.out | awk '{print $(NF-1)}')
        ACC=$(grep -E "estimated scf accuracy" ${RUN}.out | tail -n 1 | awk '{print $(NF-1)}')

        echo "$SMEARING    $DEGAUSS    $E    $ACC" >> smearing.dat

    done
done

column -t smearing.dat

