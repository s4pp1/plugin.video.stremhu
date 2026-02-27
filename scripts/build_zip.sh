#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ADDON_XML="${PROJECT_ROOT}/addon.xml"

if [[ ! -f "${ADDON_XML}" ]]; then
  echo "Hiba: addon.xml nem talalhato: ${ADDON_XML}" >&2
  exit 1
fi

ADDON_HEADER="$(awk '
  BEGIN { in_addon = 0 }
  /<addon([[:space:]]|>)/ { in_addon = 1 }
  in_addon {
    print
    if ($0 ~ />/) {
      exit
    }
  }
' "${ADDON_XML}")"

HEADER_ONE_LINE="$(printf '%s\n' "${ADDON_HEADER}" | tr '\n' ' ')"
ADDON_ID="$(printf '%s\n' "${HEADER_ONE_LINE}" | sed -nE 's/.* id="([^"]+)".*/\1/p')"
ADDON_VERSION="$(printf '%s\n' "${HEADER_ONE_LINE}" | sed -nE 's/.* version="([^"]+)".*/\1/p')"

if [[ -z "${ADDON_ID}" || -z "${ADDON_VERSION}" ]]; then
  echo "Hiba: addon id vagy version nem olvashato az addon.xml-bol." >&2
  exit 1
fi

OUTPUT_DIR="${1:-${PROJECT_ROOT}/dist}"
if [[ "${OUTPUT_DIR}" != /* ]]; then
  OUTPUT_DIR="${PROJECT_ROOT}/${OUTPUT_DIR}"
fi
mkdir -p "${OUTPUT_DIR}"

OUTPUT_ZIP="${OUTPUT_DIR}/${ADDON_ID}-${ADDON_VERSION}.zip"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/${ADDON_ID}.XXXXXX")"
PACKAGE_ROOT="${TMP_DIR}/${ADDON_ID}"

cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

mkdir -p "${PACKAGE_ROOT}"

rsync -a "${PROJECT_ROOT}/" "${PACKAGE_ROOT}/" \
  --exclude '.git/' \
  --exclude '.github/' \
  --exclude '.vscode/' \
  --exclude '.idea/' \
  --exclude '.venv/' \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  --exclude '*.pyo' \
  --exclude '.DS_Store' \
  --exclude 'dist/' \
  --exclude 'scripts/'

(
  cd "${TMP_DIR}"
  zip -r "${OUTPUT_ZIP}" "${ADDON_ID}" >/dev/null
)

echo "ZIP kesz: ${OUTPUT_ZIP}"
