from commands import CommandError
from env_vars import RequiredEnvVar
from env_vars import fingerprint_env_var_cls_for

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
        unknown_protocol_error = CommandError(f"Unknown protocol: {self.string}")
        regex = re.compile(r'(?P<protocol>[0-9a-z]+:\/\/).*')
        match = regex.match(self.string)
        if match is None:
            raise unknown_protocol_error
        protocol = match.group('protocol')
        if fingerprint_env_var_cls_for(protocol) is None:
            raise unknown_protocol_error
        return protocol

    @property
    def artifact_name(self):
        return self.__fingerprint.artifact_name

    @property
    def artifact_basename(self):
        return self.__fingerprint.artifact_basename

    @property
    def sha(self):
        return self.__fingerprint.sha

    @property
    def __fingerprint(self):
        after_protocol = self.string[len(self.protocol):]
        if after_protocol == "":
            raise CommandError(f"Empty {self.protocol} fingerprint")
        cls = fingerprint_env_var_cls_for(self.protocol)
        return cls(self.__command, self.protocol, after_protocol)
