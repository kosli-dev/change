from commands import Command, CommandError, Context
from env_vars import FingerprintEnvVar
from tests.utils import *
from pytest import raises

SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_sha_test_data():
    assert len(SHA256) == 64
    assert int(SHA256, 16) == 100382238559844117107660713596747001062775806001626650114972777586704962769372


def test_docker_protocol():
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


def test_file_protocol():
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


def test_sha_protocol():
    protocol = "sha256://"
    artifact_name = "acme/road-runner:2.34"
    fingerprint = f"{protocol}{SHA256}/{artifact_name}"
    env = {
        "MERKELY_FINGERPRINT": fingerprint
    }
    context = Context(env, None, None)
    command = Command(context)

    fev = FingerprintEnvVar(command)

    assert fev.value == fingerprint
    assert fev.protocol == protocol
    assert fev.sha == SHA256
    assert fev.artifact_name == artifact_name


def test_sha256_protocol__bad_sha256_raises():
    bad_shas = [
        "",   # empty
        'a',  # too short by a lot
        SHA256[0:-1],  # too short by 1
        SHA256+'0',  # too long
        SHA256[0:-1]+'F'  # lowercase f only
    ]
    for bad_sha in bad_shas:
        protocol = "sha256://"
        artifact_name = "acme/road-runner:2.34"
        fingerprint = f"{protocol}{bad_sha}/{artifact_name}"
        env = {
            "MERKELY_FINGERPRINT": fingerprint
        }
        context = Context(env, None, None)
        command = Command(context)
        fev = FingerprintEnvVar(command)
        with raises(CommandError) as exc:
            fev.sha
        #assert str(exc.value) == 'xxxx'


def test_sha256_protocol__bad_artifact_name_raises():
    # artifact_name empty raises
    pass


def test_unknown_protocol_raises():
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
        fev.sha
    assert str(exc.value) == f"Unknown protocol: {fingerprint}"

    with raises(CommandError) as exc:
        fev.artifact_name
    assert str(exc.value) == f"Unknown protocol: {fingerprint}"
