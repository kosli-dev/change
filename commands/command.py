import json


class Command:

    def __init__(self, context):
        self._context = context

    def execute(self):
        print("MERKELY_COMMAND={}".format(self.command))
        self.concrete_execute()

    @property
    def command(self):
        return self._env("MERKELY_COMMAND")

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

    def _env(self, name):
        return self._context['env'].get(name, None)
