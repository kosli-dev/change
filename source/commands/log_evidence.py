from commands import Command
from env_vars import *
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class LogEvidence(Command):

    def summary(self, _ci):
        return "Logs evidence in Merkely."

    def volume_mounts(self, ci):
        if ci == 'bitbucket':
            return []
        else:
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
        return DescriptionEnvVar(self.env)

    @property
    def evidence_type(self):
        return EvidenceTypeEnvVar(self.env)

    @property
    def _merkely_env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'evidence_type',
            'is_compliant',
            'description',
            'ci_build_url',
            'user_data',
            'owner',
            'pipeline',
            'api_token',
            'host',
        ]


class DescriptionEnvVar(RequiredEnvVar):

    def __init__(self, env):
        notes = "A description for the evidence."
        super().__init__(env, "MERKELY_DESCRIPTION", notes)

    def ci_doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, '${{ env.COVERAGE_SUMMARY }}'
        if ci_name == 'bitbucket':
            return True, '${COVERAGE_SUMMARY}'
        return False, ""

