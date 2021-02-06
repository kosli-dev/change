from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class LogEvidenceCommand(Command):
    """
    Command subclass for handling MERKELY_COMMAND=log_evidence
    """
    @property
    def args_list(self):
        return [
            self.api_token,
            self.ci_build_url,
            self.display_name,
            self.description,
            self.evidence_type,
            self.is_compliant,
            self.fingerprint,
            self.host
        ]

    @property
    def ci_build_url(self):
        description = ""
        return self._required_env_var('CI_BUILD_URL', description)

    @property
    def description(self):
        description = ""
        return self._optional_env_var('DESCRIPTION', description)

    @property
    def display_name(self):
        description = ""
        return self._optional_env_var("DISPLAY_NAME", description)

    @property
    def evidence_type(self):
        description = ""
        return self._required_env_var("EVIDENCE_TYPE", description)

    @property
    def is_compliant(self):
        description = ""
        return self._required_env_var('IS_COMPLIANT', description)

    @property
    def fingerprint(self):
        description = ""
        return self._required_env_var("FINGERPRINT", description)

    def execute(self):
        sha256, name = self._context.fingerprint(self)
        self._print_compliance()
        return self._create_evidence(sha256, name)

    def _print_compliance(self):
        env_var = self.is_compliant
        print(f"{env_var.name}: {env_var.value == 'TRUE'}")

    def _create_evidence(self, sha256, _name):
        payload = {
            "evidence_type": self.evidence_type.value,
            "contents": {
                "is_compliant": self.is_compliant.value == "TRUE",
                "url": self.ci_build_url.value,
                "description": self.description.value
            }
        }
        url = ApiSchema.url_for_artifact(self.host.value, self.merkelypipe, sha256)
        http_put_payload(url, payload, self.api_token.value)
        return 'Putting', url, payload
