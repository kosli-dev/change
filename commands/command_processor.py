from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload
import json


def execute(context):
    command = context['env'].get("MERKELY_COMMAND", None)
    if command == "declare_pipeline":
        DeclarePipelineCommand(context).execute()
    if command == "log_artifact":
        LogArtifactCommand(context).execute()
    return 0


class Command:

    def __init__(self, context):
        self._context = context

    def execute(self):
        print("MERKELY_COMMAND={}".format(self.command))
        self.concrete_execute()

    @property
    def command(self):
        return self._env("MERKELY_COMMAND")

    @property
    def api_token(self):
        return self._env("MERKELY_API_TOKEN")

    @property
    def host(self):
        return self._env("MERKELY_HOST")

    @property
    def merkelypipe(self):
        MERKELYPIPE_PATH = "/Merkelypipe.json"
        with open(MERKELYPIPE_PATH) as file:
            return json.load(file)

    def _env(self, name):
        return self._context['env'].get(name, None)


class DeclarePipelineCommand(Command):

    def concrete_execute(self):
        pipelines_url = ApiSchema.url_for_pipelines(self.host, self.merkelypipe)
        http_put_payload(url=pipelines_url, payload=self.merkelypipe, api_token=self.api_token)


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
        create_artifact(self.api_token, self.host, self.merkelypipe,
                        artifact_sha, pathed_filename,
                        context['description'],
                        context['git_commit'],
                        context['commit_url'],
                        context['build_url'],
                        context['is_compliant'])

    def _log_artifact_docker_image(self, image_name):
        context = self._context
        print("Getting SHA for docker:// artifact: " + image_name)
        artifact_sha = context['sha_digest_for_docker_image'](image_name)
        print("Calculated digest: " + artifact_sha)
        # print("Publish artifact to ComplianceDB")
        print('MERKELY_IS_COMPLIANT: ' + str(context['is_compliant']))
        create_artifact(self.api_token, self.host, self.merkelypipe,
                        artifact_sha, image_name,
                        context['description'],
                        context['git_commit'],
                        context['commit_url'],
                        context['build_url'],
                        context['is_compliant'])



def create_artifact(api_token, host, merkelypipe,
                    sha256, filename,
                    description, git_commit, commit_url, build_url, is_compliant):
    create_artifact_payload = {
        "sha256": sha256,
        "filename": filename,
        "description": description,
        "git_commit": git_commit,
        "commit_url": commit_url,
        "build_url": build_url,
        "is_compliant": is_compliant
    }
    url = ApiSchema.url_for_artifacts(host, merkelypipe)
    http_put_payload(url, create_artifact_payload, api_token)
