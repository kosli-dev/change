from fingerprinters import Fingerprinter
import docker

PROTOCOL = 'docker://'


class DockerFingerprinter(Fingerprinter):

    @property
    def notes(self):
        return "\n".join([
            f'The string `{PROTOCOL}` followed by the name+tag of the docker image to fingerprint.',
            'The docker socket must be volume-mounted.',
            'Example:',
            'docker run ... \\',
            f'    --env MERKELY_FINGERPRINT=”{PROTOCOL}${{YOUR_DOCKER_IMAGE_AND_TAG}}" \\',
            '    --volume /var/run/docker.sock:/var/run/docker.sock \\',
            '    ...',
        ])

    @property
    def protocol(self):
        return PROTOCOL

    def handles_protocol(self, string):
        return string.startswith(PROTOCOL)

    def artifact_basename(self, string):
        return self.artifact_name(string)

    def artifact_name(self, string):
        assert self.handles_protocol(string)
        return string[len(PROTOCOL):]

    def sha(self, image_name):
        # Mocked in /tests/unit/utils/mock_docker_fingerprinter.py
        # docker is a Python package installed in requirements.txt
        client = docker.from_env()
        image = client.images.get(image_name)
        return image.attrs["RepoDigests"][0].split(":")[1]

