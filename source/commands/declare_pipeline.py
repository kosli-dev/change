from commands import Command
from docs import *
from env_vars import *
from lib.api_schema import ApiSchema


class DeclarePipeline(Command):

    def doc_summary(self, _ci_name):
        return "Declares a pipeline in Merkely."

    def doc_volume_mounts(self):
        return []

    def doc_ref(self):
        return {
            'docker': (docker_change_makefile_line_ref, 'merkely_declare_pipeline:'),
            'github': (github_loan_calculator_master_pipeline_line_ref, 'MERKELY_COMMAND: declare_pipeline'),
            'bitbucket': (bitbucket_loan_calculator_line_ref, 'MERKELY_COMMAND: declare_pipeline'),
        }

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
