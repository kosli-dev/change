import os
from tests.utils import AutoEnvVars, UnexpectedEnvVarsError

from pytest import raises


def test_env_vars_set_before_the_with_statement_are_unaffected():
    os.environ["YOU_SEE"] = "Nature"
    env = {
        "YOU_SEE": "Wildlife"
    }
    with AutoEnvVars(env):
        assert os.getenv("YOU_SEE") == "Wildlife"

    assert os.getenv("YOU_SEE") == "Nature"


def test_new_env_vars_set_inside_with_statement_must_be_specified_in_the_second_init_arg_and_are_unavailable_after_the_with_statement():
    assert os.getenv("GETS_YOU") is None
    env = {
        "GETS_YOU": "Outside"
    }
    with AutoEnvVars({}, env):
        os.environ["GETS_YOU"] = "Outside"
        assert os.getenv("GETS_YOU") == "Outside"

    assert os.getenv("GETS_YOU") is None


def test_new_env_var_set_inside_with_statement_not_specified_in_second_init_arg_raises_exception():
    assert os.getenv("ALPHA") is None

    with raises(UnexpectedEnvVarsError) as exc:
        with AutoEnvVars({}, {}):
            os.environ["ALPHA"] = "42"

    assert os.getenv("ALPHA") is None


def test_new_env_vars_passed_in_init_are_available_only_inside_the_with_statement():
    assert os.getenv("NICE_HOBBY") is None
    env = {
        "NICE_HOBBY": "Fishing"
    }

    with AutoEnvVars(env):
        assert os.getenv("NICE_HOBBY") == "Fishing"

    assert os.getenv("NICE_HOBBY") is None
