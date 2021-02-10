from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class LogEvidenceCommand(Command):

    @property
    def summary(self):
        return "Logs evidence in Merkely."

    @property
    def invocation(self):
        def env(prop, value="${{...}}"):
            ev_name = getattr(self, prop).name
            if ev_name == "MERKELY_COMMAND":
                value = getattr(self, prop).value
            return f"    --env {ev_name}={value} \\\n"

        invocation_string = "docker run \\\n"
        for name in self._env_var_names:
            invocation_string += env(name)

        invocation_string += "    --rm \\\n"
        invocation_string += "    --volume ${YOUR_MERKELY_PIPE}:/Merkelypipe.json \\\n"
        invocation_string += "    merkely/change"
        return invocation_string

    def __call__(self):
        self._print_compliance()
        payload = {
            "evidence_type": self.evidence_type.value,
            "contents": {
                "is_compliant": self.is_compliant.value == "TRUE",
                "url": self.ci_build_url.value,
                "description": self.description.value
            }
        }
        url = ApiSchema.url_for_artifact(self.host.value, self.merkelypipe, self.fingerprint.sha)
        http_put_payload(url, payload, self.api_token.value)
        return 'Putting', url, payload

    @property
    def ci_build_url(self):
        description = "Link to the build information."
        return self._required_env_var('CI_BUILD_URL', description)

    @property
    def description(self):
        description = "The description for the evidence."
        return self._optional_env_var('DESCRIPTION', description)

    @property
    def evidence_type(self):
        description = "The evidence type."
        return self._required_env_var("EVIDENCE_TYPE", description)

    @property
    def _env_var_names(self):
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
        # Print according to this order
