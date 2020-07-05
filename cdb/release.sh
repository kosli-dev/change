#!/bin/bash
commits=$(git rev-list production..master)

commits=[$(echo "${commits[*]}" | awk -v q="\"" '{ print q$1q }' | paste -s -d, -)]

echo commits="${commits[@]}"

artifact=$(docker inspect --format='{{index .RepoDigests 0}}' $IMAGE | sed 's/.*://')
echo artifact = $artifact

jq --argjson commits "${commits[@]}" '.src_commit_list = $commits' release_template.json \
  | jq --arg artifact $artifact '.base_artifact = $artifact' \
  | jq --arg artifact $artifact '.target_artifact = $artifact' > release.json

cat release.json

