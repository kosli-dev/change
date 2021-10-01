from commands import Command
from docs import *
from env_vars import *
from lib.api_schema import ApiSchema


class EchoFingerprint(Command):

    def doc_summary(self):
        return "Echo any fingerprint to stdout"

    def doc_volume_mounts(self):
        return []

    def doc_ref(self):
        return {}

    def __call__(self):
        method = None
        url = None
        payload = None

        def callback(_response):
            stdout = self._external.stdout
            stdout.print(self.fingerprint.sha)
            return None, None, None

        return method, url, payload, callback

    @property
    def pipe_path(self):
        return PipePathEnvVar(self.env)

    @property
    def _merkely_env_var_names(self):
        return [
            'name',
            'fingerprint',
        ]
