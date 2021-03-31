from commands import Command
from docs import *
from env_vars import *
from lib.api_schema import ApiSchema


class LogDeployment(Command):

    def doc_summary(self, _ci_name):
        return "Logs a deployment in Merkely."

    def doc_volume_mounts(self, ci_name):
        if ci_name == 'docker':
            return ["/var/run/docker.sock:/var/run/docker.sock"]
        else:
            return []

    def doc_ref(self, ci_name):
        if ci_name == 'docker':
            return docker_change_makefile_line_ref('merkely_log_deployment:')
        if ci_name == 'github':
            return github_loan_calculator_master_pipeline_line_ref('MERKELY_COMMAND: log_deployment')
        if ci_name == 'bitbucket':
            return bitbucket_loan_calculator_line_ref('MERKELY_COMMAND: log_deployment')

    def __call__(self):
        payload = {
            "artifact_sha256": self.fingerprint.sha,
            "build_url": self.ci_build_url.value,
            "description": self.description.value,
            "environment": self.environment.value,
            "user_data": self.user_data.value
        }
        url = ApiSchema.url_for_deployments(self.host.value, self.merkelypipe)
        return 'POST', url, payload, None

    @property
    def description(self):
        return DescriptionEnvVar(self.env)

    @property
    def environment(self):
        return EnvironmentEnvVar(self.env)

    @property
    def _merkely_env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'ci_build_url',
            'description',
            'environment',
            'user_data',
            'owner',
            'pipeline',
            'api_token',
            'host',
            'dry_run'
        ]

class DescriptionEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_DESCRIPTION")

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, '"Deployed to production in pipeline"'
        if ci_name == 'bitbucket':
            return True, '"Deployed to production in pipeline"'
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return "A description for the deployment."


class EnvironmentEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_ENVIRONMENT")

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "production"
        if ci_name == 'bitbucket':
            return True, "production"
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return "The name of the environment the artifact is being deployed to."
