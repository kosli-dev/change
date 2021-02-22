from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class DeclarePipeline(Command):
    @property
    def summary(self):
        return "Declares a pipeline in Merkely"

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
        invocation_string += "    --volume ${YOUR_MERKELY_PIPE}:/Merkelypipe.json \\\n"
        invocation_string += "    merkely/change"
        return invocation_string

    def __call__(self):
        url = ApiSchema.url_for_pipelines(self.host.value, self.merkelypipe)
        payload = self.merkelypipe
        http_put_payload(url, payload, api_token=self.api_token.value)
        return 'Putting', url, payload

    @property
    def _env_var_names(self):
        return [
            'api_token',
            'host',
            'name',
        ]
