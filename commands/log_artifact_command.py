from collections import namedtuple
from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class LogArtifactCommand(Command):
    """
    Command subclass for handling MERKELY_COMMAND=log_artifact
    """

    def __call__(self):
        sha256, name = self._context.fingerprint(self.env_vars)
        self._print_compliance()
        return self._create_artifact(sha256, name)

    @property
    def env_vars(self):
        return namedtuple('EnvVars', (
            'api_token',
            'artifact_git_commit',
            'artifact_git_url',
            'ci_build_number',
            'ci_build_url',
            'display_name',
            'fingerprint',
            'host',
            'is_compliant'
        ))(
            self.api_token,
            self.artifact_git_commit,
            self.artifact_git_url,
            self.ci_build_number,
            self.ci_build_url,
            self.display_name,
            self.fingerprint,
            self.host,
            self.is_compliant
        )

    @property
    def artifact_git_commit(self):
        description = "The sha of the git commit that produced this build."
        return self._required_env_var('ARTIFACT_GIT_COMMIT', description)

    @property
    def artifact_git_url(self):
        description = "Link to the source git commit this build was based on."
        return self._required_env_var('ARTIFACT_GIT_URL', description)

    @property
    def ci_build_number(self):
        description = "The ci build number."
        return self._required_env_var('CI_BUILD_NUMBER', description)

    @property
    def ci_build_url(self):
        description = "Link to the build in the ci system."
        return self._required_env_var('CI_BUILD_URL', description)

    @property
    def display_name(self):
        description = ""
        return self._optional_env_var("DISPLAY_NAME", description)

    @property
    def is_compliant(self):
        description = "Whether this artifact is considered compliant from you build process."
        return self._required_env_var('IS_COMPLIANT', description)

    @property
    def fingerprint(self):
        description = ""
        return self._required_env_var("FINGERPRINT", description)

    def _print_compliance(self):
        env_var = self.is_compliant
        print(f"{env_var.name}: {env_var.value == 'TRUE'}")

    def _create_artifact(self, sha256, display_name):
        description = f"Created by build {self.ci_build_number.value}"
        payload = {
            "sha256": sha256,
            "filename": display_name,
            "description": description,
            "git_commit": self.artifact_git_commit.value,
            "commit_url": self.artifact_git_url.value,
            "build_url": self.ci_build_url.value,
            "is_compliant": self.is_compliant.value == 'TRUE'
        }
        url = ApiSchema.url_for_artifacts(self.host.value, self.merkelypipe)
        http_put_payload(url, payload, self.api_token.value)
        return 'Putting', url, payload
