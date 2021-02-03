import os
from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class LogArtifactCommand(Command):
    """
    Command subclass for handling MERKELY_COMMAND=log_artifact
    """
    @property
    def args(self):
        return (self.api_token,
                self.artifact_git_commit,
                self.artifact_git_url,
                self.ci_build_number,
                self.ci_build_url,
                self.display_name,
                self.is_compliant,
                self.fingerprint,
                self.host)

    @property
    def artifact_git_commit(self):
        return self._required_env_var('ARTIFACT_GIT_COMMIT')

    @property
    def artifact_git_url(self):
        return self._required_env_var('ARTIFACT_GIT_URL')

    @property
    def ci_build_number(self):
        return self._required_env_var('CI_BUILD_NUMBER')

    @property
    def ci_build_url(self):
        return self._required_env_var('CI_BUILD_URL')

    @property
    def is_compliant(self):
        return self._required_env_var('IS_COMPLIANT')

    @property
    def fingerprint(self):
        return self._required_env_var("FINGERPRINT")

    @property
    def display_name(self):
        return self._optional_env_var("DISPLAY_NAME")

    def execute(self):
        fp = self.fingerprint.value
        file_protocol = "file://"
        if fp.startswith(file_protocol):
            artifact_name = fp[len(file_protocol):]
            self._log_artifact_file(file_protocol, artifact_name)
        docker_protocol = "docker://"
        if fp.startswith(docker_protocol):
            artifact_name = fp[len(docker_protocol):]
            self._log_artifact_docker_image(docker_protocol, artifact_name)
        sha_protocol = "sha256://"
        if fp.startswith(sha_protocol):
            sha256 = fp[len(sha_protocol):]
            self._log_artifact_sha(sha256)

    def _log_artifact_file(self, protocol, filename):
        print(f"Getting SHA for {protocol} artifact: {filename}")
        sha256 = self._context.sha_digest_for_file('/'+filename)
        print(f"Calculated digest: {sha256}")
        self._print_compliance()
        self._create_artifact(sha256, os.path.basename(filename))

    def _log_artifact_docker_image(self, protocol, image_name):
        print(f"Getting SHA for {protocol} artifact: {image_name}")
        sha256 = self._context.sha_digest_for_docker_image(image_name)
        print(f"Calculated digest: {sha256}")
        self._print_compliance()
        self._create_artifact(sha256, image_name)

    def _log_artifact_sha(self, sha256):
        self._print_compliance()
        self._create_artifact(sha256, self.display_name.value)

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

    def _print_compliance(self):
        env_var = self.is_compliant
        print(f"{env_var.name}: {env_var.value == 'TRUE'}")
