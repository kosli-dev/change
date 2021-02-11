from commands import Command, load_json
from env_vars import UserDataEnvVar
from cdb.api_schema import ApiSchema
from cdb.http import http_post_payload


class LogDeploymentCommand(Command):
    """
    Logs a deployment in Merkely.
    Invoked like this:

    docker run \
        --env MERKELY_COMMAND=log_deployment \
        --env MERKELY_FINGERPRINT="docker://${...}" \
        \
        --env MERKELY_IS_COMPLIANT=${...} \
        --env MERKELY_CI_BUILD_NUMBER=${...} \
        --env MERKELY_DESCRIPTION=${...} \
        --env MERKELY_ENVIRONMENT=${...} \
        --env MERKELY_USER_DATA=${...} \
        --rm \
        --env MERKELY_API_TOKEN=${...} \
        --volume /var/run/docker.sock:/var/run/docker.sock \
        --volume ${YOUR_MERKELY_PIPE}:/Merkelypipe.json \
        merkely/change
    """

    def __call__(self):
        payload = {
            "artifact_sha256": self.fingerprint.sha,
            "build_url": self.ci_build_url.value,
            "description": self.description.value,
            "environment": self.environment.value,
            "user_data": self.user_data.value
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
    def user_data(self):
        return UserDataEnvVar(self.env)

    @property
    def _env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'ci_build_url',
            'description',
            'environment',
            'user_data',
            'api_token',
            'host',
        ]
