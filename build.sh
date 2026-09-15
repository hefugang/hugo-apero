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

# Canonical site URL: always used for production AND branch deploys so that
# internal links and og:url never fall back to a branch-deploy host such as
# main--pt-ic.netlify.app. Only deploy previews use their own URL.
CANONICAL_URL="https://pt-ic.netlify.app"
if [ "${CONTEXT:-production}" = "deploy-preview" ]; then
  BASEURL="${DEPLOY_PRIME_URL:-$CANONICAL_URL}"
else
  BASEURL="$CANONICAL_URL"
fi
echo "==> Building with baseURL=${BASEURL} (context=${CONTEXT:-production})"
/tmp/hugo --gc --minify -b "$BASEURL"
