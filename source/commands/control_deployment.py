from errors import ChangeError
from commands import Command
from cdb.api_schema import ApiSchema
from cdb.control_deployment import control_deployment_approved
from cdb.http import http_get_json


class ControlDeployment(Command):

    def summary(self, _ci):
        return "Controls Deployments by short-circuiting pipelines if artifact not approved for release"

    def volume_mounts(self, ci):
        if ci == 'bitbucket':
            return []
        else:
            return ["/var/run/docker.sock:/var/run/docker.sock"]

    @property
    def _merkely_env_var_names(self):
        return [
            'name',
            'fingerprint',
            'api_token',
            'host',
        ]

    def __call__(self):
        url = ApiSchema.url_for_artifact_approvals(self.host.value, self.merkelypipe, self.fingerprint.sha)
        approvals = http_get_json(url, self.api_token.value)
        is_approved = control_deployment_approved(approvals)
        if not is_approved:
            raise ChangeError(f"Artifact with sha {self.fingerprint.sha} is not approved for deployment")
        return 'Getting', url, approvals
