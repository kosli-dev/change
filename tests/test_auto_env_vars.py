import os

from tests.utils import AutoEnvVars


def test_new_env_vars_passed_in_init_are_available_only_inside_the_with_statement():
    env = {
        "NICE_HOBBY": "Fishing"
    }
    assert os.getenv("NICE_HOBBY") is None

    with AutoEnvVars(env):
        assert os.getenv("NICE_HOBBY") == "Fishing"

    assert os.getenv("NICE_HOBBY") is None


def test_new_env_vars_set_inside_with_statement_are_unavailable_after_the_with_statement():
    assert os.getenv("GETS_YOU") is None

    with AutoEnvVars():
        os.environ["GETS_YOU"] = "Outside"
        assert os.getenv("GETS_YOU") == "Outside"

    assert os.getenv("GETS_YOU") is None


def test_env_vars_set_before_the_with_statement_are_unaffected():
    os.environ["YOU_SEE"] = "Nature"

    with AutoEnvVars({"YOU_SEE":"Wildlife"}):
        assert os.getenv("YOU_SEE") == "Wildlife"

    assert os.getenv("YOU_SEE") == "Nature"
