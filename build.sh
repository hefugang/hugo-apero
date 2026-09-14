#!/usr/bin/env bash
# Build script for Netlify (also works locally).
# Installs an EXTENDED Hugo explicitly so SCSS compiles, then clones the
# hugo-apero theme and builds the site. The theme is fetched at build time,
# so it is never committed to the repository.
set -euo pipefail

V="${HUGO_VERSION:-0.126.1}"

echo "==> Installing Hugo extended ${V}..."
curl -fsSL "https://github.com/gohugoio/hugo/releases/download/v${V}/hugo_extended_${V}_linux-amd64.tar.gz" -o /tmp/hugo.tgz
tar -xzf /tmp/hugo.tgz -C /tmp hugo
chmod +x /tmp/hugo
/tmp/hugo version

echo "==> Cloning hugo-apero theme (latest main)..."
rm -rf themes/hugo-apero
git clone --depth 1 --branch main https://github.com/hugo-apero/hugo-apero.git themes/hugo-apero

# Use Netlify's deploy URL when available, otherwise fall back to "/".
BASEURL="${DEPLOY_PRIME_URL:-${URL:-/}}"
echo "==> Building with baseURL=${BASEURL}"
/tmp/hugo --gc --minify -b "$BASEURL"
