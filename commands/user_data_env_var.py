from commands import OptionalEnvVar
import json

DESCRIPTION = "\n".join([
    "TODO"
])


class UserDataEnvVar(OptionalEnvVar):

    def __init__(self, command):
        super().__init__(command.env, "MERKELY_USER_DATA", DESCRIPTION)

    @property
    def json(self):
        filename = self.value
        with open(filename) as file:
            return json.load(file)

