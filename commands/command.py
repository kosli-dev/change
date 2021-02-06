import json
from commands import CommandError, DefaultedEnvVar, OptionalEnvVar, RequiredEnvVar


class Command:
    """
    Abstract Base Class for all commands.
    """
    def __init__(self, context):
        self._context = context

    def __call__(self):
        raise NotImplementedError("Command is abstract")

    @property
    def name(self):
        description = "The Merkely command to execute."
        return self._required_env_var("COMMAND", description)

    @property
    def api_token(self):
        description = "Your API token for Merkely."
        return self._required_env_var("API_TOKEN", description)

    @property
    def merkelypipe(self):
        try:
            filename = "/Merkelypipe.json"
            with open(filename) as file:
                return json.load(file)
        except FileNotFoundError:
            raise CommandError(f"{filename} file not found.")
        except IsADirectoryError:
            raise CommandError(f"{filename} is a directory.")
        except json.decoder.JSONDecodeError as exc:
            raise CommandError(f"{filename} invalid json - {str(exc)}")

    @property
    def host(self):
        default = "https://app.compliancedb.com"
        description = f"The host name for Merkely. The default is {default}"
        return self._defaulted_env_var("HOST", default, description)

    def _defaulted_env_var(self, name, default, description):
        return DefaultedEnvVar(f"MERKELY_{name}", self._env, default, description)

    def _optional_env_var(self, name, description):
        return OptionalEnvVar(f"MERKELY_{name}", self._env, description)

    def _required_env_var(self, name, description):
        return RequiredEnvVar(f"MERKELY_{name}", self._env, description)

    @property
    def _env(self):
        return self._context.env

    def _print_compliance(self):
        env_var = self.is_compliant
        print(f"{env_var.name}: {env_var.value == 'TRUE'}")
