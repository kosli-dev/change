from commands import CommandError
from env_vars import RequiredEnvVar
from env_vars import fingerprint_env_var_cls_for

import re

DESCRIPTION = "\n".join([
    "...",
    "..."
])


class FingerprintEnvVar(RequiredEnvVar):

    def __init__(self, command):
        super().__init__(command.env, "MERKELY_FINGERPRINT", DESCRIPTION)
        self._command = command

    @property
    def value(self):
        self.protocol
        self.artifact_name
        return self._raw_value

    @property
    def protocol(self):
        unknown_protocol_error = CommandError(f"Unknown protocol: {self._raw_value}")
        regex = re.compile(r'(?P<protocol>[0-9a-z]+:\/\/).*')
        match = regex.match(self._raw_value)
        if match is None:
            raise unknown_protocol_error
        protocol = match.group('protocol')
        if fingerprint_env_var_cls_for(protocol) is None:
            raise unknown_protocol_error
        return protocol

    @property
    def artifact_name(self):
        return self._fingerprint.artifact_name

    @property
    def sha(self):
        return self._fingerprint.sha

    @property
    def _fingerprint(self):
        cls = fingerprint_env_var_cls_for(self.protocol)
        after_protocol = self._raw_value[len(self.protocol):]
        if after_protocol == "":
            raise CommandError(f"Empty {self.protocol} fingerprint")
        return cls(self._command, self.protocol, after_protocol)

    @property
    def _raw_value(self):
        return super().value
