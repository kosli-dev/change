from errors import ChangeError
from commands import Command
from cdb.api_schema import ApiSchema


class ControlDeployment(Command):

    def doc_summary(self, _ci_name):
        return "Fails a pipeline if an artifact is not approved for deployment in Merkely."

    def doc_volume_mounts(self, ci_name):
        if ci_name == 'docker':
            return ["/var/run/docker.sock:/var/run/docker.sock"]
        else:
            return []

    def __call__(self):
        url = ApiSchema.url_for_artifact_approvals(self.host.value, self.merkelypipe, self.fingerprint.sha)
        def callback(response):
            approvals = response
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
        ]


def control_deployment_approved(approvals):
    for approval in approvals:
        if approval["state"] == "APPROVED":
            return True
    return False
