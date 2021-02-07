import json
from commands import CommandError, DefaultedEnvVar, OptionalEnvVar, RequiredEnvVar


class Command:
    """
    Abstract Base Class for all merkely/change commands.
    """
    def __init__(self, context):
        self._context = context

    def __call__(self):
        raise NotImplementedError("Command subclass override missing")

    @property
    def name(self):
        description = "The Merkely command to execute."
        return self._required_env_var("COMMAND", description)

    @property
    def api_token(self):
        description = "Your API token for Merkely."
        return self._required_env_var("API_TOKEN", description)

    @property
    def display_name(self):
        description = "\n".join([
            'The name of the fingerprinted artifact.',
            'Required when using MERKELY_FINGERPRINT="sha256://..."',
            'Not required when using MERKELY_FINGERPRINT="file://..."',
            'Not required when using MERKELY_FINGERPRINT="docker://..."'
        ])
        return self._optional_env_var("DISPLAY_NAME", description)

    @property
    def fingerprint(self):
        description = "\n".join([
            '1. If prefixed by docker:// the name+tag of the docker image to fingerprint.',
            '   The docker socket must be volume-mounted.',
            '   Example:',
            '     --env MERKELY_FINGERPRINT=”docker://${YOUR_DOCKER_IMAGE_AND_TAG}"',
            '     --volume /var/run/docker.sock:/var/run/docker.sock',
            '',
            '2. If prefixed by file:// the full path of the file to fingerprint.',
            '   The full path must be volume-mounted.',
            '   Example:',
            '     --env MERKELY_FINGERPRINT=”file://${YOUR_FILE_PATH}',
            '     --volume=${YOUR_FILE_PATH}:${YOUR_FILE_PATH}',
            '',
            "3. If prefixed by sha256:// the artifact's sha256 digest."
            '   The name of the artifact must be provided in MERKELY_DISPLAY_NAME',
            '   Example:',
            '     --env MERKELY_FINGERPRINT=”sha256://${YOUR_ARTIFACT_SHA256}”',
            '     --env MERKELY_DISPLAY_NAME=”${YOUR_ARTIFACT_NAME}”'
        ])
        return self._required_env_var("FINGERPRINT", description)

    @property
    def is_compliant(self):
        description = "Whether this artifact is considered compliant from you build process."
        return self._required_env_var('IS_COMPLIANT', description)

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
        return DefaultedEnvVar(self, f"MERKELY_{name}", default, description)

    def _optional_env_var(self, name, description):
        return OptionalEnvVar(self, f"MERKELY_{name}", description)

    def _required_env_var(self, name, description):
        return RequiredEnvVar(self, f"MERKELY_{name}", description)

    def _print_compliance(self):
        env_var = self.is_compliant
        print(f"{env_var.name}: {env_var.value == 'TRUE'}")
