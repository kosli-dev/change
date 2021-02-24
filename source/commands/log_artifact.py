from commands import Command
from env_vars import *
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class LogArtifact(Command):

    @property
    def summary(self):
        return "Logs an artifact in Merkely."

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

    def __call__(self):
        self._print_compliance()
        payload = {
            "sha256": self.fingerprint.sha,
            "filename": self.fingerprint.artifact_basename,
            "description": f"Created by build {self.ci_build_number.value}",
            "git_commit": self.artifact_git_commit.value,
            "commit_url": self.artifact_git_url.value,
            "build_url": self.ci_build_url.value,
            "is_compliant": self.is_compliant.value == 'TRUE'
        }
        url = ApiSchema.url_for_artifacts(self.host.value, self.merkelypipe)
        http_put_payload(url, payload, self.api_token.value)
        return 'Putting', url, payload

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
    def _env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'is_compliant',
            'artifact_git_commit',
            'artifact_git_url',
            'ci_build_number',
            'ci_build_url',
            'api_token',
            'host',
        ]
