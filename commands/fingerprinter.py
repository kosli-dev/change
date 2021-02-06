from .command_error import CommandError
import docker
import os
import subprocess


class Fingerprinter:

    DOCKER_PROTOCOL = "docker://"
    FILE_PROTOCOL = "file://"
    SHA256_PROTOCOL = "sha256://"

    def __call__(self, env_vars):
        fingerprint = env_vars.fingerprint
        if fingerprint.value.startswith(self.FILE_PROTOCOL):
            return self._file(fingerprint)
        elif fingerprint.value.startswith(self.DOCKER_PROTOCOL):
            return self._docker(fingerprint)
        elif fingerprint.value.startswith(self.SHA256_PROTOCOL):
            return self._sha256(fingerprint), env_vars.display_name.value
        else:
            raise CommandError(f"{fingerprint.name} has unknown protocol {fingerprint.value}")

    def _file(self, env_var):
        pathed_filename = self._after(self.FILE_PROTOCOL, env_var)
        print(f"Getting SHA for {self.FILE_PROTOCOL} artifact: {pathed_filename}")
        sha256 = self._fingerprint_file(pathed_filename)
        print(f"Calculated digest: {sha256}")
        return sha256, os.path.basename(pathed_filename)

    def _docker(self, env_var):
        image_name = self._after(self.DOCKER_PROTOCOL, env_var)
        print(f"Getting SHA for {self.DOCKER_PROTOCOL} artifact: {image_name}")
        repo_digest = self._fingerprint_image(image_name)
        print(f"Calculated digest: {repo_digest}")
        return repo_digest, image_name

    def _sha256(self, env_var):
        sha256 = self._after(self.SHA256_PROTOCOL, env_var)
        return sha256

    def _after(self, protocol, env_var):
        return env_var.value[len(protocol):]

    def _fingerprint_file(self, pathed_filename):
        output = subprocess.check_output(["openssl", "dgst", "-sha256", '/'+pathed_filename])
        digest_in_bytes = output.split()[1]
        sha256 = digest_in_bytes.decode('utf-8')
        return sha256

    def _fingerprint_image(self, image_name):
        client = docker.from_env()
        image = client.images.get(image_name)
        repo_digest = image.attrs["RepoDigests"][0].split(":")[1]
        return repo_digest
