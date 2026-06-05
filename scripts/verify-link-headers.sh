#!/usr/bin/env bash
# verify-link-headers.sh — check that Link rel values are limited to IANA-registered ones.
# Usage: ./scripts/verify-link-headers.sh [BASE_URL]
# Default BASE_URL: https://tkctalent.com

set -euo pipefail

BASE_URL="${1:-https://tkctalent.com}"
ROUTES=("/" "/docs" "/api" "/skills")

ALLOWED_RELS="api-catalog|service-doc"
EXIT_CODE=0

echo "=========================================="
echo " Link header verification"
echo " Base: ${BASE_URL}"
echo "=========================================="
echo ""

for route in "${ROUTES[@]}"; do
  url="${BASE_URL}${route}"
  echo "→ ${url}"

  # Fetch headers; tolerate 404s so we still see Link headers on missing pages
  headers=$(curl -sI "${url}" || true)

  # Extract Link header lines
  link_lines=$(echo "${headers}" | grep -i '^Link:' || true)

  if [ -z "${link_lines}" ]; then
    echo "   No Link header found"
    continue
  fi

  # Show raw Link headers
  echo "${link_lines}" | sed 's/^/   /'

  # Extract every rel=\"…\" value (headers contain escaped quotes)
  rels=$(printf '%s\n' "${link_lines}" | grep -oE 'rel=\\"[^\\"]+\\"' | sed 's/rel=\\"//;s/\\"$//' | sort -u | tr '\n' ' ' || true)

  # Check for disallowed rels
  disallowed=$(printf '%s\n' "${link_lines}" | grep -oE 'rel=\\"[^\\"]+\\"' | sed 's/rel=\\"//;s/\\"$//' | grep -vE "^(${ALLOWED_RELS})$" || true)

  if [ -n "${disallowed}" ]; then
    echo "   ❌ DISALLOWED rels found: ${disallowed}"
    EXIT_CODE=1
  else
    echo "   ✅ All rels allowed: ${rels}"
  fi

  echo ""
done

if [ "${EXIT_CODE}" -eq 0 ]; then
  echo "=========================================="
  echo " ✅ All checked routes are scanner-friendly"
  echo "=========================================="
else
  echo "=========================================="
  echo " ❌ Some routes contain non-IANA rel values"
  echo "=========================================="
fi

exit ${EXIT_CODE}
