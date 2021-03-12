from commands import Command
from env_vars import *
from cdb.api_schema import ApiSchema
from cdb.http import http_post_payload


class LogDeployment(Command):

    def summary(self, _ci):
        return "Logs a deployment in Merkely."

    def volume_mounts(self, ci):
        if ci == 'bitbucket':
            return []
        else:
            return ["/var/run/docker.sock:/var/run/docker.sock"]

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
    def description(self):
        notes = "A description for the deployment."
        return self._required_env_var('MERKELY_DESCRIPTION', notes)

    @property
    def environment(self):
        notes = "The name of the environment the artifact is being deployed to."
        return self._required_env_var('MERKELY_ENVIRONMENT', notes)

    @property
    def _merkely_env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'ci_build_url',
            'description',
            'environment',
            'user_data',
            'api_token',
            'pipe_path',
            'host',
        ]
