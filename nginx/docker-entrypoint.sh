#!/bin/sh
set -e

apk add --no-cache openssl >/dev/null 2>&1 || true

DOMAIN="${DOMAIN:-brokerage-api.hopto.org}"
CERT_PATH="/etc/letsencrypt/live/$DOMAIN"

# If no real Let's Encrypt certificate exists yet, create a temporary self-signed
# one so nginx can start and serve ACME challenges on port 80.
if [ ! -f "$CERT_PATH/fullchain.pem" ]; then
  echo "==> No certificate found for $DOMAIN — generating temporary self-signed cert..."
  mkdir -p "$CERT_PATH"
  openssl req -x509 -nodes -days 1 -newkey rsa:2048 \
    -keyout "$CERT_PATH/privkey.pem" \
    -out "$CERT_PATH/fullchain.pem" \
    -subj "/CN=$DOMAIN" 2>/dev/null
  echo "==> Temporary certificate created. Certbot will replace it with a real one."
fi

# Background process: reload nginx to pick up new/renewed certificates.
# First reload after 30s (to pick up initial cert from certbot), then every 6h.
(
  sleep 30
  echo "==> Reloading nginx to pick up new certificate..."
  nginx -s reload 2>/dev/null || true
  while :; do
    sleep 6h
    echo "==> Reloading nginx to pick up renewed certificates..."
    nginx -s reload 2>/dev/null || true
  done
) &

echo "==> Starting nginx..."
exec nginx -g "daemon off;"
