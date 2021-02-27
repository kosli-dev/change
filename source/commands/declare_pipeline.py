from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class DeclarePipeline(Command):

    @property
    def summary(self):
        return "Declares a pipeline in Merkely"

    @property
    def _volume_mounts(self):
        return []

    def __call__(self):
        url = ApiSchema.url_for_pipelines(self.host.value, self.merkelypipe)
        payload = self.merkelypipe
        http_put_payload(url, payload, self.api_token.value)
        return 'Putting', url, payload

    @property
    def _merkely_env_var_names(self):
        return [
            'name',
            'api_token',
            'host',
        ]
