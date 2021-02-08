from commands import OptionalEnvVar
from os import path

DESCRIPTION = "\n".join([
    'When using the MERKELY_FINGERPRINT="sha256://${YOUR_ARTIFACT_SHA}"',
    'this env-var is the name of the fingerprinted artifact.',
    '',
    'When using MERKELY_FINGERPRINT="file://${YOUR_FILEPATH}',
    "this env-var is not required; the name used is the 'basename' of ${YOUR_FILEPATH}",
    '',
    'When using MERKELY_FINGERPRINT="docker://${YOUR_IMAGE_AND_TAG}"',
    'this env-var is not required; the name used is ${YOUR_IMAGE_AND_TAG}'
])


class DisplayNameEnvVar(OptionalEnvVar):
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

