import os
from tests.utils import AutoEnvVars, UnexpectedEnvVar, AlreadyExistingEnvVar

from pytest import raises


def test_existing_env_vars_are_restored_when_the_with_statement_exits():
    os.environ["EXISTING_ENV_VAR"] = "Alice"
    os.environ["AND_ANOTHER"] = "Wonderland"

    with AutoEnvVars({}):
        os.environ["EXISTING_ENV_VAR"] = "Different"
        os.environ["AND_ANOTHER"] = "Different"

    assert os.getenv("EXISTING_ENV_VAR") == "Alice"
    assert os.getenv("AND_ANOTHER") == "Wonderland"


def test_arg1_env_vars_that_already_exist_RAISE():
    os.environ["EXISTING_ENV_VAR"] = "Wonderland"

    env = {"EXISTING_ENV_VAR": "Adventures"}
    with raises(AlreadyExistingEnvVar):
        with AutoEnvVars(env):
            pass


def test_arg1_env_vars_are_only_available_inside_the_with_statement():
    assert os.getenv("NEW_ENV_VAR") is None

    new_env = {"NEW_ENV_VAR": "Fishing"}
    with AutoEnvVars(new_env):
        assert os.getenv("NEW_ENV_VAR") == "Fishing"

    assert os.getenv("NEW_ENV_VAR") is None


def test_arg2_must_specify_ALL_new_env_vars_set_inside_the_with_statement():
    assert os.getenv("ENV_SET_INSIDE_WITH") is None

    env = {"ENV_SET_INSIDE_WITH": "Humpty"}
    with AutoEnvVars({}, env):
        os.environ["ENV_SET_INSIDE_WITH"] = "Humpty"
        assert os.getenv("ENV_SET_INSIDE_WITH") == "Humpty"


def test_arg2_with_NO_entry_for_new_env_var_RAISES():
    assert os.getenv("ENV_VAR_NOT_IN_ARG2") is None
    assert os.getenv("IN_ARG2") is None

    with raises(UnexpectedEnvVar) as exc:
        with AutoEnvVars({}, {"IN_ARG2": "wibble"}):
            os.environ["ENV_VAR_NOT_IN_ARG2"] = "XXXX"
            os.environ["IN_ARG2"] = "wibble"

    assert exc.value.expected() == {"IN_ARG2": "wibble"}
    assert exc.value.actual() == {"ENV_VAR_NOT_IN_ARG2": "XXXX", "IN_ARG2": "wibble"}


def test_arg2_with_entry_for_new_env_which_is_NOT_set_RAISES():
    assert os.getenv("ENV_VAR") is None

    with raises(UnexpectedEnvVar) as exc:
        with AutoEnvVars({}, {"ENV_VAR": "bye"}):
            pass

    assert exc.value.expected() == {"ENV_VAR": "bye"}
    assert exc.value.actual() == {}


def test_arg2_with_entry_for_new_env_var_which_is_set_to_a_DIFFERENT_value_RAISES():
    assert os.getenv("ENV_VAR") is None

    with raises(UnexpectedEnvVar) as exc:
        with AutoEnvVars({}, {"ENV_VAR": "bye"}):
            os.environ["ENV_VAR"] = "hello"

    assert exc.value.expected() == {"ENV_VAR": "bye"}
    assert exc.value.actual() == {"ENV_VAR": "hello"}
