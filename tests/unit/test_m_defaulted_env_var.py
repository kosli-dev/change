from env_vars import DefaultedEnvVar

NAME = "MERKELY_HOST"
DEFAULT = "https://default.merkely.com"
DESCRIPTION = "The hostname of Merkely"


def test_value_from_default():
    _env, smart_env_var = make_test_variables()

    assert smart_env_var.name == NAME
    assert smart_env_var.value == DEFAULT
    assert smart_env_var.description == DESCRIPTION


def test_value_from_env():
    env, smart_env_vars = make_test_variables()

    not_default = "https://test.merkely.com"
    env.update({NAME: not_default})

    assert smart_env_vars.name == NAME
    assert smart_env_vars.value == not_default
    assert smart_env_vars.description == DESCRIPTION


def make_test_variables():
    env = {}
    name = "MERKELY_HOST"
    default = "https://default.merkely.com"
    description = "The hostname of Merkely"
    return env, DefaultedEnvVar(env, name, default, description)
