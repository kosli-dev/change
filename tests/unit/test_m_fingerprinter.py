from collections import namedtuple
from commands import Command, CommandError, Context, Fingerprinter, RequiredEnvVar

from tests.utils import *
from pytest import raises

SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_docker_protocol():
    image_name = "acme/road-runner:4.8"

    fingerprint = f"docker://{image_name}"
    env_vars = make_env_vars(fingerprint, None)

    fingerprinter = MockImageFingerprinter(image_name, SHA256)
    expected = SHA256, image_name

    assert fingerprinter(env_vars) == expected


def test_file_protocol_for_unpathed_filename_is_at_root():
    filename = "jam.jar"

    fingerprint = f"file://{filename}"
    env_vars = make_env_vars(fingerprint, None)

    fingerprinter = MockFileFingerprinter(filename, SHA256)
    expected = SHA256, filename

    assert fingerprinter(env_vars) == expected


def test_file_protocol_for_pathed_filename_uses_display_name_of_unpathed_filename():
    directory, filename = "/user/data", "jam.jar"

    fingerprint = f"file://{directory}/{filename}"
    env_vars = make_env_vars(fingerprint, None)

    expected = SHA256, filename
    assert MockFileFingerprinter(f"{directory}/{filename}", SHA256)(env_vars) == expected


def test_unknown_protocol_raises():
    protocol = "xyz://"
    fingerprint = f"{protocol}{SHA256}"
    image_name = "acme/road-runner:4.8"
    env_vars = make_env_vars(fingerprint, image_name)

    with raises(CommandError) as exc:
        Fingerprinter()(env_vars)

    expected_message = f"MERKELY_FINGERPRINT has unknown protocol {fingerprint}"
    assert str(exc.value) == expected_message


def make_env_vars(fingerprint, display_name):
    env = {}
    if fingerprint is not None:
        env["MERKELY_FINGERPRINT"] = fingerprint
    if display_name is not None:
        env["MERKELY_DISPLAY_NAME"] = display_name

    command = Command(Context(env))
    description = ""
    return namedtuple('EnvVars', (
        'fingerprint',
        'display_name'
    ))(
        RequiredEnvVar(command, 'MERKELY_FINGERPRINT', description),
        RequiredEnvVar(command, 'MERKELY_DISPLAY_NAME', description)
    )

# Further tests
# sha256 and SHA does not look like a SHA?
# sha256 when DISPLAY_NAME is missing
# sha256 when supplied DISPLAY_NAME has full path...?

# docker image not found (error message)
# image not pushed (eg to dockerhub) so cannot get digest (error message)
# docker socket not volume-mounted (error message)
