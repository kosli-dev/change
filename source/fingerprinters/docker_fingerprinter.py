from errors import ChangeError
from fingerprinters import Fingerprinter
import docker
import requests

PROTOCOL = 'docker://'

NOTES = " ".join([
    f'To fingerprint a docker image use the string `{PROTOCOL}`',
    'followed by the name+tag of the docker image.',
    'The command uses the docker daemon to query the repoDigest of the docker image.',
    'The docker socket must be volume-mounted.',
    'The image must have been pushed to a registry.'
])

EXAMPLE = "\n".join([
    'docker run \\',
    '    ...',
    f'    --env MERKELY_FINGERPRINT=”{PROTOCOL}${{YOUR_DOCKER_IMAGE_AND_TAG}}" \\',
    '    --volume /var/run/docker.sock:/var/run/docker.sock \\',
    '    ...',
])


class DockerFingerprinter(Fingerprinter):

    @property
    def notes(self):
        return NOTES

    @property
    def example(self):
        return EXAMPLE

    def handles_protocol(self, string):
        return string.startswith(PROTOCOL)

    def artifact_basename(self, string):
        return self.artifact_name(string)

    def artifact_name(self, string):
        assert self.handles_protocol(string)
        result = string[len(PROTOCOL):].rstrip()  # Postel's Law
        if result == "":
            raise ChangeError(f"Empty {PROTOCOL} fingerprint")
        return result

    def sha(self, string):
        assert self.handles_protocol(string)
        image_name = self.artifact_name(string)
        # Mocked in /tests/unit/utils/mock_docker_fingerprinter.py
        # docker is a Python package installed in requirements.txt
        try:
            client = docker.from_env()
            image = client.images.get(image_name)
            return image.attrs["RepoDigests"][0].split(":")[1]
        except (docker.errors.ImageNotFound, requests.exceptions.HTTPError, IndexError):
            # For example, see
            # https://github.com/merkely-development/loan-calculator/runs/1903030144?check_suite_focus=true
            message = " ".join([
                f"Cannot determine digest for image: {image_name}",
                "Check the image name is correct.",
                "Check the image has been pushed to a registry."
            ])
            raise ChangeError(message)


