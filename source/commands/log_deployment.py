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
        return DescriptionEnvVar(self.env)

    @property
    def environment(self):
        return EnvironmentEnvVar(self.env)

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
            'owner',
            'pipeline',
            'api_token',
            'host',
        ]

class DescriptionEnvVar(RequiredEnvVar):

    def __init__(self, env):
        notes = "A description for the deployment."
        super().__init__(env, "MERKELY_DESCRIPTION", notes)

    def ci_doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, '"Deployed to production in pipeline"'
        return False, ""


class EnvironmentEnvVar(RequiredEnvVar):

    def __init__(self, env):
        notes = "The name of the environment the artifact is being deployed to."
        super().__init__(env, "MERKELY_ENVIRONMENT", notes)

    def ci_doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "production"
        return False, ""
