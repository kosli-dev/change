from commands import Command
from env_vars import *
from cdb.api_schema import ApiSchema
from cdb.git import repo_at, list_commits_between


class RequestApproval(Command):

    def doc_summary(self, _ci_name):
        return "Request an approval in Merkely."

    def doc_volume_mounts(self, ci_name):
        if ci_name == 'docker':
            return [
                "${PWD}:/src",
                "/var/run/docker.sock:/var/run/docker.sock"
            ]
        else:
            return []

    def __call__(self):
        commit_list = list_commits_between(repo_at(self.src_repo_root.value),
                                           self.newest_src_commitish.value,
                                           self.oldest_src_commitish.value)
        payload = {
            "artifact_sha256": self.fingerprint.sha,
            "description": self.description.value,
            "src_commit_list": commit_list,
            "user_data": self.user_data.value,
            "approvals": []
        }
        url = ApiSchema.url_for_approvals(self.host.value, self.merkelypipe)
        return 'POST', url, payload, None

    @property
    def description(self):
        return DescriptionEnvVar(self.env)

    @property
    def oldest_src_commitish(self):
        return OldestSrcCommitishEnvVar(self.env)

    @property
    def newest_src_commitish(self):
        return NewestSrcCommitishEnvVar(self.env)

    @property
    def src_repo_root(self):
        return SrcRepoRootEnvVar(self.env)

    @property
    def _merkely_env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'oldest_src_commitish',
            'newest_src_commitish',
            'description',
            'src_repo_root',
            'user_data',
            'owner',
            'pipeline',
            'api_token',
            'host',
        ]


class DescriptionEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_DESCRIPTION")

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, '"Approval requested by ${{ github.actor }} on github"'
        if ci_name == 'bitbucket':
            return True, '"Approval requested on bitbucket"'
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return f"A description for the approval request."
