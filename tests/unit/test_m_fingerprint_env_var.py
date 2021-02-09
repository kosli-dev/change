from commands import Command, CommandError, Context
from env_vars import FingerprintEnvVar
from tests.utils import *
from pytest import raises

SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_unknown_protocol__all_properties_raise():
    def assert_bad_property_raises(protocol, property_name):
        fingerprint = f"{protocol}{SHA256}"
        env = {"MERKELY_FINGERPRINT": fingerprint}
        context = Context(env, None, None)
        command = Command(context)
        ev = FingerprintEnvVar(command)
        with raises(CommandError) as exc:
            getattr(ev, property_name)
        assert str(exc.value) == f"Unknown protocol: {fingerprint}"

    for bad_protocol in ['ash256://', 'not_even_a_colon']:
        assert_bad_property_raises(bad_protocol, 'value')
        assert_bad_property_raises(bad_protocol, 'protocol')
        assert_bad_property_raises(bad_protocol, 'sha')
        assert_bad_property_raises(bad_protocol, 'artifact_name')
