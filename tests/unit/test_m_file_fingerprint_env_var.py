from commands import Command, CommandError, Context
from env_vars import FingerprintEnvVar
from tests.utils import *
from pytest import raises
import re

SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_file_protocol__good():
    protocol = "file://"
    filename = "/user/artifact/jam.jar"
    fingerprint = f"{protocol}{filename}"
    env = {"MERKELY_FINGERPRINT": fingerprint}
    fingerprinter = MockFileFingerprinter(filename, SHA256)
    context = Context(env, None, fingerprinter)
    command = Command(context)
    fev = FingerprintEnvVar(command)
    assert fev.value == fingerprint
    assert fev.protocol == protocol
    assert fev.artifact_name == filename
    assert fev.sha == SHA256


def test_file_protocol__empty_filename_raises():
    protocol = "file://"
    filename = ""
    env = {"MERKELY_FINGERPRINT": f"{protocol}{filename}"}
    context = Context(env, None, None)
    command = Command(context)
    fev = FingerprintEnvVar(command)

    assert fev.protocol == protocol

    expected_diagnostic = "Empty file:// fingerprint"

    with raises(CommandError) as exc:
        fev.value
    assert str(exc.value) == expected_diagnostic

    with raises(CommandError) as exc:
        fev.artifact_name
    assert str(exc.value) == expected_diagnostic

