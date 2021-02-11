from commands import Command
from env_vars import *
from cdb.api_schema import ApiSchema
from cdb.http import http_post_payload
from cdb.git import list_commits_between, repo_at


class LogApprovalCommand(Command):

    def __call__(self):
        commit_list = list_commits_between(repo_at(self.src_repo_root.value),
                                           self.target_src_commitish.value,
                                           self.base_src_commitish.value)
        payload = {
            "base_artifact": self.fingerprint.sha,
            "description": self.release_description.value,
            "target_artifact": self.fingerprint.sha,
            "src_commit_list": commit_list,
        }
        url = ApiSchema.url_for_releases(self.host.value, self.merkelypipe)
        http_post_payload(url, payload, self.api_token.value)
        return 'Posting', url, payload

    @property
    def release_description(self):
        notes = "todo"
        default = "No description provided"
        return self._static_defaulted_env_var("RELEASE_DESCRIPTION", default, notes)

    @property
    def target_src_commitish(self):
        notes = "todo"
        default = None
        return self._static_defaulted_env_var("TARGET_SRC_COMMITISH", default, notes)

    @property
    def base_src_commitish(self):
        notes = "todo"
        default = None
        return self._static_defaulted_env_var("BASE_SRC_COMMITISH", default, notes)

    @property
    def src_repo_root(self):
        notes = "todo"
        default = "/src/"
        return self._static_defaulted_env_var("SRC_REPO_ROOT", default, notes)

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
