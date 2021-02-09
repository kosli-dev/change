from commands import Command, CommandError, Context
from env_vars import FingerprintEnvVar
from tests.utils import *
from pytest import raises

FILE_PROTOCOL = "file://"
SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_file_protocol__non_empty_filename_properties():
    filename = "/user/artifact/jam.jar"
    ev, fingerprint = make_fingerprint_env_var(filename)
    assert ev.protocol == FILE_PROTOCOL
    assert ev.value == fingerprint
    assert ev.artifact_name == filename
    assert ev.sha == SHA256


def test_file_protocol__empty_filename_raises():
    filename = ""
    ev, _ = make_fingerprint_env_var(filename)

    def assert_raises(property_name):
        with raises(CommandError) as exc:
            getattr(ev, property_name)
        assert str(exc.value) == f"Empty {FILE_PROTOCOL} fingerprint"

    assert ev.protocol == FILE_PROTOCOL
    assert_raises('value')
    assert_raises('artifact_name')
    assert_raises('sha')


def make_fingerprint_env_var(filename):
    fingerprint = f"{FILE_PROTOCOL}{filename}"
    env = {"MERKELY_FINGERPRINT": fingerprint}
    fingerprinter = MockFileFingerprinter(filename, SHA256)
    context = Context(env, None, fingerprinter)
    command = Command(context)
    return FingerprintEnvVar(command), fingerprint
