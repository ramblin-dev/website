#!/usr/bin/env bash
# Submits all URLs from output/sitemap.xml to IndexNow.
# IndexNow notifies Bing, Yandex, Seznam, Naver, Yep instantly (one shared API).
# Run after `uv run task build`. Safe to re-run; idempotent.
#
# Override via env: HOST, KEY, SITEMAP, ENDPOINT

set -euo pipefail

HOST="${HOST:-ramblin.dev}"
KEY="${KEY:-b6746e9d951fd5f64f1059f04b919e7e94b15f34f85d8d903c73a6eb75c5f0d3}"
SITEMAP="${SITEMAP:-output/sitemap.xml}"
ENDPOINT="${ENDPOINT:-https://api.indexnow.org/IndexNow}"

if [[ ! -f "$SITEMAP" ]]; then
  echo "indexnow-ping: $SITEMAP not found. Run the build first." >&2
  exit 1
fi

mapfile -t URLS < <(grep -oE '<loc>[^<]+</loc>' "$SITEMAP" | sed -E 's|</?loc>||g')

if [[ ${#URLS[@]} -eq 0 ]]; then
  echo "indexnow-ping: no URLs found in $SITEMAP" >&2
  exit 1
fi

PAYLOAD=$(jq -n \
  --arg host "$HOST" \
  --arg key "$KEY" \
  --arg keyloc "https://$HOST/$KEY.txt" \
  --argjson urls "$(printf '%s\n' "${URLS[@]}" | jq -R . | jq -s .)" \
  '{host: $host, key: $key, keyLocation: $keyloc, urlList: $urls}')

echo "indexnow-ping: submitting ${#URLS[@]} URL(s) for $HOST"
HTTP_CODE=$(curl -sS -X POST "$ENDPOINT" \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d "$PAYLOAD" \
  -w '%{http_code}' \
  -o /dev/stderr)

echo
echo "indexnow-ping: HTTP $HTTP_CODE"
if [[ "$HTTP_CODE" != 2* ]]; then
  echo "indexnow-ping: submission failed (expected 2xx)" >&2
  exit 1
fi
