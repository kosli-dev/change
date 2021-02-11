from commands import Command
from env_vars import *
from cdb.api_schema import ApiSchema
from cdb.http import http_post_payload


class LogApprovalCommand(Command):

    def __call__(self):
        payload = {
            "base_artifact": self.fingerprint.sha,
            "description": "No description provided",
            "src_commit_list": [
                "8f5b384644eb83e7f2a6d9499539a077e7256b8b",
                "e0ad84e1a2464a9486e777c1ecde162edff930a9"
            ],
            "target_artifact": self.fingerprint.sha
        }
        url = ApiSchema.url_for_releases(self.host.value, self.merkelypipe)
        http_post_payload(url, payload, self.api_token.value)
        return 'Posting', url, payload

    @property
    def release_description(self):
        notes = "todo"
        # defaults to "No description provided""
        return self._defaulted_env_var("RELEASE_DESCRIPTION", notes)

    @property
    def target_src_commitish(self):
        notes = "todo"
        # defaults to None
        return self._defaulted_env_var("TARGET_SRC_COMMITISH", notes)

    @property
    def base_src_commitish(self):
        notes = "todo"
        # defaults to None
        return self._defaulted_env_var("BASE_SRC_COMMITISH", notes)

    @property
    def src_repo_root(self):
        notes = "todo"
        # defaults to DEFAULT_REPO_ROOT
        return self._defaulted_env_var("SRC_REPO_ROOT", notes)

    @property
    def _env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'target_src_commitish',
            'base_src_commitish',
            'release_description',
            'src_repo_root',
            'api_token',
            'host',
        ]
