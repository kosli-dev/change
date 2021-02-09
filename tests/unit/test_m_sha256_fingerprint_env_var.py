from commands import Command, CommandError, Context
from env_vars import FingerprintEnvVar
from tests.utils import *
from pytest import raises
import re

SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_sha_protocol__good():
    protocol = "sha256://"
    image_name = "acme/road-runner:2.34"
    fingerprint = f"{protocol}{SHA256}/{image_name}"
    env = {"MERKELY_FINGERPRINT": fingerprint}
    context = Context(env, None, None)
    command = Command(context)
    fev = FingerprintEnvVar(command)
    assert fev.value == fingerprint
    assert fev.protocol == protocol
    assert fev.sha == SHA256
    assert fev.artifact_name == image_name


def test_sha256_protocol__bad_sha_value_raises():
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
        protocol = "sha256://"
        image_name = "acme/road-runner:2.34"
        env = {"MERKELY_FINGERPRINT": f"{protocol}{bad_sha}/{image_name}"}
        context = Context(env, None, None)
        command = Command(context)
        fev = FingerprintEnvVar(command)
        with raises(CommandError) as exc:
            fev.sha
        assert str(exc.value) == f"Invalid sha256:// fingerprint: {bad_sha}/{image_name}"


def test_sha256_protocol__no_artifact_name_raises():
    no_slash = ''
    empty = '/'
    for bad in [no_slash, empty]:
        protocol = 'sha256://'
        fingerprint = f"{protocol}{SHA256}{bad}"
        env = {"MERKELY_FINGERPRINT": fingerprint}
        context = Context(env, None, None)
        command = Command(context)
        fev = FingerprintEnvVar(command)
        with raises(CommandError) as exc:
            fev.artifact_name
        assert str(exc.value) == f"Invalid sha256:// fingerprint: {SHA256}{bad}"
