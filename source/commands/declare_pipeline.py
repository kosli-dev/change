from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class DeclarePipeline(Command):

    def summary(self, _ci):
        return "Declares a pipeline in Merkely"

    def volume_mounts(self, _ci):
        return []

    def __call__(self):
        url = ApiSchema.url_for_pipelines(self.host.value, self.merkelypipe)
        payload = self.merkelypipe
        http_put_payload(url, payload, self.api_token.value)
        return 'Putting', url, payload

    @property
    def pipe_path(self):
        # See external.merkelypipe
        name = "MERKELY_PIPE_PATH"
        default = "/data/Merkelypipe.json"
        notes = " ".join([
            f"The full path to your Merkelypipe file.",
            "Must be volume-mounted in the container.",
            f"Defaults to {default}.",
        ])
        return self._static_defaulted_env_var(name, default, notes)

    @property
    def _merkely_env_var_names(self):
        return [
            'name',
            'api_token',
            'owner',
            'pipeline',
            'pipe_path',
            'host',
        ]
