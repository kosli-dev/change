import json
from commands import CommandError, RequiredEnvVar


class Command:
    """
    Abstract Base Class for all commands.
    """
    class Error(Exception):
        pass

    def __init__(self, context):
        self._context = context

    def execute(self):
        print("MERKELY_COMMAND={}".format(self.name))
        self._verify_args()  # Template Method Pattern
        self._concrete_execute()  # Template Method Pattern

    @property
    def name(self):
        return RequiredEnvVar("COMMAND", self._context.env).verify().value

    @property
    def merkelypipe(self):
        try:
            merkelypipe_path = "/Merkelypipe.json"
            with open(merkelypipe_path) as file:
                return json.load(file)
        except FileNotFoundError:
            raise CommandError(f"{merkelypipe_path} file not found")
        except IsADirectoryError:
            raise CommandError(f"{merkelypipe_path} is a directory")
        except json.decoder.JSONDecodeError as exc:
            raise CommandError(f"{merkelypipe_path} invalid json - {str(exc)}")

    def _env(self, key):
        return self._context.env.get(key, None)
