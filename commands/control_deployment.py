from cdb.api_schema import ApiSchema
from cdb.control_deployment import control_deployment_approved
from cdb.http import http_get_json
from commands import Command, CommandError


class ControlDeployment(Command):

    @property
    def summary(self):
        return "Controls Deployments by short-circuiting pipelines if artifact not approved for release"

    def invocation(self, type):
        def env(var):
            if var.name == "MERKELY_COMMAND":
                value = var.value
            elif var.name == "MERKELY_FINGERPRINT":
                value = var.example
            else:
                value = "${...}"
            return f'    --env {var.name}="{value}" \\\n'

        invocation_string = "docker run \\\n"
        for name in self._env_var_names:
            var = getattr(self, name)
            if type == 'full':
                invocation_string += env(var)
            if type == 'minimum' and var.is_required:
                invocation_string += env(var)

        invocation_string += "    --rm \\\n"
        invocation_string += "    --volume /var/run/docker.sock:/var/run/docker.sock \\\n"
        invocation_string += "    --volume ${YOUR_MERKELY_PIPE}:/Merkelypipe.json \\\n"
        invocation_string += "    merkely/change"
        return invocation_string

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
        return 'Getting', url, approvals
