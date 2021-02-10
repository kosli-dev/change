from commands import Command
from env_vars import FingerprintEnvVar, UserDataFileEnvVar
from cdb.api_schema import ApiSchema
from cdb.http import http_post_payload


class CreateDeploymentCommand(Command):

    def __call__(self):
        payload = {
            "artifact_sha256": self.fingerprint.sha,
            "environment": self.environment.value,
            "description": self.description.value,
            "build_url": self.ci_build_url.value,
        }
        if self.user_data_file.is_set:
            payload["user_data"] = self.user_data_file.json
        url = ApiSchema.url_for_deployments(self.host.value, self.merkelypipe)
        http_post_payload(url, payload, self.api_token.value)
        return 'Posting', url, payload

    @property
    def ci_build_url(self):
        description = "TODO"
        return self._defaulted_env_var("CI_BUILD_URL", None, description)

    @property
    def description(self):
        description = "TODO"
        return self._defaulted_env_var("DESCRIPTION", 'None', description)

    @property
    def environment(self):
        description = "TODO"
        return self._defaulted_env_var("ENVIRONMENT", 'None', description)

    @property
    def user_data_file(self):
        return UserDataFileEnvVar(self.env)

    @property
    def _env_var_names(self):
        return [
            'fingerprint',
            'ci_build_url',
            'description',
            'environment',
            'user_data_file'
        ]
