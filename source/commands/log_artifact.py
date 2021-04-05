from commands import Command
from docs import *
from env_vars import *
from lib.api_schema import ApiSchema


class LogArtifact(Command):

    def doc_summary(self):
        return "Logs an artifact in Merkely."

    def doc_volume_mounts(self):
        return ["/var/run/docker.sock:/var/run/docker.sock"]

    def doc_ref(self):
        return {
            'docker': (docker_change_makefile_line_ref, 'merkely_log_artifact:'),
            'github': (github_loan_calculator_master_pipeline_line_ref, 'MERKELY_COMMAND: log_artifact'),
            'bitbucket': (bitbucket_loan_calculator_line_ref, 'MERKELY_COMMAND: log_artifact'),
        }

    def __call__(self):
        url = ApiSchema.url_for_artifacts(self.host.value, self.merkelypipe)
        payload = {
            "sha256": self.fingerprint.sha,
            "filename": self.fingerprint.artifact_basename,
            "description": f"Created by build {self.ci_build_number.value}",
            "git_commit": self.artifact_git_commit.value,
            "commit_url": self.artifact_git_url.value,
            "build_url": self.ci_build_url.value,
            "is_compliant": self.is_compliant.value == 'TRUE',
            "user_data": self.user_data.value
        }
        return 'PUT', url, payload, None

    @property
    def artifact_git_commit(self):
        return ArtifactGitCommitEnvVar(self.env)

    @property
    def artifact_git_url(self):
        return ArtifactGitUrlEnvVar(self.env)

    @property
    def ci_build_number(self):
        return CIBuildNumberEnvVar(self.env)

    @property
    def _merkely_env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'is_compliant',
            'artifact_git_commit',
            'artifact_git_url',
            'ci_build_number',
            'ci_build_url',
            'user_data',
            'owner',
            'pipeline',
            'api_token',
            'host',
            'dry_run'
        ]
