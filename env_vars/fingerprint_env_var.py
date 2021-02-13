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
        f = self.__fingerprinter
        return f.protocol

    @property
    def artifact_name(self):
        f = self.__fingerprinter
        p = f.protocol
        after = self.string[len(p):]
        return f.artifact_name(after)

    @property
    def artifact_basename(self):
        f = self.__fingerprinter
        p = f.protocol
        after = self.string[len(p):]
        return f.artifact_basename(after)

    @property
    def sha(self):
        f = self.__fingerprinter
        p = f.protocol
        after = self.string[len(p):]
        return f.sha(p, after)

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
