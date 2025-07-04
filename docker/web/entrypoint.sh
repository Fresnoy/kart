#!/bin/sh
echo "🛠 ENVIRONNEMENT DE DEBUG"
echo "DATABASE_URL=$DATABASE_URL"
echo "Attente manuelle pour test..."
sleep 10

exec "$@"

