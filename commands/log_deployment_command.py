from collections import namedtuple
from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_post_payload


class LogDeploymentCommand(Command):
    """
    Logs a deployment in Merkely.
    Invoked like this:

    docker run \
        --env MERKELY_COMMAND=log_deployment \
        --env MERKELY_API_TOKEN=${...} \
        \
        --env MERKELY_FINGERPRINT=${...} \
        --env MERKELY_DISPLAY_NAME=${...} \
        \
        --env MERKELY_CI_BUILD_NUMBER=${...} \
        --env MERKELY_CI_BUILD_URL=${...} \
        --env MERKELY_DESCRIPTION=${...} \
        --env MERKELY_ENVIRONMENT=${...} \
        --env MERKELY_IS_COMPLIANT=${...} \
        --rm \
        ... \
        --volume ${YOUR_MERKELY_PIPE}:/Merkelypipe.json \
        merkely/change
    """

    def __call__(self):
        payload = {
            "artifact_sha256": self.fingerprint.sha,
            "build_url": self.ci_build_url.value,
            "description": self.description.value,
            "environment": self.environment.value,
        }
        url = ApiSchema.url_for_deployments(self.host.value, self.merkelypipe)
        http_post_payload(url, payload, self.api_token.value)
        return 'Posting', url, payload

    @property
    def env_vars(self):
        return namedtuple('EnvVars', (
            'api_token',
            'ci_build_url',
            'display_name',
            'description',
            'environment',
            'fingerprint',
            'host',
            'name'
        ))(
            self.api_token,
            self.ci_build_url,
            self.display_name,
            self.description,
            self.environment,
            self.fingerprint,
            self.host,
            self.name
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
