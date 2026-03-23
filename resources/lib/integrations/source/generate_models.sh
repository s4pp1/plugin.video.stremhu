#!/usr/bin/env bash
set -euo pipefail

SPEC_URL="http://localhost:3000/api/docs/kodi-json"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}"
while [ ! -f "${PROJECT_ROOT}/environment.yaml" ] && [ "${PROJECT_ROOT}" != "/" ]; do
  PROJECT_ROOT="$(dirname "${PROJECT_ROOT}")"
done
OUTPUT_PATH="${SCRIPT_DIR}/models.py"
PYTHON_BIN="${PROJECT_ROOT}/.conda/bin/python"

if [ ! -f "${PYTHON_BIN}" ]; then
  echo "Hiba: A .conda környezet nem található a ${PROJECT_ROOT} könyvtárban." >&2
  echo "Hozd létre a környezetet manuálisan:" >&2
  echo "conda env create -p ./.conda -f environment.yaml" >&2
  exit 1
fi

mkdir -p "$(dirname "${OUTPUT_PATH}")"

"${PYTHON_BIN}" -m datamodel_code_generator \
  --url "${SPEC_URL}" \
  --input-file-type openapi \
  --output "${OUTPUT_PATH}" \
  --target-python-version 3.8 \
  --output-model-type dataclasses.dataclass \
  --disable-timestamp \
  --reuse-model \
  --openapi-scopes schemas parameters paths \
  --use-operation-id-as-name

echo "Modellek generalva: ${OUTPUT_FILE}"
