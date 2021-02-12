from commands import CommandError # avoid cyclic dependency
from env_vars import DefaultedEnvVar

NAME = "HOST"
NOTES = "The hostname of Merkely"


def test_is_not_required():
    os_env = {}
    ev = DefaultedEnvVar(os_env, NAME, NOTES)
    assert not ev.is_required
