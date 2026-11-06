#!/bin/bash
set -euo pipefail

JOB_ID="${1:?Usage: healthcheck.sh <job_id>}"

RESULT=$(databricks jobs list-runs --job-id "$JOB_ID" --limit 1 --output json \
  | jq -r '(.runs // .)[0].state.result_state // "UNKNOWN"')

echo "$(date '+%F %T') job=$JOB_ID latest_result=$RESULT"

if [ "$RESULT" = "SUCCESS" ]; then
    echo "Pipeline healthy"
else
    echo "Pipeline unhealthy" >&2
    exit 1
fi	
