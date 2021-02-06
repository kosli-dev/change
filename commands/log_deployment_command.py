import os
from collections import namedtuple
from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_post_payload


class LogDeploymentCommand(Command):
    """
    Command subclass for handling MERKELY_COMMAND=log_deployment
    """

    def __call__(self):
        sha256, name = self._context.fingerprint(self.env_vars)
        return self._create_deployment(sha256, name)

    @property
    def env_vars(self):
        return namedtuple('EnvVars', (
            'api_token',
            'ci_build_url',
            'display_name',
            'description',
            'environment',
            'fingerprint',
            'host'
        ))(
            self.api_token,
            self.ci_build_url,
            self.display_name,
            self.description,
            self.environment,
            self.fingerprint,
            self.host
        )

    @property
    def ci_build_url(self):
        description = "A url for the deployment."
        return self._required_env_var('CI_BUILD_URL', description)

    @property
    def description(self):
        description = "A description for the deployment."
        return self._required_env_var('DESCRIPTION', description)

    @property
    def environment(self):
        description = "The name of the environment the artifact is being deployed to."
        return self._required_env_var('ENVIRONMENT', description)

    @property
    def fingerprint(self):
        description = "\n".join([
            '1. If prefixed by docker:// the name+tag of the docker image to fingerprint.',
            '   The docker socket must be volume-mounted.',
            '   Example:',
            '     --env MERKELY_FINGERPRINT=”docker://${YOUR_DOCKER_IMAGE_AND_TAG}"',
            '     --volume /var/run/docker.sock:/var/run/docker.sock',
            '',
            '2. If prefixed by file:// the full path of the file to fingerprint.',
            '   The full path must be volume-mounted.',
            '   Example:',
            '     --env MERKELY_FINGERPRINT=”file://${YOUR_FILE_PATH}',
            '     --volume=${YOUR_FILE_PATH}:${YOUR_FILE_PATH}',
            '',
            "3. If prefixed by sha256:// the deployed artifact's sha256 digest."
            '   The name of the artifact must be provided in MERKELY_DISPLAY_NAME',
            '   Example:',
            '     --env MERKELY_FINGERPRINT=”sha256://${YOUR_ARTIFACT_SHA256}”',
            '     --env MERKELY_DISPLAY_NAME=”${YOUR_ARTIFACT_NAME}”'
        ])
        return self._required_env_var("FINGERPRINT", description)

    @property
    def display_name(self):
        description = "\n".join([
            'The name of the deployed artifact.',
            'Required when using MERKELY_FINGERPRINT="sha256://..."',
            'Not required when using MERKELY_FINGERPRINT="file://..."',
            'Not required when using MERKELY_FINGERPRINT="docker://..."'
        ])
        return self._optional_env_var("DISPLAY_NAME", description)

    def _create_deployment(self, sha256, _display_name):
        payload = {
            "artifact_sha256": sha256,
            "build_url": self.ci_build_url.value,
            "description": self.description.value,
            "environment": self.environment.value,
        }
        url = ApiSchema.url_for_deployments(self.host.value, self.merkelypipe)
        http_post_payload(url, payload, self.api_token.value)
        return 'Posting', url, payload
