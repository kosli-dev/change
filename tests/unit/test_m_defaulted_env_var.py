from env_vars import DefaultedEnvVar

NAME = "HOST"
NOTES = "The hostname of Merkely"


def test_is_required_is_false_for_raw_docker():
    os_env = {}
    ev = Example(os_env, NAME, NOTES)
    assert not ev.is_required('docker')


class Example(DefaultedEnvVar):

    def value(self):
        pass
