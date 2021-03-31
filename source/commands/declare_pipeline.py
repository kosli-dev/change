from commands import Command
from env_vars import *
from lib.api_schema import ApiSchema


class DeclarePipeline(Command):

    def doc_summary(self, _ci_name):
        return "Declares a pipeline in Merkely."

    def doc_volume_mounts(self, _ci_name):
        return []

    def __call__(self):
        url = ApiSchema.url_for_pipelines(self.host.value, self.merkelypipe)
        payload = self.merkelypipe
        return 'PUT', url, payload, None

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
            'dry_run'
        ]
