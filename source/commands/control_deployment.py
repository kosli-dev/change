from errors import ChangeError
from commands import Command
from cdb.api_schema import ApiSchema


class ControlDeployment(Command):

    def summary(self, _ci_name):
        return "Fails a pipeline if an artifact is not approved for deployment."

    def volume_mounts(self, ci_name):
        if ci_name == 'bitbucket':
            return []
        else:
            return ["/var/run/docker.sock:/var/run/docker.sock"]

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

    def __call__(self):
        url = ApiSchema.url_for_artifact_approvals(self.host.value, self.merkelypipe, self.fingerprint.sha)
        def callback(response):
            approvals = response
            is_approved = control_deployment_approved(approvals)
            if not is_approved:
                raise ChangeError(f"Artifact with sha {self.fingerprint.sha} is not approved.")
            return 'GET', url, approvals
        return 'GET', url, None, callback


def control_deployment_approved(approvals):
    for approval in approvals:
        if approval["state"] == "APPROVED":
            return True
    return False
