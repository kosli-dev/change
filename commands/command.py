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
        description = "The Merkely command to execute"
        return self._required_env_var("COMMAND", description).verify().value

    @property
    def args(self):
        return sorted(self.args_list, key=lambda arg: arg.name)

    def verify_args(self):
        for arg in self.args:
            arg.verify()

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
        description = "Your API token for Merkely"
        return self._required_env_var("API_TOKEN", description)

    @property
    def host(self):
        description = "The host name for Merkely"
        host = "https://app.compliancedb.com"
        return self._defaulted_env_var("HOST", host, description)

    def _defaulted_env_var(self, name, default, description=None):
        return DefaultedEnvVar(f"MERKELY_{name}", self._context.env, default, description)

    def _optional_env_var(self, name, description=None):
        return OptionalEnvVar(f"MERKELY_{name}", self._context.env, description)

    def _required_env_var(self, name, description=None):
        return RequiredEnvVar(f"MERKELY_{name}", self._context.env, description)

