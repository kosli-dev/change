from errors import ChangeError
from pygit2 import Repository, _pygit2
from pygit2._pygit2 import GIT_SORT_TIME


def repo_at(root):
    try:
        # Ensure dir/ does not have duplicted / in error messages
        if root.endswith('/'):
            dir = root + '.git'
        else:
            dir = root + '/.git'
        return Repository(dir)
    except _pygit2.GitError as err:
        raise ChangeError(f"Error: {str(err)}")


def commit_for_commitish(repo, commitish):
    """returns the commit for a given reference as a string"""
    commit = repo.revparse_single(commitish)
    return str(commit.id)


def list_commits_between(repo, target_commit, base_commit):
    start = repo.revparse_single(target_commit)
    stop = repo.revparse_single(base_commit)

    commits = []

    walker = repo.walk(start.id, GIT_SORT_TIME)
    walker.hide(stop.id)
    for commit in walker:
        commits.append(str(commit.id))

    return commits
