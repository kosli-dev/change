from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class LogArtifactCommand(Command):

    def __init__(self, context):
        super().__init__(context)
        self.description = "Created by build " + self._env('MERKELY_CI_BUILD_NUMBER')
        self.git_commit = self._env('MERKELY_ARTIFACT_GIT_COMMIT')
        self.commit_url = self._env('MERKELY_ARTIFACT_GIT_URL')
        self.build_url = self._env('MERKELY_CI_BUILD_URL')
        self.is_compliant = self._env('MERKELY_IS_COMPLIANT') == "TRUE"
        self.fingerprint = self._env("MERKELY_FINGERPRINT")

    def concrete_execute(self):
        FILE_PROTOCOL = "file://"
        DOCKER_PROTOCOL = "docker://"
        if self.fingerprint.startswith(FILE_PROTOCOL):
            self._log_artifact_file(self.fingerprint[len(FILE_PROTOCOL):])
        if self.fingerprint.startswith(DOCKER_PROTOCOL):
            self._log_artifact_docker_image(self.fingerprint[len(DOCKER_PROTOCOL):])

    def _log_artifact_file(self, filename):
        pathed_filename = '/' + filename
        print("Getting SHA for file:// artifact: " + pathed_filename)
        sha256 = self._context['sha_digest_for_file'](pathed_filename)
        print("Calculated digest: " + sha256)
        # print("Publish artifact to ComplianceDB")
        print('MERKELY_IS_COMPLIANT: ' + str(self.is_compliant))
        self._create_artifact(sha256, pathed_filename)

    def _log_artifact_docker_image(self, image_name):
        print("Getting SHA for docker:// artifact: " + image_name)
        sha256 = self._context['sha_digest_for_docker_image'](image_name)
        print("Calculated digest: " + sha256)
        # print("Publish artifact to ComplianceDB")
        print('MERKELY_IS_COMPLIANT: ' + str(self.is_compliant))
        self._create_artifact(sha256, image_name)

    def _create_artifact(self, sha256, filename):
        create_artifact_payload = {
            "sha256": sha256,
            "filename": filename,
            "description": self.description,
            "git_commit": self.git_commit,
            "commit_url": self.commit_url,
            "build_url": self.build_url,
            "is_compliant": self.is_compliant
        }
        url = ApiSchema.url_for_artifacts(self.host, self.merkelypipe)
        http_put_payload(url, create_artifact_payload, self.api_token)

