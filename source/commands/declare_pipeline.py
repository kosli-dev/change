from commands import Command
from docs import *
from env_vars import *
from lib.api_schema import ApiSchema


class DeclarePipeline(Command):

    def doc_summary(self, _ci_name):
        return "Declares a pipeline in Merkely."

    def doc_volume_mounts(self, _ci_name):
        return []

    def doc_ref(self, ci_name):
        if ci_name == 'docker':
            return docker_change_makefile_line_ref('merkely_declare_pipeline')
        if ci_name == 'github':
            return github_loan_calculator_master_line_ref('MERKELY_COMMAND: declare_pipeline')
        if ci_name == 'bitbucket':
            return bitbucket_loan_calculator_line_ref('MERKELY_COMMAND: declare_pipeline')

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
