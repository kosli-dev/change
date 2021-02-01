import docker
import os
import subprocess


class Context:
    """
    Holds (some) external dependencies to make Classic style testing easier.
    """
    @property
    def env(self):
        return os.environ

    def sha_digest_for_file(self, pathed_filename):
        output = subprocess.check_output(["openssl", "dgst", "-sha256", pathed_filename])
        digest_in_bytes = output.split()[1]
        artifact_sha = digest_in_bytes.decode('utf-8')
        return artifact_sha

    def sha_digest_for_docker_image(self, docker_image_name):
        client = docker.from_env()
        print("Inspecting docker image for sha256Digest")
        image = client.images.get(docker_image_name)
        repo_digest = image.attrs["RepoDigests"][0].split(":")[1]
        return repo_digest

