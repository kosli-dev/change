from collections import namedtuple
from commands import CommandError, Fingerprinter, RequiredEnvVar

from tests.utils import ScopedEnvVars
from pytest import raises

# TODO: test_sha256 and SHA does not look like a SHA?
# TODO: test_sha256 when DISPLAY_NAME is missing
# TODO: test_sha256 when supplied DISPLAY_NAME has full path...?

# TODO: Test when docker image not found (error message)
# TODO: Test when image not pushed (eg to dockerhub) so cannot get digest (error message)
# TODO: Test when docker socket not volume-mounted (error message)


def test_unknown_protocol(capsys):
    fingerprint = "ash256://ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    image_name = "acme/road-runner:4.8"

    set_env_vars = {
        "MERKELY_FINGERPRINT": fingerprint,
        "MERKELY_DISPLAY_NAME": image_name
    }
    with ScopedEnvVars(set_env_vars) as ev, raises(CommandError) as exc:
        Fingerprinter()(make_env_vars(ev))

    expected_message = f"MERKELY_FINGERPRINT has unknown protocol {fingerprint}"
    assert str(exc.value) == expected_message


def make_env_vars(env):
    return namedtuple('EnvVars', (
        'fingerprint',
        'display_name'
    ))(
        RequiredEnvVar('MERKELY_FINGERPRINT', env, "description"),
        RequiredEnvVar('MERKELY_DISPLAY_NAME', env, "description")
    )
