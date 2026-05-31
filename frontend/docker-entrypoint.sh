#!/bin/sh
set -e

HASH_FILE=/app/node_modules/.install-hash

current_hash=$(node -e "
const crypto = require('crypto');
const fs = require('fs');
process.stdout.write(crypto.createHash('sha1').update(fs.readFileSync('/app/package-lock.json')).digest('hex'));
")

stored_hash=""
if [ -f "$HASH_FILE" ]; then
  stored_hash=$(cat "$HASH_FILE")
fi

if [ "$current_hash" != "$stored_hash" ]; then
  echo "Dependencies changed, running npm ci..."
  npm ci --include=optional
  echo "$current_hash" > "$HASH_FILE"
else
  echo "Dependencies up to date, skipping install."
fi

exec "$@"
