from commands import RequiredEnvVar
from os import path

DESCRIPTION = "\n".join([
    'The name of the fingerprinted artifact.',
    'Required when using MERKELY_FINGERPRINT="sha256://..."',
    'Not required when using MERKELY_FINGERPRINT="file://..."',
    'Not required when using MERKELY_FINGERPRINT="docker://..."'
])


class DisplayNameEnvVar(RequiredEnvVar):
    def __init__(self, command):
        super().__init__(command.env, "MERKELY_DISPLAY_NAME", DESCRIPTION)
        self._command = command

    @property
    def value(self):
        fingerprint = self._command.env_vars.fingerprint
        if fingerprint.protocol == 'sha256://':
            return super().value
        elif fingerprint.protocol == 'file://':
            return path.basename(fingerprint.artifact_name)
        else:
            return fingerprint.artifact_name

