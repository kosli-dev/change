from env_vars import DefaultedEnvVar

NAME = "HOST"
NOTES = "The hostname of Merkely"


def test_is_not_required():
    os_env = {}
    ev = Example(os_env, NAME, NOTES)
    assert not ev.is_required


class Example(DefaultedEnvVar):

    def value(self):
        pass
