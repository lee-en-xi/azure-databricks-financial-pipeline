#!/bin/bash
set -euo pipefail

CATALOG="${CATALOG:-workspace}"
SCHEMA="${SCHEMA:-fin_pipeline}"
SRC_DIR="data/sample_landing"
TARGET="dbfs:/Volumes/${CATALOG}/${SCHEMA}/landing"

shopt -s nullglob
files=("$SRC_DIR"/*.csv)

if [ "${#files[@]}" -eq 0 ]; then
    echo "ERROR: no CSV files in $SRC_DIR. Run the generator first." >&2
    exit 1
fi

for f in "${files[@]}"; do
    echo "Uploading $f"
    databricks fs cp "$f" "$TARGET/" --overwrite
done

echo "Uploaded ${#files[@]} file(s) to $TARGET"
