from errors import ChangeError
from env_vars import CompoundEnvVar
from pytest import raises

NAME = "MERKELY_ARTIFACT_GIT_URL"


def test_original_env_var_is_used_in_error_messages():
    target = CompoundEnvVar(NAME, 'abc')
    assert target.name == NAME


def test_plain_strings_remain_unchanged():
    target = CompoundEnvVar(NAME, 'abc')
    assert target.string == 'abc'


def test_plain_string_are_concatenated():
    target = CompoundEnvVar(NAME, 'abc', '/', 'wibble.json')
    assert target.string == 'abc/wibble.json'


def test_plain_string_is_not_expanded():
    target = CompoundEnvVar(NAME, 'NOT_AN_ENV_VAR')
    ev = {'NOT_AN_ENV_VAR': 'hello world'}
    assert target.value(ev) == 'NOT_AN_ENV_VAR'


def test_env_var_string_is_expanded():
    target = CompoundEnvVar(NAME, '${SOME_ENV_VAR}')
    ev = {'SOME_ENV_VAR': 'hello world'}
    assert target.value(ev) == 'hello world'


def test_expansion_of_env_var_not_set_raises():
    not_set = 'SOME_ENV_VAR'
    part = '${' + not_set + '}'
    target = CompoundEnvVar(NAME, '/path/', part)
    ev = {}
    with raises(ChangeError) as exc:
        target.value(ev)

    assert str(exc.value) == f"Error: environment-variable {NAME} defaults to `{target.string}` but `{not_set}` is not set."