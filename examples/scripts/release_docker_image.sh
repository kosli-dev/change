#!/bin/sh

set -e

# This script creates a release in ComplianceDB.
#
# It relies on the following environment variables being present
#
#   $CDB_API_TOKEN - Your api token for ComplianceDB
#   $CDB_DOCKER_IMAGE - The docker image specification
#   $CDB_TARGET_SRC_COMMITISH - The commit that is going into produciton
#   $CDB_BASE_SRC_COMMITISH - The commit from the previous release
#   $CDB_RELEASE_DESCRIPTION - The description for the list
#
# Additionally, the script has the following dependencies
#
#   jq
#   git
#   docker
#   curl

if [[ -z "$CDB_API_TOKEN" ]]; then
    echo "Must provide CDB_API_TOKEN in environment" 1>&2
    exit 1
fi

if [[ -z "$CDB_OWNER" ]]; then
    echo "Must provide CDB_OWNER in environment" 1>&2
    exit 1
fi

if [[ -z "$CDB_PROJECT" ]]; then
    echo "Must provide CDB_PROJECT in environment" 1>&2
    exit 1
fi

if [[ -z "$CDB_DOCKER_IMAGE" ]]; then
    echo "Must provide CDB_DOCKER_IMAGE in environment" 1>&2
    exit 1
fi

if [[ -z "$CDB_TARGET_SRC_COMMITISH" ]]; then
    echo "Must provide CDB_TARGET_SRC_COMMITISH in environment" 1>&2
    exit 1
fi

if [[ -z "$CDB_BASE_SRC_COMMITISH" ]]; then
    echo "Must provide CDB_BASE_SRC_COMMITISH in environment" 1>&2
    exit 1
fi

if [[ -z "$CDB_RELEASE_DESCRIPTION" ]]; then
    echo "Must provide CDB_RELEASE_DESCRIPTION in environment" 1>&2
    exit 1
fi


RELEASE_TEMPLATE=$(cat <<-END
{
     "base_artifact": "",
     "target_artifact": "",
     "description": "",
     "src_commit_list": []
}
END
)

commits=$(git rev-list $CDB_BASE_SRC_COMMITISH..$CDB_TARGET_SRC_COMMITISH)

commits=[$(echo "${commits[*]}" | awk -v q="\"" '{ print q$1q }' | paste -s -d, -)]

echo 'Relevent commits found in git'="${commits[@]}"

ARTIFACT_SHA=$(docker inspect --format='{{index .RepoDigests 0}}' $CDB_DOCKER_IMAGE | sed 's/.*://')
echo "Found repoDigest of $ARTIFACT_SHA for $CDB_DOCKER_IMAGE"

echo "$RELEASE_TEMPLATE" \
  | jq --argjson commits "${commits[@]}" '.src_commit_list = $commits' \
  | jq --arg ARTIFACT_SHA "$ARTIFACT_SHA" '.base_artifact = $ARTIFACT_SHA' \
  | jq --arg ARTIFACT_SHA "$ARTIFACT_SHA" '.target_artifact = $ARTIFACT_SHA' \
  | jq --arg CDB_RELEASE_DESCRIPTION "$CDB_RELEASE_DESCRIPTION" '.description = $CDB_RELEASE_DESCRIPTION' \
  | curl -H 'Content-Type: application/json' \
      -u ${CDB_API_TOKEN}:unused \
      -X POST \
      --data-binary @- \
     http://localhost/api/v1/projects/$CDB_OWNER/$CDB_PROJECT/releases/
