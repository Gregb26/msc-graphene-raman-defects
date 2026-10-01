#!/bin/bash
#SBATCH --account=rrg-cotemich-ac
#SBATCH --job-name=wann_7x7
#SBATCH --ntasks=64
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --time=00-03:00
#SBATCH --output=wann_7x7_%j.out
#SBATCH --error=wann_7x7_%j.err
module restore qe
export OMP_NUM_THREADS=1
cd /home/gregb26/links/projects/rrg-cotemich-ac/gregb26/graphene/qe/defects/unit_cell/7x7 || exit 1
set -e
srun pw.x < scf.in  > scf.out
srun pw.x < nscf.in > nscf.out
srun -n 1 wannier90.x -pp wannier
srun -n 1 pw2wannier90.x < pw2wann.in > pw2wann.out
srun -n 1 wannier90.x wannier
echo "DONE 7x7"
