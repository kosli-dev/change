from commands import DefaultedEnvVar
from tests.utils import *


def test_value_from_default():
    name = "MERKELY_HOST"
    default = "https://default.merkely.com"
    dev = DefaultedEnvVar(name, {}, default)
    assert dev.value == default


def test_value_from_env():
    name = "MERKELY_HOST"
    value = "https://test.merkely.com"
    default = "https://other.merkely.com"
    with ScopedEnvVars({name: value}) as env:
        assert DefaultedEnvVar(name, env, default).value == value
