from commands import OptionalEnvVar, load_json

DESCRIPTION = "\n".join([
    "A filename whose json content to embed in the deployment.",
    "The filename must be volume-mounted in the container."
])


class UserDataEnvVar(OptionalEnvVar):

    def __init__(self, command):
        super().__init__(command.env, "MERKELY_USER_DATA", DESCRIPTION)

    @property
    def json(self):
        filename = self.value
        return load_json(filename)

