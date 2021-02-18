from cdb.bitbucket import adapt_create_release_variables
from tests.utils import *
import os


def test_only_required_env_vars():
    env = {
        "BITBUCKET_CLONE_DIR": "tests/some/dir",
        "CDB_ARTIFACT_SHA": "aacdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212",
        "BITBUCKET_WORKSPACE": "test_project",
        "BITBUCKET_REPO_SLUG": "test_repo",
        "BITBUCKET_COMMIT": "12037940e4e7503055d8a8eea87e177f04f14616",
        "BITBUCKET_BUILD_NUMBER": "1234"
    }
    set_env_vars = {
        "CDB_ARTIFACT_GIT_URL": f"https://bitbucket.org/test_project/test_repo/commits"
                                f"/{env['BITBUCKET_COMMIT']}",
        "CDB_ARTIFACT_GIT_COMMIT": env['BITBUCKET_COMMIT'],
        "CDB_BUILD_NUMBER": env['BITBUCKET_BUILD_NUMBER'],
        "CDB_CI_BUILD_URL": f"https://bitbucket.org/{env['BITBUCKET_WORKSPACE']}/{env['BITBUCKET_REPO_SLUG']}/addon"
                            f"/pipelines/home#!/results/{env['BITBUCKET_BUILD_NUMBER']}",
        "CDB_SRC_REPO_ROOT": f"{env['BITBUCKET_CLONE_DIR']}/"
    }
    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        adapt_create_release_variables()
