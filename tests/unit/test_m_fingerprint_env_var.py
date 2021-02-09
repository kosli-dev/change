from commands import Command, CommandError, Context
from env_vars import FingerprintEnvVar
from tests.utils import *
from pytest import raises

SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_unknown_protocol__all_properties_raise():
    fingerprint = f"ash256://{SHA256}"
    env = {"MERKELY_FINGERPRINT": fingerprint}
    context = Context(env, None, None)
    command = Command(context)
    fev = FingerprintEnvVar(command)

    expected_diagnostic = f"Unknown protocol: {fingerprint}"

    with raises(CommandError) as exc:
        fev.value
    assert str(exc.value) == expected_diagnostic

    with raises(CommandError) as exc:
        fev.protocol
    assert str(exc.value) == expected_diagnostic

    with raises(CommandError) as exc:
        fev.sha
    assert str(exc.value) == expected_diagnostic

    with raises(CommandError) as exc:
        fev.artifact_name
    assert str(exc.value) == expected_diagnostic
