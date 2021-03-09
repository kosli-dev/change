#!/bin/bash

echo_merkelypipe_json()
{
  local -r OWNER="${1}"
  local -r NAME="${2}"
  cat <<- JSON
  {
    "owner": "${OWNER}",
    "name": "${NAME}",
    "description": "Pipeline Controls for Merkely",
    "visibility": "public",
    "template": [
        "artifact",
        "unit_test",
        "integration_test",
        "coverage"
    ]
  }
JSON
}

# use:
#   source ./echo_merkelypipe_json.sh
#   echo_merkelypipe_json merkely "loan calculator"

echo_merkelypipe_json "$@"