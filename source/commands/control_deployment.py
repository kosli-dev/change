from errors import ChangeError
from docs import *
from commands import Command
from lib.api_schema import ApiSchema


class ControlDeployment(Command):

    def doc_summary(self, _ci_name):
        return "Fails a pipeline if an artifact is not approved for deployment in Merkely."

    def doc_volume_mounts(self, ci_name):
        if ci_name == 'docker':
            return ["/var/run/docker.sock:/var/run/docker.sock"]
        else:
            return []

    def doc_ref(self, ci_name):
        if ci_name == 'docker':
            return docker_change_makefile_line_ref('merkely_control_deployment:')
        if ci_name == 'github':
            return github_loan_calculator_deploy_to_production_line_ref('MERKELY_COMMAND: control_deployment')
        if ci_name == 'bitbucket':
            return bitbucket_loan_calculator_line_ref('MERKELY_COMMAND: control_deployment')

    def __call__(self):
        url = ApiSchema.url_for_artifact_approvals(self.host.value, self.merkelypipe, self.fingerprint.sha)

        def callback(response):
            approvals = response.json()
            is_approved = control_deployment_approved(approvals)
            if not is_approved:
                raise ChangeError(f"Artifact with sha {self.fingerprint.sha} is not approved.")
            return 'GET', url, approvals
        return 'GET', url, None, callback

    @property
    def _merkely_env_var_names(self):
        return [
            'name',
            'fingerprint',
            'owner',
            'pipeline',
            'api_token',
            'host',
            'dry_run'
        ]


def control_deployment_approved(approvals):
    for approval in approvals:
        if approval["state"] == "APPROVED":
            return True
    return False
