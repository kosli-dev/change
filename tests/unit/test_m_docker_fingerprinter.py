from commands import CommandError
from fingerprinters import DockerFingerprinter
from pytest import raises

DOCKER_PROTOCOL = "docker://"


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


def test_empty_image_name_raises():
    fingerprinter = DockerFingerprinter()
    image_name = ""
    string = DOCKER_PROTOCOL + image_name
    def assert_raises(method_name):
        with raises(CommandError) as exc:
            getattr(fingerprinter, method_name)(string)
        assert str(exc.value) == f"Empty {DOCKER_PROTOCOL} fingerprint"

    assert_raises('artifact_name')
    assert_raises('artifact_basename')
    assert_raises('sha')
