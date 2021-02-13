from commands import Command, CommandError, Context
from env_vars import FingerprintEnvVar
from tests.utils import *
from pytest import raises

SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_docker_protocol_properties():
    protocol = "docker://"
    image_name = "acme/road-runner:4.5"
    fingerprint = f"{protocol}/{image_name}"
    ev = make_fingerprint_env_var(fingerprint)
    assert ev.protocol == protocol
    assert ev.artifact_name == image_name
    assert ev.artifact_basename == image_name


def test_file_protocol__file_in_root_dir_properties():
    protocol = "file://"
    filename = "jam.jar"
    fingerprint = f"{protocol}/{filename}"
    ev = make_fingerprint_env_var(fingerprint)
    assert ev.protocol == protocol
    assert ev.artifact_name == filename
    assert ev.artifact_basename == filename


def test_file_protocol__file_in_sub_dir_properties():
    protocol = "file://"
    directory = "/user/data"
    filename = "jam.jar"
    fingerprint = f"{protocol}/{directory}/{filename}"
    ev = make_fingerprint_env_var(fingerprint)
    assert ev.protocol == protocol
    assert ev.artifact_name == f"{directory}/{filename}"
    assert ev.artifact_basename == filename


def test_unknown_protocol__all_properties_raise():
    def assert_raises(unknown_protocol, property_name):
        fingerprint = f"{unknown_protocol}{SHA256}/jam.jar"
        ev = make_fingerprint_env_var(fingerprint)
        with raises(CommandError) as exc:
            getattr(ev, property_name)
        assert str(exc.value) == f"Unknown protocol: {fingerprint}"

    for protocol in ['ash256://', 'not_even_a_colon']:
        assert_raises(protocol, 'value')
        assert_raises(protocol, 'protocol')
        assert_raises(protocol, 'sha')
        assert_raises(protocol, 'artifact_name')


def make_fingerprint_env_var(fingerprint):
    env = {"MERKELY_FINGERPRINT": fingerprint}
    context = Context(env, None, None)
    command = Command(context)
    return FingerprintEnvVar(command)
