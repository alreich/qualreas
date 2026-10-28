#!/usr/bin/env bash
# Run from the top of your qualreas clone (the folder that contains src/, docs/, ...).
# Renames top-level folders to lowercase and moves the data folders into data/.
# Uses a two-step git mv so it also works on macOS (case-insensitive filesystem).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

mv2() {   # mv2 OLD NEW : two-step git mv (needed when OLD and NEW differ only in case)
  git mv "$1" "$1.__tmp__"
  mkdir -p "$(dirname "$2")"
  git mv "$1.__tmp__" "$2"
}

mkdir -p data
mv2 Algebras    data/algebras
mv2 Images      data/images
mv2 Networks    data/networks
mv2 Ontologies  data/ontologies
mv2 Misc        misc
mv2 Notebooks   notebooks
mv2 Trash       trash

echo "Moved. Summary of staged changes:"
git status --short | cut -c1-3 | sort | uniq -c || true
echo "Done. Review with 'git status', then commit."
