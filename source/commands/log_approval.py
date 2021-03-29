from commands import Command
from env_vars import *
from cdb.api_schema import ApiSchema
from cdb.git import repo_at, list_commits_between


class LogApproval(Command):

    def summary(self, _ci):
        return "Logs an approval made outside of Merkely in Merkely"

    def volume_mounts(self, ci):
        mounts = ["${PWD}:/src"]
        if ci != 'bitbucket':
            mounts.append("/var/run/docker.sock:/var/run/docker.sock")
        return mounts

    def __call__(self):
        commit_list = list_commits_between(repo_at(self.src_repo_root.value),
                                           self.newest_src_commitish.value,
                                           self.oldest_src_commitish.value)
        payload = {
            "artifact_sha256": self.fingerprint.sha,
            "description": self.description.value,
            "src_commit_list": commit_list,
            "user_data": self.user_data.value,
            "approvals": [
                {
                    "state": self.approval_state(),
                    "comment": self.description.value,
                    "approved_by": "External",
                    "approval_url": "undefined"
                }
            ]
        }
        url = ApiSchema.url_for_approvals(self.host.value, self.merkelypipe)
        return 'Posting', url, payload, self.api_token.value, None

    def approval_state(self):
        if self.is_approved.value == 'TRUE':
            return "APPROVED"
        else:
            return "UNAPPROVED"

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
    def is_approved(self):
        return IsApprovedEnvVar(self.env)

    @property
    def _merkely_env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'oldest_src_commitish',
            'newest_src_commitish',
            'description',
            'is_approved',
            'src_repo_root',
            'user_data',
            'owner',
            'pipeline',
            'api_token',
            'host',
        ]


class IsApprovedEnvVar(StaticDefaultedEnvVar):

    def __init__(self, env):
        default = 'TRUE'
        super().__init__(env, "MERKELY_IS_APPROVED", default)

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, '"TRUE"'
        if ci_name == 'bitbucket':
            return True, '"TRUE"'
        return False, ""

    def doc_note(self, ci_name, _command_name):
        return f'Defaults to "TRUE"'



class DescriptionEnvVar(RequiredEnvVar):

    def __init__(self, env):
        super().__init__(env, "MERKELY_DESCRIPTION")

    def doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, '"Approval created by ${{ github.actor }} on github"'
        if ci_name == 'bitbucket':
            return True, '"Production release requested"'
        return False, ""

    def doc_note(self, _ci_name, _command_name):
        return f"A description for the approval."
