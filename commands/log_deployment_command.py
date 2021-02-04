import os
from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_post_payload


class LogDeploymentCommand(Command):
    """
    Command subclass for handling MERKELY_COMMAND=log_deployment
    """
    @property
    def args_list(self):
        return [
            self.api_token,
            self.ci_build_url,
            self.display_name,
            self.description,
            self.environment,
            self.fingerprint,
            self.host
        ]

    @property
    def ci_build_url(self):
        description = "A url for the deployment"
        return self._required_env_var('CI_BUILD_URL', description)

    @property
    def description(self):
        description = "A description for the deployment"
        return self._required_env_var('DESCRIPTION', description)

    @property
    def environment(self):
        description = "The environment the artifact is being deployed to"
        return self._required_env_var('ENVIRONMENT', description)

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
            self._log_deployment_file(file_protocol, artifact_name)
        docker_protocol = "docker://"
        if fp.startswith(docker_protocol):
            artifact_name = fp[len(docker_protocol):]
            self._log_deployment_docker_image(docker_protocol, artifact_name)
        sha_protocol = "sha256://"
        if fp.startswith(sha_protocol):
            sha256 = fp[len(sha_protocol):]
            self._log_deployment_sha(sha256)

    def _log_deployment_file(self, protocol, filename):
        print(f"Getting SHA for {protocol} artifact: {filename}")
        sha256 = self._context.sha_digest_for_file('/'+filename)
        print(f"Calculated digest: {sha256}")
        self._create_deployment(sha256, os.path.basename(filename))

    def _log_deployment_docker_image(self, protocol, image_name):
        print(f"Getting SHA for {protocol} artifact: {image_name}")
        sha256 = self._context.sha_digest_for_docker_image(image_name)
        print(f"Calculated digest: {sha256}")
        self._create_deployment(sha256, image_name)

    def _log_deployment_sha(self, sha256):
        self._create_deployment(sha256, self.display_name.value)

    def _create_deployment(self, sha256, display_name):
        payload = {
            "artifact_sha256": sha256,
            "build_url": self.ci_build_url.value,
            "description": self.description.value,
            "environment": self.environment.value,
        }
        url = ApiSchema.url_for_deployments(self.host.value, self.merkelypipe)
        http_post_payload(url, payload, self.api_token.value)
