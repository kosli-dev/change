Logging Artifacts
=================

To register an artifact in Merkely, you use the `log_artifact` command.  To get the sha256 for your artifact, you have three options:

* Explicitly provide the sha256 of the binary to the command.
* Provide the full path to the file - the command will calculate the sha digest.
* Provide the docker image and access to the docker daemon - the command will use the docker daemon to query the repoDigest of the docker image. This requires the image to be pushed to a registry first.

Here is an example using a docker image:

.. describe_command:: log_artifact invocation_minimum docker


