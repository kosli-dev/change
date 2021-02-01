from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class LogArtifactCommand(Command):
    """
    Command subclass for handling MERKELY_COMMAND=log_artifact
    """
    def __init__(self, context):
        super().__init__(context)
        self.description = "Created by build " + self._required_env('MERKELY_CI_BUILD_NUMBER')
        self.git_commit = self._required_env('MERKELY_ARTIFACT_GIT_COMMIT')
        self.commit_url = self._env('MERKELY_ARTIFACT_GIT_URL')
        self.build_url = self._env('MERKELY_CI_BUILD_URL')
        self.is_compliant = self._env('MERKELY_IS_COMPLIANT') == "TRUE"
        self.fingerprint = self._env("MERKELY_FINGERPRINT")

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
        self._create_artifact(sha256, filename)

    def _log_artifact_docker_image(self, protocol, image_name):
        print(f"Getting SHA for {protocol} artifact: {image_name}")
        sha256 = self._context.sha_digest_for_docker_image(image_name)
        print(f"Calculated digest: {sha256}")
        # print("Publish artifact to ComplianceDB")
        print(f"MERKELY_IS_COMPLIANT: {self.is_compliant}")
        self._create_artifact(sha256, image_name)

    def _log_artifact_sha(self, sha256):
        artifact = self._env("MERKELY_ARTIFACT")
        index = len('file://')
        filename = artifact[index:]
        print(f"MERKELY_IS_COMPLIANT: {self.is_compliant}")
        self._create_artifact(sha256, filename)

    def _create_artifact(self, sha256, name):
        create_artifact_payload = {
            "sha256": sha256,
            "filename": name,
            "description": self.description,
            "git_commit": self.git_commit,
            "commit_url": self.commit_url,
            "build_url": self.build_url,
            "is_compliant": self.is_compliant
        }
        url = ApiSchema.url_for_artifacts(self.host, self.merkelypipe)
        http_put_payload(url, create_artifact_payload, self.api_token)

