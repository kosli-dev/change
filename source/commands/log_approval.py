from errors import ChangeError
from commands import Command
from env_vars import *
from cdb.api_schema import ApiSchema
from cdb.http import http_post_payload
from pygit2 import Repository, _pygit2
from pygit2._pygit2 import GIT_SORT_TIME


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
            "is_approved": self.is_approved.value == 'TRUE',
            "src_commit_list": commit_list,
            "user_data": self.user_data.value
        }
        url = ApiSchema.url_for_approvals(self.host.value, self.merkelypipe)
        http_post_payload(url, payload, self.api_token.value)
        return 'Posting', url, payload

    @property
    def description(self):
        return DescriptionEnvVar(self.env)

    @property
    def newest_src_commitish(self):
        return NewestSrcCommitishEnvVar(self.env)

    @property
    def oldest_src_commitish(self):
        return OldestSrcCommitishEnvVar(self.env)

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
        notes = f"Defaults to {default}"
        super().__init__(env, "MERKELY_IS_APPROVED", default, notes)

    def ci_doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, '"TRUE"'
        return False, ""


class SrcRepoRootEnvVar(StaticDefaultedEnvVar):

    def __init__(self, env):
        default = "/src"
        notes = " ".join([
            "The directory where the source git repository is volume-mounted.",
            f"Defaults to `{default}`",
        ])
        super().__init__(env, "MERKELY_SRC_REPO_ROOT", default, notes)

    def ci_doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, "${{ github.workspace }}"
        return False, ""


class DescriptionEnvVar(RequiredEnvVar):

    def __init__(self, env):
        notes = f"A description for the approval."
        super().__init__(env, "MERKELY_DESCRIPTION", notes)

    def ci_doc_example(self, ci_name, _command_name):
        if ci_name == 'github':
            return True, '"Approval created by ${{ github.actor }} on github"'
        return False, ""



def repo_at(root):
    try:
        repo = Repository(root + '/.git')
    except _pygit2.GitError as err:
        raise ChangeError(f"Error: {str(err)}")
    return repo


def list_commits_between(repo, target_commit, base_commit):
    start = repo.revparse_single(target_commit)
    stop = repo.revparse_single(base_commit)

    commits = []

    walker = repo.walk(start.id, GIT_SORT_TIME)
    walker.hide(stop.id)
    for commit in walker:
        commits.append(str(commit.id))

    return commits
