from commands import CommandError
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
        return self.__fingerprinter.artifact_name(self.after_protocol)

    @property
    def artifact_basename(self):
        return self.__fingerprinter.artifact_basename(self.after_protocol)

    @property
    def sha(self):
        return self.__fingerprinter.sha(self.protocol, self.after_protocol)

    @property
    def __fingerprinter(self):
        d = self.__command.docker_fingerprinter
        f = self.__command.file_fingerprinter
        s = self.__command.sha256_fingerprinter
        if d.handles_protocol(self.string):
            return d
        elif f.handles_protocol(self.string):
            return f
        elif s.handles_protocol(self.string):
            return s
        else:
            raise CommandError(f"Unknown protocol: {self.string}")

    @property
    def after_protocol(self):
        return self.string[len(self.__fingerprinter.protocol):]
