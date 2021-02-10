from commands import load_json
from env_vars import OptionalEnvVar

DESCRIPTION = "\n".join([
    "A filename whose json content to embed in the deployment.",
    "The filename must be volume-mounted in the container."
])


class UserDataFileEnvVar(OptionalEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_USER_DATA_FILE", DESCRIPTION)

    @property
    def json(self):
        filename = self.value
        return load_json(filename)

