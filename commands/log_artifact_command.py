import os
from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class RequiredEnvVar:
    def __init__(self, name, env):
        self._name = name
        self._env = env

    @property
    def name(self):
        return f"MERKELY_{self._name}"

    @property
    def value(self):
        value = self._env.get(self.name, None)
        if value is None:
            raise Command.Error(f"{self.name} environment-variable not set")
        if value == "":
            raise Command.Error(f"{self.name} environment-variable is empty string")
        return value


class LogArtifactCommand(Command):
    """
    Command subclass for handling MERKELY_COMMAND=log_artifact
    """

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
        return self._merkely_env('IS_COMPLIANT') == "TRUE"

    @property
    def fingerprint(self):
        return self._merkely_env("FINGERPRINT")

    @property
    def display_name(self):
        return self._env("MERKELY_DISPLAY_NAME")

    def _required_env_var(self, name):
        return RequiredEnvVar(name, self._context.env)

    def _verify_args(self):
        self.artifact_git_commit.value
        self.artifact_git_url.value
        self.ci_build_number.value
        self.ci_build_url.value
        self.fingerprint
        self.is_compliant

    def _concrete_execute(self):
        file_protocol = "file://"
        if self.fingerprint.startswith(file_protocol):
            index = len(file_protocol)
            name = self.fingerprint[index:]
            self._log_artifact_file(file_protocol, name)
        docker_protocol = "docker://"
        if self.fingerprint.startswith(docker_protocol):
            index = len(docker_protocol)
            name = self.fingerprint[index:]
            self._log_artifact_docker_image(docker_protocol, name)
        sha_protocol = "sha256://"
        if self.fingerprint.startswith(sha_protocol):
            index = len(sha_protocol)
            sha256 = self.fingerprint[index:]
            self._log_artifact_sha(sha256)

    def _log_artifact_file(self, protocol, filename):
        print(f"Getting SHA for {protocol} artifact: {filename}")
        sha256 = self._context.sha_digest_for_file('/'+filename)
        print(f"Calculated digest: {sha256}")
        # print("Publish artifact to ComplianceDB")
        print(f"MERKELY_IS_COMPLIANT: {self.is_compliant}")
        self._create_artifact(sha256, os.path.basename(filename))

    def _log_artifact_docker_image(self, protocol, image_name):
        print(f"Getting SHA for {protocol} artifact: {image_name}")
        sha256 = self._context.sha_digest_for_docker_image(image_name)
        print(f"Calculated digest: {sha256}")
        # print("Publish artifact to ComplianceDB")
        print(f"MERKELY_IS_COMPLIANT: {self.is_compliant}")
        self._create_artifact(sha256, image_name)

    def _log_artifact_sha(self, sha256):
        print(f"MERKELY_IS_COMPLIANT: {self.is_compliant}")
        self._create_artifact(sha256, self.display_name)

    def _create_artifact(self, sha256, display_name):
        description = f"Created by build {self.ci_build_number.value}"
        create_artifact_payload = {
            "sha256": sha256,
            "filename": display_name,
            "description": description,
            "git_commit": self.artifact_git_commit.value,
            "commit_url": self.artifact_git_url.value,
            "build_url": self.ci_build_url.value,
            "is_compliant": self.is_compliant
        }
        url = ApiSchema.url_for_artifacts(self.host, self.merkelypipe)
        http_put_payload(url, create_artifact_payload, self.api_token)

