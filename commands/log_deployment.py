from commands import Command, load_json
from env_vars import UserDataEnvVar
from cdb.api_schema import ApiSchema
from cdb.http import http_post_payload


class LogDeployment(Command):

    @property
    def summary(self):
        return "Logs a deployment in Merkely."

    def invocation(self, type):
        def env(var):
            if var.name == "MERKELY_COMMAND":
                value = var.value
            elif var.name == "MERKELY_FINGERPRINT":
                value = var.example
            else:
                value = "${...}"
            return f'    --env {var.name}="{value}" \\\n'

        invocation_string = "docker run \\\n"
        for name in self._env_var_names:
            var = getattr(self, name)
            if type == 'full':
                invocation_string += env(var)
            if type == 'minimum' and var.is_required:
                invocation_string += env(var)

        invocation_string += "    --rm \\\n"
        invocation_string += "    --volume /var/run/docker.sock:/var/run/docker.sock \\\n"
        invocation_string += "    --volume ${YOUR_MERKELY_PIPE}:/Merkelypipe.json \\\n"
        invocation_string += "    merkely/change"
        return invocation_string

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
        notes = "A url for the deployment."
        return self._required_env_var('CI_BUILD_URL', notes)

    @property
    def description(self):
        notes = "A description for the deployment."
        return self._required_env_var('DESCRIPTION', notes)

    @property
    def environment(self):
        notes = "The name of the environment the artifact is being deployed to."
        return self._required_env_var('ENVIRONMENT', notes)

    @property
    def user_data(self):
        return UserDataEnvVar(self._env)

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
