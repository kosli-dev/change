#!/bin/bash

export ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"


MERKELY_COMMAND=log_artifact
MERKELY_DOCKER_IMAGE=acme/road-runner:2.3
MERKELY_IS_COMPLIANT=TRUE
MERKELY_ARTIFACT_GIT_URL=https://github/me/project/commit/abc50c8a53f79974d615df335669b59fb56a4ed3
MERKELY_ARTIFACT_GIT_COMMIT=abc50c8a53f79974d615df335669b59fb56a4ed3
MERKELY_CI_BUILD_URL=https://gitlab/build/1456
MERKELY_CI_BUILD_NUMBER=23
MERKELY_API_TOKEN=5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4

CDB_DRY_RUN=TRUE

docker run \
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
      --volume ${PWD}/${MERKELYPIPE}:/Merkelypipe.json \
      merkely/change




