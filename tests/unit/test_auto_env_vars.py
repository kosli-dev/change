import os
from tests.utils import AutoEnvVars, UnexpectedEnvVarSetOnExitError, AlreadyExistingEnvVarOnEnterError

from pytest import raises


def test_a_new_env_var_that_already_exists_raises():
    os.environ["EXISTING_ENV_VAR"] = "Wonderland"

    env = {"EXISTING_ENV_VAR": "Adventures"}
    with raises(AlreadyExistingEnvVarOnEnterError) as exc:
        with AutoEnvVars(env):
            pass

    assert exc.value.vars() == {"EXISTING_ENV_VAR":"Wonderland"}


def test_new_env_vars_are_only_available_inside_the_with_statement():
    assert os.getenv("NEW_ENV_VAR") is None

    env = {"NEW_ENV_VAR": "Fishing"}
    with AutoEnvVars(env):
        assert os.getenv("NEW_ENV_VAR") == "Fishing"

    assert os.getenv("NEW_ENV_VAR") is None


def test_env_vars_that_exist_before_the_with_statement_still_exist_after_it():
    os.environ["EXISTING_ENV_VAR"] = "Wonderland"

    with AutoEnvVars({}):
        assert os.getenv("EXISTING_ENV_VAR") == "Wonderland"

    assert os.getenv("EXISTING_ENV_VAR") == "Wonderland"


def test_new_env_vars_set_inside_with_statement_must_be_specified_in_the_second_init_arg_and_are_unavailable_after_the_with_statement():
    assert os.getenv("ENV_SET_INSIDE_WITH") is None

    env = {"ENV_SET_INSIDE_WITH": "Humpty"}
    with AutoEnvVars({}, env):
        os.environ["ENV_SET_INSIDE_WITH"] = "Humpty"
        assert os.getenv("ENV_SET_INSIDE_WITH") == "Humpty"

    assert os.getenv("ENV_SET_INSIDE_WITH") is None


def test_new_env_var_set_inside_with_statement_not_specified_in_arg2_raises_exception():
    assert os.getenv("ENV_VAR_NOT_IN_ARG2") is None
    assert os.getenv("IN_ARG2") is None

    with raises(UnexpectedEnvVarSetOnExitError) as exc:
        with AutoEnvVars({}, {"IN_ARG2": "wibble"}):
            os.environ["ENV_VAR_NOT_IN_ARG2"] = "42"
            os.environ["IN_ARG2"] = "wibble"

    assert exc.value.expected() == {"IN_ARG2": "wibble"}
    assert exc.value.actual() == {"ENV_VAR_NOT_IN_ARG2": "42", "IN_ARG2": "wibble"}

    assert os.getenv("ENV_VAR_NOT_IN_ARG2") is None
    assert os.getenv("IN_ARG2") is None


