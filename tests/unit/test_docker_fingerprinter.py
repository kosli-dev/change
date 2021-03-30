from errors import ChangeError
from fingerprinters import DockerFingerprinter
from pytest import raises
import docker

DOCKER_PROTOCOL = "docker://"


class DockerImagesGetAttrStub:
    def __init__(self, repo_digests):
        self._repo_digests = repo_digests
    @property
    def images(self):
        stubber = self
        class Getter:
            def get(self, _image_name):
                class Attrs:
                    @property
                    def attrs(self):
                        return {
                            "RepoDigests": stubber._repo_digests
                        }
                return Attrs()
        return Getter()


class DockerImageNotFoundStub:
    @property
    def images(self):
        raise docker.errors.ImageNotFound("")


def test_gets_sha_when_image_retrieved_from_registry(mocker):
    sha256 = '13032d90afaaa111e92920eea2b1abb0a6b6eafa6863ad7a4bd082a9c8574240'
    stub = DockerImagesGetAttrStub([f"acme@sha256:{sha256}"])
    mocker.patch('fingerprinters.docker_fingerprinter.docker.from_env', return_value=stub)
    image_name = 'acme/road-runner:3.7'
    fingerprinter = DockerFingerprinter()
    assert fingerprinter.sha(f"{DOCKER_PROTOCOL}{image_name}") == sha256


def test_fails_to_get_sha_when_image_not_retrieved_from_registry(mocker):
    stub = DockerImagesGetAttrStub([])
    mocker.patch('fingerprinters.docker_fingerprinter.docker.from_env', return_value=stub)

    fingerprinter = DockerFingerprinter()
    image_name = 'acme/road-runner:3.7'
    with raises(ChangeError) as exc:
        fingerprinter.sha(f"{DOCKER_PROTOCOL}{image_name}")

    start = f"Cannot determine digest for image: {image_name}"
    diagnostic = str(exc.value)
    assert diagnostic.startswith(start), diagnostic


def test_fails_to_get_sha_when_image_does_not_exist(mocker):
    stub = DockerImageNotFoundStub()
    mocker.patch('fingerprinters.docker_fingerprinter.docker.from_env', return_value=stub)

    fingerprinter = DockerFingerprinter()
    image_name = 'acme/road-runner:3.7'
    with raises(ChangeError) as exc:
        fingerprinter.sha(f"{DOCKER_PROTOCOL}{image_name}")

    start = f"Cannot determine digest for image: {image_name}"
    diagnostic = str(exc.value)
    assert diagnostic.startswith(start), diagnostic


def test_handles_only_its_own_protocol():
    fingerprinter = DockerFingerprinter()
    assert fingerprinter.handles_protocol(DOCKER_PROTOCOL)
    assert not fingerprinter.handles_protocol('X'+DOCKER_PROTOCOL)


def test_non_empty_image_name_properties():
    fingerprinter = DockerFingerprinter()
    image_name = "acme/road-runner:4.8"
    string = DOCKER_PROTOCOL + image_name
    assert fingerprinter.artifact_name(string) == image_name
    assert fingerprinter.artifact_basename(string) == image_name


def test_notes_and_example_docs_are_set():
    fingerprinter = DockerFingerprinter()
    assert len(fingerprinter.notes) > 0
    assert len(fingerprinter.example) > 0


def test_empty_image_name_raises():
    fingerprinter = DockerFingerprinter()
    image_name = ""
    string = DOCKER_PROTOCOL + image_name

    def assert_raises_empty_image(method_name):
        with raises(ChangeError) as exc:
            getattr(fingerprinter, method_name)(string)
        assert str(exc.value) == f"Empty {DOCKER_PROTOCOL} fingerprint"

    assert_raises_empty_image('artifact_name')
    assert_raises_empty_image('artifact_basename')
    assert_raises_empty_image('sha')


def test_trailing_whitespace_is_stripped_from_image_name():
    fingerprinter = DockerFingerprinter()
    image_name = " " * 4
    string = DOCKER_PROTOCOL + image_name

    def assert_raises_empty_image(method_name):
        with raises(ChangeError) as exc:
            getattr(fingerprinter, method_name)(string)
        assert str(exc.value) == f"Empty {DOCKER_PROTOCOL} fingerprint"

    assert_raises_empty_image('sha')
