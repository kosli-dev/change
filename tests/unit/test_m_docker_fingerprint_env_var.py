from commands import Command, CommandError, Context
from env_vars import FingerprintEnvVar, DockerFingerprintEnvVar
from tests.utils import *
from pytest import raises

DOCKER_PROTOCOL = "docker://"
SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_docker_protocol__non_empty_image_name_properties():
    image_name = "acme/road-runner:4.8"
    ev, fingerprint = make_fingerprint_env_var(image_name)
    assert ev.protocol == DOCKER_PROTOCOL
    assert ev.value == fingerprint
    assert ev.artifact_name == image_name
    assert ev.sha == SHA256


def test_docker_protocol__empty_image_name_raises():
    image_name = ""
    ev, _ = make_fingerprint_env_var(image_name)

    def assert_raises(property_name):
        with raises(CommandError) as exc:
            getattr(ev, property_name)
        assert str(exc.value) == f"Empty {DOCKER_PROTOCOL} fingerprint"

    assert ev.protocol == DOCKER_PROTOCOL
    assert_raises('value')
    assert_raises('artifact_name')
    assert_raises('sha')


def test_notes_is_not_empty():
    ev = DockerFingerprintEnvVar(None, None, None)
    assert len(ev.notes) > 0


def make_fingerprint_env_var(image_name):
    fingerprint = f"{DOCKER_PROTOCOL}{image_name}"
    env = {"MERKELY_FINGERPRINT": fingerprint}
    fingerprinter = MockDockerFingerprinter(image_name, SHA256)
    context = Context(env, fingerprinter, None)
    command = Command(context)
    return FingerprintEnvVar(command), fingerprint
