import docker
import subprocess


class Fingerprinter:

    def of_file(self, pathed_filename):
        output = subprocess.check_output(["openssl", "dgst", "-sha256", pathed_filename])
        digest_in_bytes = output.split()[1]
        sha256 = digest_in_bytes.decode('utf-8')
        return sha256

    def of_docker_image(self, docker_image_name):
        client = docker.from_env()
        print("Inspecting docker image for sha256Digest")
        image = client.images.get(docker_image_name)
        repo_digest = image.attrs["RepoDigests"][0].split(":")[1]
        return repo_digest

