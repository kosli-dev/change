from env_vars import RequiredEnvVar


class FingerprintEnvVar(RequiredEnvVar):

    def __init__(self, external):
        super().__init__(external.env, "MERKELY_FINGERPRINT", '')
        self.__external = external

    def notes(self, _ci):
        # See docs.merkely.com/source/_ext/describe_command.py
        return "<FINGERPRINT_LINK>"

    @property
    def value(self):
        super().value
        self.artifact_name
        return self.string

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
        return self.__external.fingerprinter_for(self.string)
