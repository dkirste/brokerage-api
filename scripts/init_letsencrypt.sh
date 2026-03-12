#!/usr/bin/env bash
set -euo pipefail

DOMAIN="${DOMAIN:-ip213-165-72-53.pbiaas.com}"
EMAIL="${CERTBOT_EMAIL:-admin@example.com}"

echo "==> Starting services (nginx will create a temporary self-signed cert if needed)..."
docker compose up -d

echo "==> Waiting for nginx to be ready..."
until curl -sf -o /dev/null http://localhost/.well-known/acme-challenge/ 2>/dev/null || \
      curl -sf -o /dev/null --insecure https://localhost 2>/dev/null; do
  echo "    waiting..."
  sleep 3
done
echo "==> nginx is ready."

echo "==> Requesting real certificate from Let's Encrypt..."
docker compose run --rm --entrypoint certbot certbot \
  certonly --webroot -w /var/www/certbot \
  -d "$DOMAIN" \
  --email "$EMAIL" \
  --agree-tos --non-interactive --force-renewal

echo "==> Reloading nginx with real certificate..."
docker compose exec nginx nginx -s reload

echo ""
echo "==> Done! SSL certificate issued for $DOMAIN"
echo "==> API available at https://$DOMAIN"
