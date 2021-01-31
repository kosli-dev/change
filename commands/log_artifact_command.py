from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class LogArtifactCommand(Command):

    def concrete_execute(self):
        fingerprint = self._env("MERKELY_FINGERPRINT")
        context = self._context
        context['description'] = "Created by build " + self._env('MERKELY_CI_BUILD_NUMBER')
        context['git_commit'] = self._env('MERKELY_ARTIFACT_GIT_COMMIT')
        context['commit_url'] = self._env('MERKELY_ARTIFACT_GIT_URL')
        context['build_url'] = self._env('MERKELY_CI_BUILD_URL')
        context['is_compliant'] = self._env('MERKELY_IS_COMPLIANT') == "TRUE"

        FILE_PROTOCOL = "file://"
        if fingerprint.startswith(FILE_PROTOCOL):
            self._log_artifact_file(fingerprint[len(FILE_PROTOCOL):])

        DOCKER_PROTOCOL = "docker://"
        if fingerprint.startswith(DOCKER_PROTOCOL):
            self._log_artifact_docker_image(fingerprint[len(DOCKER_PROTOCOL):])

    def _log_artifact_file(self, filename):
        context = self._context
        pathed_filename = '/' + filename
        print("Getting SHA for file:// artifact: " + pathed_filename)
        artifact_sha = context['sha_digest_for_file'](pathed_filename)
        print("Calculated digest: " + artifact_sha)
        # print("Publish artifact to ComplianceDB")
        print('MERKELY_IS_COMPLIANT: ' + str(context['is_compliant']))
        self._create_artifact(artifact_sha, pathed_filename)

    def _log_artifact_docker_image(self, image_name):
        context = self._context
        print("Getting SHA for docker:// artifact: " + image_name)
        artifact_sha = context['sha_digest_for_docker_image'](image_name)
        print("Calculated digest: " + artifact_sha)
        # print("Publish artifact to ComplianceDB")
        print('MERKELY_IS_COMPLIANT: ' + str(context['is_compliant']))
        self._create_artifact(artifact_sha, image_name)

    def _create_artifact(self, sha256, filename):
        context = self._context
        create_artifact_payload = {
            "sha256": sha256,
            "filename": filename,
            "description": context['description'],
            "git_commit": context['git_commit'],
            "commit_url": context['commit_url'],
            "build_url": context['build_url'],
            "is_compliant": context['is_compliant']
        }
        url = ApiSchema.url_for_artifacts(self.host, self.merkelypipe)
        http_put_payload(url, create_artifact_payload, self.api_token)

