import json


class Command:
    class Error(Exception):
        def __init__(self, message):
            super().__init__(message)

    def __init__(self, context):
        self._context = context

    def execute(self):
        print("MERKELY_COMMAND={}".format(self.name))
        self._concrete_execute()  # Template Method Pattern

    @property
    def name(self):
        command = self._env("MERKELY_COMMAND")
        if command is None:
            raise self.Error("MERKELY_COMMAND environment-variable not set")
        if command == "":
            raise self.Error("MERKELY_COMMAND environment-variable is empty string")
        return command

    @property
    def api_token(self):
        return self._env("MERKELY_API_TOKEN")

    @property
    def host(self):
        return self._env("MERKELY_HOST")

    @property
    def merkelypipe(self):
        MERKELYPIPE_PATH = "/Merkelypipe.json"
        with open(MERKELYPIPE_PATH) as file:
            return json.load(file)

    def _env(self, key):
        return self._context.env.get(key, None)
