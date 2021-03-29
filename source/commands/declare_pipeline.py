from commands import Command
from env_vars import *
from cdb.api_schema import ApiSchema


class DeclarePipeline(Command):

    def summary(self, _ci):
        return "Declares a pipeline in Merkely"

    def volume_mounts(self, _ci):
        return []

    def __call__(self):
        url = ApiSchema.url_for_pipelines(self.host.value, self.merkelypipe)
        payload = self.merkelypipe
        return 'Putting', url, payload, self.api_token.value, None


    @property
    def pipe_path(self):
        return PipePathEnvVar(self.env)

    @property
    def _merkely_env_var_names(self):
        return [
            'name',
            'owner',
            'pipeline',
            'pipe_path',
            'api_token',
            'host',
        ]
