from commands import Command
from env_vars import *
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class LogEvidence(Command):

    @property
    def summary(self):
        return "Logs evidence in Merkely."

    @property
    def _volume_mounts(self):
        return ["/var/run/docker.sock:/var/run/docker.sock"]

    def __call__(self):
        self._print_compliance()
        payload = {
            "evidence_type": self.evidence_type.value,
            "user_data": self.user_data.value,
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
    def description(self):
        notes = "..."
        return self._required_env_var("MERKELY_DESCRIPTION", notes)

    @property
    def evidence_type(self):
        notes = "The evidence type."
        return self._required_env_var("MERKELY_EVIDENCE_TYPE", notes)

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
            'user_data',
            'api_token',
            'host',
        ]
