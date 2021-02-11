from commands import Command, CommandError, Context
from env_vars import FingerprintEnvVar
from tests.utils import *
from pytest import raises

SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_unknown_protocol__all_properties_raise():
    def assert_raises(unknown_protocol, property_name):
        fingerprint = f"{unknown_protocol}{SHA256}/jam.jar"
        env = {"MERKELY_FINGERPRINT": fingerprint}
        context = Context(env, None, None)
        command = Command(context)
        ev = FingerprintEnvVar(command)
        with raises(CommandError) as exc:
            getattr(ev, property_name)
        assert str(exc.value) == f"Unknown protocol: {fingerprint}"

    for protocol in ['ash256://', 'not_even_a_colon']:
        assert_raises(protocol, 'value')
        assert_raises(protocol, 'protocol')
        assert_raises(protocol, 'sha')
        assert_raises(protocol, 'artifact_name')
