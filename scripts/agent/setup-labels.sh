#!/usr/bin/env bash
# shellcheck disable=SC1112  # apostrophes typographiques volontaires dans les descriptions
# Crée (ou met à jour) les labels du cycle agent. À lancer une fois :
#   GH_REPO=delitamakanda/elearning bash scripts/agent/setup-labels.sh
set -euo pipefail

label() {
  gh label create "$1" --color "$2" --description "$3" --force
}

label 'agent:refine'  'c5def5' 'Agent : rédiger une spec à partir de ce ticket'
label 'spec:review'   'fbca04' 'Spec rédigée par l’agent, à valider par un humain'
label 'agent:ready'   '0e8a16' 'Spec validée : l’agent peut implémenter'
label 'agent:working' '1d76db' 'L’agent implémente ce ticket'
label 'agent:review'  '5319e7' 'PR ouverte par l’agent, en attente de revue humaine'
label 'agent:blocked' 'b60205' 'L’agent n’a pas pu terminer — intervention humaine requise'
