from env_vars import DefaultedEnvVar

DEFAULT = {}


class UserDataEnvVar(DefaultedEnvVar):

    def __init__(self, external):
        super().__init__(external.env, "MERKELY_USER_DATA", '')
        self._external = external

    @property
    def value(self):
        if self.string != "":
            filename = self.string
            return self._external.load_json(filename)
        else:
            return DEFAULT

    def doc_example(self, _ci_name, _command_name):
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return " ".join([
            "A pathed filename containing json content to embed in the data logged to Merkely.",
            "If provided, must be volume-mounted in the container.",
            f"If not provided, the json content defaults to {DEFAULT}",
        ])
