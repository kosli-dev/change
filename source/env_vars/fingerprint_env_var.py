from env_vars import RequiredEnvVar

NOTES = "\n".join([
    "...",
])

EXAMPLE = "docker://${YOUR_IMAGE_AND_TAG}"


class FingerprintEnvVar(RequiredEnvVar):

    def __init__(self, context):
        super().__init__(context.env, "MERKELY_FINGERPRINT", NOTES, EXAMPLE)
        self.__context = context

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
        return self.__context.fingerprinter_for(self.string)
