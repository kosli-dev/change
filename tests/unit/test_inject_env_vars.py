from tests.utils import inject_env_vars, AlreadySetEnvVars

import os
from pytest import raises


def test_injected_env_vars_are_set_inside_decorated_callable():
    @inject_env_vars({"ALPHA": "42"})
    def set_with_inject():
        return os.environ["ALPHA"] == "42"

    def set_without_inject():
        return "ALPHA" in os.environ.keys()

    assert set_with_inject()
    assert not set_without_inject()


def test_injected_env_vars_are_not_set_before_or_after_decorated_callable():
    @inject_env_vars({"BETA": "FortyTwo"})
    def set_with_inject():
        return os.environ["BETA"] == "FortyTwo"
    assert "BETA" not in os.environ.keys()
    assert set_with_inject()
    assert "BETA" not in os.environ.keys()


def test_injected_env_vars_are_unset_when_decorated_callable_raises():
    class MyError(EnvironmentError):
        pass
    @inject_env_vars({"GAMMA": "Six"})
    def set_with_inject():
        raise MyError()
    with raises(MyError):
        set_with_inject()
    assert not "GAMMA" in os.environ.keys()


def test_inject_env_vars_raises_when_name_is_already_an_env_var():
    @inject_env_vars({"PYTHONPATH": "abc"})
    def set_with_inject():
        pass
    assert "PYTHONPATH" in os.environ.keys()
    paths = os.environ["PYTHONPATH"]
    with raises(AlreadySetEnvVars) as exc:
        set_with_inject()
    assert exc.value.already_existing() == {"PYTHONPATH": paths}
