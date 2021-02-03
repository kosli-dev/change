import json
from commands import CommandError, DefaultedEnvVar, OptionalEnvVar, RequiredEnvVar


class Command:
    """
    Abstract Base Class for all commands.
    """
    def __init__(self, context):
        self._context = context

    @property
    def name(self):
        return self._required_env_var("COMMAND").verify().value

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

    @property
    def api_token(self):
        return self._required_env_var("API_TOKEN")

    @property
    def host(self):
        return self._defaulted_env_var("HOST", "https://app.compliancedb.com")

    def _defaulted_env_var(self, name, default):
        return DefaultedEnvVar(f"MERKELY_{name}", self._context.env, default)

    def _optional_env_var(self, name):
        return OptionalEnvVar(f"MERKELY_{name}", self._context.env)

    def _required_env_var(self, name):
        return RequiredEnvVar(f"MERKELY_{name}", self._context.env)

