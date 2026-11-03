#!/bin/bash
set -euo pipefail
FILE="app.log"

if [ -f "$FILE" ]; then
	echo "$FILE exists, line count: $(wc -l < "$FILE")"
	
	ERRORS=$(grep -c "ERROR" "$FILE" || true)
	if [ "$ERRORS" -gt 2 ]; then
	echo "Pipeline unhealthy"

	else 
	echo "Pipeline healthy"
	fi
else 
	echo "ERROR: $FILE not found" >&2
	exit 1
fi

	
