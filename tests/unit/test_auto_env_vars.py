import os

from tests.unit.utils import AutoEnvVars


def test_env_vars_set_before_the_with_statement_are_unaffected():
    os.environ["YOU_SEE"] = "Nature"

    with AutoEnvVars({"YOU_SEE":"Wildlife"}):
        assert os.getenv("YOU_SEE") == "Wildlife"

    assert os.getenv("YOU_SEE") == "Nature"


def test_new_env_vars_set_inside_with_statement_are_unavailable_after_the_with_statement():
    assert os.getenv("GETS_YOU") is None

    with AutoEnvVars():
        os.environ["GETS_YOU"] = "Outside"
        assert os.getenv("GETS_YOU") == "Outside"

    assert os.getenv("GETS_YOU") is None


def test_new_env_vars_passed_in_init_are_available_only_inside_the_with_statement():
    assert os.getenv("NICE_HOBBY") is None
    env = {
        "NICE_HOBBY": "Fishing"
    }

    with AutoEnvVars(env):
        assert os.getenv("NICE_HOBBY") == "Fishing"

    assert os.getenv("NICE_HOBBY") is None


def test_new_env_vars_set_inside_with_statement_can_be_interrogated_after_the_with_statement_in_context_object():
    assert os.getenv("ALPHA") is None
    assert os.getenv("BETA") is None

    with AutoEnvVars() as context_manager:
        os.environ["ALPHA"] = "123"
        os.environ["BETA"] = "456"
        assert os.getenv("ALPHA") == "123"
        assert os.getenv("BETA") == "456"

    assert os.getenv("ALPHA") is None
    assert os.getenv("BETA") is None
    new_env_vars = context_manager.new_env_vars()
    assert sorted(list(new_env_vars.keys())) == ["ALPHA", "BETA"]
    assert new_env_vars["ALPHA"] == "123"
    assert new_env_vars["BETA"] == "456"
    assert context_manager.is_creating_env_var("ALPHA")
    assert context_manager.is_creating_env_var("BETA")
    assert not context_manager.is_creating_env_var("GAMMA")
