#!/usr/bin/env bash
set -euo pipefail

SPEC_URL="http://localhost:4000/api/docs/kodi-json"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_PATH="${SCRIPT_DIR}/models.py"

mkdir -p "$(dirname "${OUTPUT_PATH}")"

conda run -n kodi python -m datamodel_code_generator \
  --url "${SPEC_URL}" \
  --input-file-type openapi \
  --output "${OUTPUT_PATH}" \
  --target-python-version 3.8 \
  --output-model-type dataclasses.dataclass \
  --disable-timestamp \
  --reuse-model \
  --openapi-scopes schemas parameters paths \
  --use-operation-id-as-name

echo "Modellek generalva: ${OUTPUT_PATH}"
