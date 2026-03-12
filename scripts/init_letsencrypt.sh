#!/usr/bin/env bash
set -euo pipefail

DOMAIN="ip213-165-72-53.pbiaas.com"
EMAIL="${CERTBOT_EMAIL:-admin@example.com}"

echo "==> Creating dummy certificate so nginx can start..."
docker compose run --rm --entrypoint "" certbot sh -c "
  mkdir -p /etc/letsencrypt/live/$DOMAIN &&
  openssl req -x509 -nodes -days 1 -newkey rsa:2048 \
    -keyout /etc/letsencrypt/live/$DOMAIN/privkey.pem \
    -out /etc/letsencrypt/live/$DOMAIN/fullchain.pem \
    -subj '/CN=localhost'
"

echo "==> Starting nginx..."
docker compose up -d nginx

echo "==> Requesting real certificate from Let's Encrypt..."
docker compose run --rm --entrypoint "" certbot \
  certbot certonly --webroot -w /var/www/certbot \
  -d "$DOMAIN" \
  --email "$EMAIL" \
  --agree-tos --non-interactive --force-renewal

echo "==> Reloading nginx with real certificate..."
docker compose exec nginx nginx -s reload

echo "==> Done! SSL certificate issued for $DOMAIN"
