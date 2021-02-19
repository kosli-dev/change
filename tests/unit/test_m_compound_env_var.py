from env_vars import CompoundEnvVar
from tests.utils import *
from pytest import raises


def test_plain_strings_remain_unchanged():
    target = CompoundEnvVar('abc')
    assert target.string == 'abc'
