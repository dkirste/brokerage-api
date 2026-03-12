#!/usr/bin/env bash
# Generate self-signed certificates for local development only.
# For production, use scripts/init_letsencrypt.sh instead.
set -euo pipefail

CERT_DIR="$(cd "$(dirname "$0")/.." && pwd)/certs"
mkdir -p "$CERT_DIR"

DOMAIN="${1:-localhost}"

openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout "$CERT_DIR/server.key" \
  -out "$CERT_DIR/server.crt" \
  -subj "/C=US/ST=Local/L=Local/O=Dev/CN=$DOMAIN" \
  -addext "subjectAltName=DNS:$DOMAIN"

echo "Self-signed certificates generated in $CERT_DIR"
