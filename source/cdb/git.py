from pygit2 import Repository, _pygit2
from pygit2._pygit2 import GIT_SORT_TIME


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


def repo_at(root):
    try:
        repo = Repository(root + '.git')
    except _pygit2.GitError as err:
        print("Error: " + str(err))
        return None
    return repo