from commands import Command
from env_vars import *
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class LogTestCommand(Command):

    @property
    def summary(self):
        return "Logs test evidence in Merkely."

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

    """
    def __call__(self):
        payload = {
        }
        url = ApiSchema.url_for_artifact(self.host.value, self.merkelypipe, self.fingerprint.sha)
        http_put_payload(url, payload, self.api_token.value)
        return 'Putting', url, payload

    @property
    def ci_build_url(self):
        notes = "Link to the build information."
        return self._required_env_var('CI_BUILD_URL', notes)

    @property
    def description(self):
        notes = "..."
        return self._required_env_var("DESCRIPTION", notes)

    @property
    def evidence_type(self):
        notes = "The evidence type."
        return self._required_env_var("EVIDENCE_TYPE", notes)

    @property
    def _env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'evidence_type',
            'is_compliant',
            'description',
            'ci_build_url',
            'api_token',
            'host',
        ]
    """

