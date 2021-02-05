from commands import DefaultedEnvVar
from tests.utils import *


def test_value_from_default():
    name = "MERKELY_HOST"
    default = "https://default.merkely.com"
    description = "The hostname of Merkely"

    dev = DefaultedEnvVar(name, {}, default, description)

    assert dev.name == name
    assert dev.value == default
    assert dev.description == description


def test_value_from_env():
    name = "MERKELY_HOST"
    value = "https://test.merkely.com"
    default = None  # "https://other.merkely.com"
    description = "The hostname of Merkely"

    with ScopedEnvVars({name: value}) as env:
        dev = DefaultedEnvVar(name, env, default, description)

        assert dev.value == value
        assert dev.name == name
        assert dev.description == description
