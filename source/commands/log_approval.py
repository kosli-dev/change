from errors import ChangeError
from commands import Command
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
        notes = f"A description for the approval."
        return self._required_env_var("MERKELY_DESCRIPTION", notes)

    @property
    def newest_src_commitish(self):
        notes = "The source commit-ish for the newest change in the approval."
        return self._required_env_var("MERKELY_NEWEST_SRC_COMMITISH", notes)

    @property
    def oldest_src_commitish(self):
        notes = "The source commit-ish for the oldest change in the approval."
        return self._required_env_var("MERKELY_OLDEST_SRC_COMMITISH", notes)

    @property
    def src_repo_root(self):
        default = "/src"
        notes = " ".join([
            "The directory where the source git repository is volume-mounted.",
            f"Defaults to `{default}`",
            ''
         ])
        return self._static_defaulted_env_var("MERKELY_SRC_REPO_ROOT", default, notes)

    @property
    def is_approved(self):
        default = 'TRUE'
        notes = f"Defaults to {default}"
        return self._static_defaulted_env_var("MERKELY_IS_APPROVED", default, notes)

    @property
    def _merkely_env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'newest_src_commitish',
            'oldest_src_commitish',
            'description',
            'is_approved',
            'src_repo_root',
            'user_data',
            'api_token',
            'host',
        ]


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
