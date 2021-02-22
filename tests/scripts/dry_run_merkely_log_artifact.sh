#!/bin/bash

export ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

MERKELY_COMMAND=log_artifact
MERKELY_FINGERPRINT=docker://python:3.7-alpine
MERKELY_IS_COMPLIANT=TRUE
MERKELY_API_TOKEN=5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4

BITBUCKET_WORKSPACE=acme
BITBUCKET_REPO_SLUG=road-runner
BITBUCKET_COMMIT=abc50c8a53f79974d615df335669b59fb56a4ed3
BITBUCKET_BUILD_NUMBER=1975

function merkely_log_artifact()
{
  local -r MERKELYPIPE="${1}"
  docker run \
        --interactive \
        --tty \
        --env CDB_DRY_RUN=TRUE \
        --env MERKELY_COMMAND=log_artifact \
        \
        --env MERKELY_FINGERPRINT=${MERKELY_FINGERPRINT} \
        --env MERKELY_IS_COMPLIANT=${MERKELY_IS_COMPLIANT} \
        --env BITBUCKET_WORKSPACE=${BITBUCKET_WORKSPACE} \
        --env BITBUCKET_REPO_SLUG=${BITBUCKET_REPO_SLUG} \
        --env BITBUCKET_COMMIT=${BITBUCKET_COMMIT} \
        --env BITBUCKET_BUILD_NUMBER=${BITBUCKET_BUILD_NUMBER} \
        \
        --env MERKELY_API_TOKEN=${MERKELY_API_TOKEN} \
        --rm \
        --volume=/var/run/docker.sock:/var/run/docker.sock \
        --volume ${MERKELYPIPE}:/Merkelypipe.json \
        merkely/change:master
}

function test_status_non_zero()
{
  local -r expected=144
  merkely_log_artifact "${ROOT_DIR}/Dockerfile"
  status=$?
  echo
  echo "expected STATUS=${expected}"
  echo "  actual STATUS=${status}"
  if [ "${status}" == "${expected}" ]; then
    echo "PASSED"; echo
    true
  else
    echo "FAILED"; echo
    false
  fi
}

function test_status_zero()
{
  local -r expected=0
  merkely_log_artifact "${ROOT_DIR}/tests/data/Merkelypipe.json"
  status=$?
  echo
  echo "expected STATUS=${expected}"
  echo "  actual STATUS=${status}"
  if [ "${status}" == "${expected}" ]; then
    echo "PASSED"; echo
    true
  else
    echo "FAILED"; echo
    false
  fi
}

test_status_zero
test_status_non_zero