#!/usr/bin/env bash
#SBATCH --job-name=kpoint_conv
#SBATCH --account=rrg-cotemich-ac
#SBATCH --nodes=1
#SBATCH --ntasks=128
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --time=02:00:00
#SBATCH --output=kpoint_conv_%j.log

set -euo pipefail # fails if there is one error
module restore qe

NCPUS=128 # number of CPUs to use during the runs

# set variables related to directories
PSEUDO_DIR="/home/gregb26/links/projects/rrg-cotemich-ac/gregb26/abinit_processing/pseudo" # directory containing pseudopotential file
PSEUDO="C.upf" # name of pseudopotential
OUTBASE="/home/gregb26/links/scratch/qe_conv/kpoint" # parent directory of outdir

mkdir -p "$OUTBASE" # make outbase directory

ECUT=100 # set ecut, determined in early convergence test
ECUTRHO=400 # set ecutrho based on ecut, 4*ecut is recommended
DEGAUSS=0.02 # set degauss 

echo "K Etot(Ry)   ACC(Ry)" > kpoint.dat # write columns K Etot and ACC in a file named kpoint_scf.dat, will make the file automatically

for K in 9 12 15 18 21 24 27 30 33 36 39 42; do # loop over desired kpoint grid
  
  RUN="kpoint_${K}_e${ECUT}" # run name variable
  OUTDIR="$OUTBASE/$RUN" # outdir
  
  mkdir -p "$OUTDIR" # make outdir directory
  
  # now create input files, with its name based on the run
  # everything bewteen the EOF's will be written
  # everything with a $ sign references a variable previously defined	
  cat > ${RUN}.in << EOF 

&CONTROL
  calculation = 'scf'
  prefix      = 'kpoint'
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
  $K $K 1  0 0 0
EOF
  
  # run the scripts
  srun -n $NCPUS --cpus-per-task=1 pw.x < ${RUN}.in > ${RUN}.out

  E=$(grep -m1 -E "!\s+total energy" ${RUN}.out | awk '{print $(NF-1)}')
  ACC=$(grep -E "estimated scf accuracy" ${RUN}.out | tail -n 1 | awk '{print $(NF-1)}')
  
  # write total energy and accuracy of the run in kpoint_scf.dat file 
  echo "$K $E $ACC" >> kpoint.dat

done

# read columns of kpoint_scf.dat file for a summary of the convergence
column -t kpoint.dat
