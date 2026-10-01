#!/usr/bin/env bash
#SBATCH --job-name=ecut_cross_conv
#SBATCH --account=rrg-cotemich-ac
#SBATCH --nodes=1
#SBATCH --ntasks=128
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --time=02:00:00
#SBATCH --output=ecut_conv_%j.log

set -euo pipefail # fails if there is one error
module restore qe

NCPUS=128 # number of CPUs to use for the runs

# Set variables related to directories
PSEUDO_DIR="/home/gregb26/links/projects/rrg-cotemich-ac/gregb26/abinit_processing/pseudo" # directory containing pseudo potentials
PSEUDO="C.upf" # name of pseudo potential
OUTBASE="/home/gregb26/links/scratch/qe_conv" # parent directory of outdir

mkdir -p "$OUTBASE" # make OUTBASE directory

K1=24; K2=24; K3=1 # use optimal kpoint grid 
DEGAUSS=0.02 # set degauss variable

echo "ecut(Ry)  Etot(Ry)       ACC(Ry)" > ecut_cross.dat # write columns ecut Etot and Accuracy in a file named ecut_scf.dat, will be created automatically

for ECUT in 40 50 60 70 80 90 100 110 120 130; do # loop over desired values of ecut for convergence test
  
  ECUTRHO=$((ECUT*4)) # set ecutrho based on ecutwfc

  RUN="ecut_${ECUT}_k${K1}" # create run name variable
  OUTDIR="$OUTBASE/$RUN"    # outdir variable
  mkdir -p "$OUTDIR"        # make outdir directory

  # now create input files, with its name based on the run
  # everything bewteen the EOF's will be written
  # everything with a $ sign references a variable previously defined
  cat > ${RUN}.in << EOF 

&CONTROL
  calculation = 'scf'
  prefix      = 'ecut_${ECUT}'
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
  smearing    = 'mv'
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
  $K1 $K2 $K3  0 0 0
EOF
	
  # Run the scripts	
  srun -n $NCPUS --cpus-per-task=1 pw.x < ${RUN}.in > ${RUN}.out

  # Extract total energy and accuracy of the run
  E=$(grep -m1 -E "!\s+total energy" ${RUN}.out | awk '{print $(NF-1)}')
  ACC=$(grep -E "estimated scf accuracy" ${RUN}.out | tail -n 1 | awk '{print $(NF-1)}')
 
  # Write total energy and accuracy of the run in the ecut_scf.dat file 
  echo "$ECUT  $E  $ACC" >> ecut_cross.dat

done

# read the columns of the ecut_scf.dat file for a summary of the convergence
column -t ecut_cross.dat
