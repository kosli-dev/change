from commands import Command, CommandError, Context
from env_vars import FingerprintEnvVar, Sha256FingerprintEnvVar
from tests.utils import *
from pytest import raises

SHA256_PROTOCOL = 'sha256://'
SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_sha256_protocol__valid_sha_and_non_empty_artifact_name_properties():
    image_name = "acme/road-runner:2.34"
    ev, fingerprint = make_fingerprint_env_var(SHA256, '/'+image_name)
    assert ev.value == fingerprint
    assert ev.protocol == SHA256_PROTOCOL
    assert ev.sha == SHA256
    assert ev.artifact_name == image_name


def test_sha256_protocol__bad_sha_raises():
    bad_shas = [
        "",   # empty
        'a',  # too short by a lot
        SHA256[0:-1],  # too short by 1
        SHA256+'0',  # too long by 1
        SHA256+'0123456789abcdef',  # too long by a lot
        SHA256[0:-1]+'F',  # bad last char
        'E'+SHA256[1:],  # bad first char
        ('4'*32) + 'B' + ('5'*31),  # bad middle char
    ]
    for bad_sha in bad_shas:
        image_name = "acme/road-runner:2.34"
        ev, fingerprint = make_fingerprint_env_var(bad_sha, image_name)
        with raises(CommandError) as exc:
            ev.sha
        assert str(exc.value) == f"Invalid {SHA256_PROTOCOL} fingerprint: {bad_sha}{image_name}"


def test_sha256_protocol__no_artifact_name_raises():
    no_slash = ''
    empty = '/'
    for bad in [no_slash, empty]:
        ev, _fingerprint = make_fingerprint_env_var(SHA256, bad)
        with raises(CommandError) as exc:
            ev.artifact_name
        assert str(exc.value) == f"Invalid {SHA256_PROTOCOL} fingerprint: {SHA256}{bad}"


def make_fingerprint_env_var(sha256, artifact_name):
    fingerprint = f"{SHA256_PROTOCOL}{sha256}{artifact_name}"
    env = {"MERKELY_FINGERPRINT": fingerprint}
    context = Context(env, None, None)
    command = Command(context)
    return FingerprintEnvVar(command), fingerprint
