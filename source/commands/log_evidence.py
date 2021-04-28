from commands import Command
from docs import *
from env_vars import *
from lib.api_schema import ApiSchema


class LogEvidence(Command):

    def doc_summary(self):
        return "Logs evidence in Merkely."

    def doc_volume_mounts(self):
        return ["/var/run/docker.sock:/var/run/docker.sock"]

    def doc_ref(self):
        return {
            'docker': (docker_change_makefile_line_ref, 'merkely_log_evidence:'),
            'github': (github_loan_calculator_master_pipeline_line_ref, 'MERKELY_COMMAND: log_evidence'),
            'bitbucket': (bitbucket_loan_calculator_line_ref, 'MERKELY_COMMAND: log_evidence'),
        }

    def __call__(self):
        url = ApiSchema.url_for_artifact(self.host.value, self.merkelypipe, self.fingerprint.sha)
        payload = {
            "evidence_type": self.evidence_type.value,
            "contents": {
                "is_compliant": self.is_compliant.value == "TRUE",
                "url": self.ci_build_url.value,
                "description": self.description.value,
                "user_data": self.user_data.value
            }
        }
        return 'PUT', url, payload, None

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
            'dry_run'
        ]


class DescriptionEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_DESCRIPTION")

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, '${{ env.COVERAGE_SUMMARY }}'
        if ci_name == 'bitbucket':
            return True, '${COVERAGE_SUMMARY}'
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return "A description for the evidence."

