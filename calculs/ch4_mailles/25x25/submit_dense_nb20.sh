#!/bin/bash
#SBATCH --account=rrg-cotemich-ac
#SBATCH --job-name=dnb20_25
#SBATCH --ntasks=64
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=00-04:00
#SBATCH --output=dense_nb20_25_%j.out
#SBATCH --error=dense_nb20_25_%j.err
module restore qe
export OMP_NUM_THREADS=1
cd /home/gregb26/links/projects/rrg-cotemich-ac/gregb26/graphene/qe/defects/unit_cell/25x25 || exit 1
set -e
srun pw.x < nscf.in > nscf.out
srun -n 1 wannier90.x -pp wannier
srun -n 1 pw2wannier90.x < pw2wann.in > pw2wann.out
srun -n 1 wannier90.x wannier
grep -c "Wannierisation convergence criteria satisfied" wannier.wout || true
module load scipy-stack
cd "${GRAPHENE_RAMAN:-$PROJECTS/graphene-raman}" || exit 1
.venv/bin/python scripts/finalize_wannier.py 25x25
echo "DONE dense nb20 25x25"
