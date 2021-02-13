from env_vars import RequiredEnvVar

import re

NOTES = "\n".join([
    "...",
])

EXAMPLE = "docker://${YOUR_IMAGE_AND_TAG}"


class FingerprintEnvVar(RequiredEnvVar):

    def __init__(self, command):
        super().__init__(command.env, "FINGERPRINT", NOTES, EXAMPLE)
        self.__command = command

    @property
    def value(self):
        super().value
        self.protocol
        self.artifact_name
        return self.string

    @property
    def protocol(self):
        return self.__fingerprinter.protocol

    @property
    def artifact_name(self):
        return self.__fingerprinter.artifact_name(self.string)

    @property
    def artifact_basename(self):
        return self.__fingerprinter.artifact_basename(self.string)

    @property
    def sha(self):
        return self.__fingerprinter.sha(self.string)

    @property
    def __fingerprinter(self):
        return self.__command.fingerprinter_for(self.string)
