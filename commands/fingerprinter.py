from .command_error import CommandError
import docker
import os
import subprocess


class Fingerprinter:

    DOCKER_PROTOCOL = "docker://"
    FILE_PROTOCOL = "file://"
    SHA256_PROTOCOL = "sha256://"

    def fingerprint(self, command):
        env_var = command.fingerprint
        if env_var.value.startswith(self.FILE_PROTOCOL):
            return self._file(env_var)
        elif env_var.value.startswith(self.DOCKER_PROTOCOL):
            return self._docker(env_var)
        elif env_var.value.startswith(self.SHA256_PROTOCOL):
            return self._sha256(env_var, command)
        else:
            raise CommandError(f"{env_var.name} has unknown protocol {env_var.value}")

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

    def _sha256(self, env_var, command):
        sha256 = self._after(self.SHA256_PROTOCOL, env_var)
        return sha256, command.display_name.value

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
