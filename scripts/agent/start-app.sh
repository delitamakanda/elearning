#!/usr/bin/env bash
# Démarre l'app pour les agents (vérification dans le navigateur via le MCP
# Playwright), en arrière-plan :
#   - base SQLite jetable dans .agent-out/ (jamais commitée), migrée puis
#     peuplée avec `manage.py seed_demo` ;
#   - `manage.py runserver` sur :8000 (DEBUG, sans Redis ni Celery : cache
#     factice, e-mails dans la console). Le serveur se recharge à chaque
#     modification de code.
# Attend que l'app réponde. Logs dans .agent-out/runserver.log.
#
# Prérequis : pip install -r requirements.txt
# Les variables exportées par ce script sont aussi écrites dans $GITHUB_ENV
# (si défini) pour que les étapes suivantes utilisent la même base.
set -euo pipefail

out=.agent-out
mkdir -p "$out/playwright"

export DEBUG=True
export SECRET_KEY="${SECRET_KEY:-agent-local-secret}"
export DATABASE_URL="sqlite:///$PWD/$out/agent.sqlite3"
export REDIS_URL=""
if [ -n "${GITHUB_ENV:-}" ]; then
  {
    echo "DEBUG=$DEBUG"
    echo "SECRET_KEY=$SECRET_KEY"
    echo "DATABASE_URL=$DATABASE_URL"
    echo "REDIS_URL="
  } >> "$GITHUB_ENV"
fi

rm -f "$out/agent.sqlite3"
python manage.py migrate --noinput > "$out/migrate.log" 2>&1 || { tail -n 40 "$out/migrate.log"; exit 1; }
python manage.py seed_demo

nohup python manage.py runserver 127.0.0.1:8000 > "$out/runserver.log" 2>&1 < /dev/null &

if ! timeout "${START_TIMEOUT:-120}" bash -c \
  'until curl -sf http://localhost:8000/course/ >/dev/null; do sleep 2; done'; then
  echo "::error::l'app n'a pas démarré à temps"
  tail -n 50 "$out/runserver.log"
  exit 1
fi
echo "App prête : http://localhost:8000/course/ (comptes demo-teacher / demo-student)"
