from env_vars import HostEnvVar

NAME = "MERKELY_HOST"
DEFAULT = "https://app.compliancedb.com"


def test_value_when_set_from_env_var():
    not_default = "http://accu.org"
    ev = make_env_var({NAME: not_default})
    assert ev.value == not_default


def test_value_defaults_when_not_set_from_env_var():
    ev = make_env_var({})
    assert ev.value == DEFAULT


def test_value_defaults_when_set_to_empty_string():
    empty = ""
    ev = make_env_var({NAME: empty})
    assert ev.value == DEFAULT


def make_env_var(ev):
    return HostEnvVar(ev)
