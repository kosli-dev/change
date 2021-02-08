from commands import Command, CommandError, Context
from env_vars import FingerprintEnvVar
from tests.utils import *
from pytest import raises

SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_docker_protocol(capsys):
    protocol = "docker://"
    artifact_name = "acme/road-runner:4.8"
    fingerprint = f"{protocol}{artifact_name}"
    env = {
        "MERKELY_FINGERPRINT": fingerprint
    }
    fingerprinter = MockDockerFingerprinter(artifact_name, SHA256)
    context = Context(env, fingerprinter, None)
    command = Command(context)

    fev = FingerprintEnvVar(command)

    assert fev.value == fingerprint
    assert fev.protocol == protocol
    assert fev.artifact_name == artifact_name
    assert fev.sha == SHA256

    capsys_read(capsys)


def test_file_protocol(capsys):
    protocol = "file://"
    artifact_name = "/user/artifact/jam.jar"
    fingerprint = f"{protocol}{artifact_name}"
    env = {
        "MERKELY_FINGERPRINT": fingerprint
    }
    fingerprinter = MockFileFingerprinter(artifact_name, SHA256)
    context = Context(env, None, fingerprinter)
    command = Command(context)

    fev = FingerprintEnvVar(command)

    assert fev.value == fingerprint
    assert fev.protocol == protocol
    assert fev.artifact_name == artifact_name
    assert fev.sha == SHA256

    capsys_read(capsys)


def test_sha_protocl(capsys):
    protocol = "sha256://"
    artifact_name = SHA256
    fingerprint = f"{protocol}{artifact_name}"
    env = {
        "MERKELY_FINGERPRINT": fingerprint
    }
    context = Context(env, None, None)
    command = Command(context)

    fev = FingerprintEnvVar(command)

    assert fev.value == fingerprint
    assert fev.protocol == protocol
    assert fev.artifact_name == SHA256
    assert fev.sha == SHA256

    capsys_read(capsys)  # TODO


def test_unknown_protocol(capsys):
    protocol = "ash256://"
    artifact_name = SHA256
    fingerprint = f"{protocol}{artifact_name}"
    env = {
        "MERKELY_FINGERPRINT": fingerprint
    }
    context = Context(env, None, None)
    command = Command(context)
    fev = FingerprintEnvVar(command)

    assert fev.value == fingerprint

    with raises(CommandError) as exc:
        fev.protocol
    assert str(exc.value) == f"Unknown protocol: {fingerprint}"

    with raises(CommandError) as exc:
        fev.artifact_name
    assert str(exc.value) == f"Unknown protocol: {fingerprint}"

    with raises(CommandError) as exc:
        fev.sha
    assert str(exc.value) == f"Unknown protocol: {fingerprint}"
