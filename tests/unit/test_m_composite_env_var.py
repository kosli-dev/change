from env_vars import CompositeEnvVar
from tests.utils import *
from pytest import raises


def test_plain_strings_remain_unchanged():
    target = CompositeEnvVar('abc')
    assert target.string == 'abc'
