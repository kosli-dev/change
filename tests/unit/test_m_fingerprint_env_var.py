from commands import Command, Context, CommandError
from commands import FingerprintEnvVar
from tests.utils import *

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


# Further tests
# sha256 and SHA does not look like a SHA?
# sha256 when DISPLAY_NAME is missing
# sha256 when supplied DISPLAY_NAME has full path...?

# docker image not found (error message)
# image not pushed (eg to dockerhub) so cannot get digest (error message)
# docker socket not volume-mounted (error message)
