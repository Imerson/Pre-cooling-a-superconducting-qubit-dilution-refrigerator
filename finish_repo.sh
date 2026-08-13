#!/bin/bash
# ============================================================================
# finish_repo.sh — run this ON YOUR MAC (Terminal) from the repo root:
#   cd "<this folder>" && bash finish_repo.sh
#
# It copies the OpenFOAM case trees (0/, constant/ minus polyMesh, system/,
# postProcessing/) from the dissertation model folders into this repo.
# macOS downloads OneDrive cloud-only files automatically on access, so no
# manual hydration is needed — just let it run (first run may be slow).
#
# It then commits everything and pushes to GitHub.
# ============================================================================
set -e

BASE="$HOME/Library/CloudStorage/OneDrive-Personal/Documents/Education Hub/15-Energy Systems/4-Year 3/4-Dissertation/2-Model"
REPO="$(cd "$(dirname "$0")" && pwd)"

copy_case () {   # $1 = source case dir, $2 = destination dir in repo
  local SRC="$1" DST="$2"
  echo ">> $SRC -> $DST"
  mkdir -p "$DST"
  rsync -a --no-perms \
    --exclude 'polyMesh/' --exclude '.DS_Store' --exclude '._*' \
    "$SRC/0" "$SRC/constant" "$SRC/system" "$DST/" 2>/dev/null || true
  [ -d "$SRC/postProcessing" ] && rsync -a --no-perms --exclude '.DS_Store' \
    "$SRC/postProcessing" "$DST/" 2>/dev/null || true
}

# --- enclosure CHT cases ---------------------------------------------------
for c in stage1_shield_50K_v2 stage1_shield_77K_v2 \
         stage2_4K_from50K_v2 stage2_4K_from77K_v2; do
  copy_case "$BASE/1-CHT models/$c" "$REPO/enclosure_CHT/$c"
done

# --- cold-plate heat-exchanger cases ---------------------------------------
HX="$BASE/2-Stage 1 Heat exchanger"
copy_case "$HX/Buoyancy_50K_Microchannel_Re2300" \
          "$REPO/cold_plate_HX/Buoyancy_50K_Microchannel_Re2300"
copy_case "$HX/stage1_microchannel_LN2_77K_Re2300" \
          "$REPO/cold_plate_HX/stage1_microchannel_LN2_77K_Re2300"

echo ""
echo ">> Case trees copied. Repo size:"
du -sh "$REPO"

# --- git -------------------------------------------------------------------
cd "$REPO"
# Clean stale lock/temp files left by the initial commit (made in a sandbox
# that could not delete files).
rm -f .git/*.lock .git/objects/maintenance.lock
find .git/objects -name 'tmp_obj_*' -delete 2>/dev/null || true
git add -A
git commit -m "Add OpenFOAM case trees (0/, constant/, system/, postProcessing/)" || true
git push -u origin main

echo ""
echo "Done. Check https://github.com/Imerson/Pre-cooling-a-superconducting-qubit-dilution-refrigerator"
