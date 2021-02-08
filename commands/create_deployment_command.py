from commands import Command, DisplayNameEnvVar, FingerprintEnvVar, UserDataEnvVar
from cdb.api_schema import ApiSchema
from cdb.http import http_post_payload


class CreateDeploymentCommand(Command):

    def __call__(self):
        payload = {
            "artifact_sha256": self.fingerprint.sha,
            "environment": self.environment.value,
            "description": self.description.value,
            "build_url": self.ci_build_url.value,
            # Note: The CDB payload does not contain the artifact name
        }
        if self.user_data.is_present:
            payload["user_data"] = self.user_data.json
        url = ApiSchema.url_for_deployments(self.host.value, self.merkelypipe)
        http_post_payload(url, payload, self.api_token.value)
        return 'Posting', url, payload

    @property
    def _env_var_names(self):
        return [
            'fingerprint',
            'ci_build_url',
            'description',
            'display_name',
            'environment',
            'user_data'
        ]

    @property
    def fingerprint(self):
        return FingerprintEnvVar(self)

    @property
    def ci_build_url(self):
        description = ""
        return self._defaulted_env_var(self, "CI_BUILD_URL", None, description)

    @property
    def description(self):
        description = ""
        return self._defaulted_env_var(self, "DESCRIPTION", 'None', description)

    @property
    def display_name(self):
        return DisplayNameEnvVar(self)

    @property
    def environment(self):
        description = ""
        return self._defaulted_env_var(self, "ENVIRONMENT", 'None', description)

    @property
    def user_data(self):
        return UserDataEnvVar(self)
