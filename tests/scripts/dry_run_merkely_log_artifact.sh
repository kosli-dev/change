#!/bin/bash

export ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

MERKELY_COMMAND=log_artifact
MERKELY_DOCKER_IMAGE=python:3.7-alpine
MERKELY_IS_COMPLIANT=TRUE
MERKELY_ARTIFACT_GIT_URL=https://github/me/project/commit/abc50c8a53f79974d615df335669b59fb56a4ed3
MERKELY_ARTIFACT_GIT_COMMIT=abc50c8a53f79974d615df335669b59fb56a4ed3
MERKELY_CI_BUILD_URL=https://gitlab/build/1456
MERKELY_CI_BUILD_NUMBER=23
MERKELY_API_TOKEN=5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4

function merkely_log_artifact()
{
  local -r MERKELYPIPE="${1}"
  docker run \
        --interactive \
        --tty \
        --env CDB_DRY_RUN=TRUE \
        --env MERKELY_COMMAND=log_artifact \
        \
        --env MERKELY_FINGERPRINT="docker://${MERKELY_DOCKER_IMAGE}" \
        --env MERKELY_IS_COMPLIANT=${MERKELY_IS_COMPLIANT} \
        --env MERKELY_ARTIFACT_GIT_URL=${MERKELY_ARTIFACT_GIT_URL} \
        --env MERKELY_ARTIFACT_GIT_COMMIT=${MERKELY_ARTIFACT_GIT_COMMIT} \
        --env MERKELY_CI_BUILD_URL=${MERKELY_CI_BUILD_URL} \
        --env MERKELY_CI_BUILD_NUMBER=${MERKELY_CI_BUILD_NUMBER} \
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