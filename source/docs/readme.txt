
The generated .rst files contains tables which look like this:

ENV_VAR_NAME        Required?    Notes
MERKELY_COMMAND     yes          The Merkely command to execute. This page documents a ...
MERKELY_FINGERPRINT yes          The artifact’s Fingerprint
...
MERKELY_USER_DATA   no           A pathed filename containing json content ...


There is a reason for using a column called "Required?" instead of
a column called "Defaulted?" (say). The reason is that the table appears
in multiple tabs, one tab for the generic [Docker] case and extra
tab for each for each supported CI system, eg [Github] Actions.

The table for the [Docker] case might contain this...

ENV_VAR_NAME                  Required?    Notes
MERKELY_ARTIFACT_GIT_COMMIT   yes          The sha of the git commit that produced this build.

whereas the table for the [Github] case might contain this...

ENV_VAR_NAME                  Required?    Notes
MERKELY_ARTIFACT_GIT_COMMIT   no           The sha of the git commit that produced this build.
                                           Defaults to ${GITHUB_SHA}

Why the difference?

The reason is that in for a raw docker command _every_ environment-variable has to be
_explicitly_ passed in. In contrast, for Github Actions, for example, you do _not_
have to explicitly pass in all environment variables. This is because your yaml
looks like this:

    - name: Log Docker image in Merkely
      uses: docker://merkely/change:latest
      env:
        MERKELY_COMMAND: log_artifact
        ...

and all the CI's built-in environment variables, such as ${GITHUB_SHA}, are
automatically passed into the docker container created from the:
      uses: docker://merkely/change:latest
