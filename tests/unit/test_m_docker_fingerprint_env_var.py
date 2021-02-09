from commands import Command, CommandError, Context
from env_vars import FingerprintEnvVar
from tests.utils import *
from pytest import raises
import re

SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_docker_protocol__good():
    protocol = "docker://"
    image_name = "acme/road-runner:4.8"
    fingerprint = f"{protocol}{image_name}"
    env = {"MERKELY_FINGERPRINT": fingerprint}
    fingerprinter = MockDockerFingerprinter(image_name, SHA256)
    context = Context(env, fingerprinter, None)
    command = Command(context)
    fev = FingerprintEnvVar(command)
    assert fev.value == fingerprint
    assert fev.protocol == protocol
    assert fev.artifact_name == image_name
    assert fev.sha == SHA256


def test_docker_protocol__empty_image_name_raises():
    protocol = "docker://"
    image_name = ""
    env = {"MERKELY_FINGERPRINT": f"{protocol}{image_name}"}
    context = Context(env, None, None)
    command = Command(context)
    fev = FingerprintEnvVar(command)

    assert fev.protocol == protocol

    expected_diagnostic = f"Empty docker:// fingerprint"

    with raises(CommandError) as exc:
        fev.value
    assert str(exc.value) == expected_diagnostic

    with raises(CommandError) as exc:
        fev.artifact_name
    assert str(exc.value) == expected_diagnostic
