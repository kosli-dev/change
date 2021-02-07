from collections import namedtuple
from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class LogArtifactCommand(Command):
    """
    Logs an artifact in Merkely.
    Invoked like this:

    docker run \
        --env MERKELY_COMMAND=log_artifact \
        --env MERKELY_API_TOKEN=${...} \
        \
        --env MERKELY_FINGERPRINT=${...} \
        --env MERKELY_DISPLAY_NAME=${...} \
        \
        --env MERKELY_ARTIFACT_GIT_COMMIT=${...} \
        --env MERKELY_ARTIFACT_GIT_URL=${...} \
        --env MERKELY_CI_BUILD_NUMBER=${...} \
        --env MERKELY_CI_BUILD_URL=${...} \
        --env MERKELY_IS_COMPLIANT=${...} \
        --rm \
        ... \
        --volume ${YOUR_MERKELY_PIPE}:/Merkelypipe.json \
        merkely/change
    """

    def __call__(self):
        self._print_compliance()
        payload = {
            "sha256": self.fingerprint.sha,
            "filename": self.display_name.value,
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
            'is_compliant',
            'name'
        ))(
            self.api_token,
            self.artifact_git_commit,
            self.artifact_git_url,
            self.ci_build_number,
            self.ci_build_url,
            self.display_name,
            self.fingerprint,
            self.host,
            self.is_compliant,
            self.name
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
