from commands import load_json
from env_vars import DefaultedEnvVar

NOTES = "\n".join([
    "Defaults to the BITBUCKET_COMMIT env-var if set.",
    "Otherwise",
])


class ArtifactGitCommitEnvVar(DefaultedEnvVar):
    # A 'dynamic' env-var
    # If BITBUCKET_COMMIT is defined, use that
    # If GITHUB_SHA is defined, use that
    # Also need to consider living documentation

    def __init__(self, env):
        super().__init__(env, "ARTIFACT_GIT_COMMIT", NOTES)

    @property
    def value(self):
        if self.is_set and not self.is_empty:
            filename = self.string
            return load_json(filename)
        else:
            return DEFAULT
