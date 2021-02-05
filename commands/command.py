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
        return self._required_env_var("COMMAND", description)

    @property
    def args(self):
        return sorted(self.args_list, key=lambda arg: arg.name)

    def verify_args(self):
        for arg in self.args:
            arg.verify()

    @property
    def merkelypipe(self):
        try:
            filename = "/Merkelypipe.json"
            with open(filename) as file:
                return json.load(file)
        except FileNotFoundError:
            raise CommandError(f"{filename} file not found")
        except IsADirectoryError:
            raise CommandError(f"{filename} is a directory")
        except json.decoder.JSONDecodeError as exc:
            raise CommandError(f"{filename} invalid json - {str(exc)}")

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
        return DefaultedEnvVar(f"MERKELY_{name}", self._env, default, description)

    def _optional_env_var(self, name, description=None):
        return OptionalEnvVar(f"MERKELY_{name}", self._env, description)

    def _required_env_var(self, name, description=None):
        return RequiredEnvVar(f"MERKELY_{name}", self._env, description)

    @property
    def _env(self):
        return self._context.env