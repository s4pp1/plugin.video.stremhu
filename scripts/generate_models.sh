#!/usr/bin/env bash
set -euo pipefail

SPEC_URL="${1:-http://localhost:3000/api/docs/kodi-json}"
OUTPUT_FILE="${2:-resources/lib/models/stremhu_source_models.py}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUTPUT_PATH="${PROJECT_ROOT}/${OUTPUT_FILE}"

if ! python3 -m datamodel_code_generator --version >/dev/null 2>&1; then
  echo "A datamodel-code-generator nincs telepitve. Telepites:" >&2
  echo "python3 -m pip install --user datamodel-code-generator" >&2
  exit 1
fi

mkdir -p "$(dirname "${OUTPUT_PATH}")"

python3 -m datamodel_code_generator \
  --url "${SPEC_URL}" \
  --input-file-type openapi \
  --output "${OUTPUT_PATH}" \
  --output-model-type dataclasses.dataclass \
  --disable-timestamp \
  --formatters black isort \
  --reuse-model

echo "Modellek generalva: ${OUTPUT_FILE}"
