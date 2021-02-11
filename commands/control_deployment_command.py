from cdb.api_schema import ApiSchema
from cdb.control_deployment import control_deployment_approved
from cdb.http import http_get_json
from commands import Command, CommandError


class ControlDeploymentCommand(Command):

    @property
    def _env_var_names(self):
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
            raise CommandError()
        # what do I return?
        return 'Getting', url, approvals