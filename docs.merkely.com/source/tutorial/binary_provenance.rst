Logging Artifacts
=================

To register an artifact in Merkely, you use the `log_artifact` command.  To get the sha256 for your artifact, you have three options:

* Explicitly provide the sha256 of the binary to the command.
* Provide the full path to the file - the command will calculate the sha digest.
* Provide the docker image and access to the docker daemon - the command will use the docker daemon to query the repoDigest of the docker image. This requires the image to be pushed to a registry first.

Here is an example using a docker image:

.. code-block:: bash
    :linenos:

    docker run \
      --env MERKELY_COMMAND=log_artifact \
      \
      --env MERKELY_FINGERPRINT="docker://${YOUR_DOCKER_IMAGE_AND_TAG}" \
      --env MERKELY_CI_BUILD_URL=${YOUR_CI_BUILD_URL} \
      --env MERKELY_BUILD_NUMBER=${YOUR_BUILD_NUMBER} \
      --env MERKELY_ARTIFACT_GIT_URL=${YOUR_GIT_COMMIT_URL} \
      --env MERKELY_ARTIFACT_GIT_COMMIT=${YOUR_SOURCE_GIT_COMMIT} \
      --env MERKELY_API_TOKEN=${YOUR_API_TOKEN} \
      --rm \
      --volume ${PWD}/${YOUR_MERKELY_PIPE}:/data/Merkelypipe.json \
      --volume /var/run/docker.sock:/var/run/docker.sock \
      merkely/change


