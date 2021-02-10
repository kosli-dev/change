from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class LogEvidenceCommand(Command):

    @property
    def overview(self):
        return "\n".join([
            "Logs evidence in Merkely.",
            "Invoked like this:",
            "",
            "docker run \\",
            "    --env MERKELY_COMMAND=log_deployment \\",
            f"    --env {self.fingerprint.name}=${{...}} \\",
            "    \\",
            "    --env MERKELY_CI_BUILD_URL=${...} \\",
            "    --env MERKELY_DESCRIPTION=${...} \\",
            "    --env MERKELY_EVIDENCE_TYPE=${...} \\",
            "    --env MERKELY_IS_COMPLIANT=${...} \\",
            "    --rm \\",
            f"    --env {self.api_token.name}=${{...}} \\",
            "    --volume ${YOUR_MERKELY_PIPE}:/Merkelypipe.json \\",
            "    merkely/change",
        ])

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
            'api_token',
            'ci_build_url',
            'description',
            'evidence_type',
            'fingerprint',
            'host',
            'is_compliant',
            'name'
        ]
