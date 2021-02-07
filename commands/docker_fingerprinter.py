from commands import Fingerprinter
import docker


class DockerFingerprinter(Fingerprinter):

    def _fingerprint(self, image_name):
        # Mocked in /tests/unit/utils/mock_docker_fingerprinter.py
        # docker is a Python package installed in requirements.txt
        client = docker.from_env()
        image = client.images.get(image_name)
        return image.attrs["RepoDigests"][0].split(":")[1]

