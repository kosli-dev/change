from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_post_payload


class LogDeploymentCommand(Command):
    """
    Logs a deployment in Merkely.
    Invoked like this:

    docker run \
        --env MERKELY_COMMAND=log_deployment \
        --env MERKELY_FINGERPRINT=${...} \
        \
        --env MERKELY_CI_BUILD_NUMBER=${...} \
        --env MERKELY_CI_BUILD_URL=${...} \
        --env MERKELY_DESCRIPTION=${...} \
        --env MERKELY_ENVIRONMENT=${...} \
        --env MERKELY_IS_COMPLIANT=${...} \
        --rm \
        --env MERKELY_API_TOKEN=${...} \
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
    def _env_var_names(self):
        return [
            'api_token',
            'ci_build_url',
            'description',
            'environment',
            'fingerprint',
            'host',
            'name'
        ]
