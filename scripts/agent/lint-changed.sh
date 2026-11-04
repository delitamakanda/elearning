#!/usr/bin/env bash
# Ruff (lint + format) sur les seuls fichiers Python modifiés par rapport à la
# branche de base. Le dépôt n'est pas encore entièrement propre (erreurs ruff,
# fichiers non formatés) : on ne bloque l'agent que sur ce qu'il a touché.
#
# Usage : bash scripts/agent/lint-changed.sh [--check|--fix]   (défaut : --check)
# Env   : BASE_REF (défaut : origin/master)
set -euo pipefail

mode="${1:---check}"
base="${BASE_REF:-origin/master}"

mapfile -t files < <(
  {
    git diff --name-only --diff-filter=ACMR "$base" -- 2>/dev/null || true
    git ls-files --others --exclude-standard
  } | sort -u | grep -E '\.py$' | grep -v '/migrations/' || true
)

if [ "${#files[@]}" -eq 0 ]; then
  echo "Aucun fichier Python modifié à vérifier."
  exit 0
fi

printf 'Fichiers vérifiés :\n'
printf '  %s\n' "${files[@]}"

if [ "$mode" = "--fix" ]; then
  ruff check --fix "${files[@]}"
  ruff format "${files[@]}"
else
  ruff check "${files[@]}"
  ruff format --check "${files[@]}"
fi
