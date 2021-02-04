from cdb.put_artifact import put_artifact

from tests.utils import ScopedEnvVars, CDB_DRY_RUN, verify_approval, silent


def test_required_env_vars_uses_CDB_ARTIFACT_FILENAME(capsys, mocker):
    # Does not provide CDB_ARTIFACT_SHA
    # Assumption is that CDB_ARTIFACT_FILENAME names a file
    # that is volume-mounted and the CDB_ARTIFACT_SHA is calculated.
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_FILENAME": "jam.jar",
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_ARTIFACT_GIT_URL": "http://github/me/project/commit/abc50c8a53f79974d615df335669b59fb56a4ed3",
        "CDB_ARTIFACT_GIT_COMMIT": "abc50c8a53f79974d615df335669b59fb56a4ed3",
        "CDB_CI_BUILD_URL": "https://gitlab/build/1456",
        "CDB_BUILD_NUMBER": "349"
    }
    sha = "ddcdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee"
    set_env_vars = {'CDB_ARTIFACT_SHA': sha}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_file', return_value=sha)
        put_artifact("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_all_env_vars_uses_FILENAME_and_SHA(capsys):
    # Provides CDB_ARTIFACT_FILENAME and CDB_ARTIFACT_SHA.
    # Assumption is that CDB_ARTIFACT_FILENAME is naming a file
    # that is not volume-mounted, so the sha cannot be calculated
    # from the file, so SHA is passed too.
    env = {
        "CDB_HOST": "http://test.compliancedb.com",
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_FILENAME": "src/data/widget.hpp",
        "CDB_ARTIFACT_SHA": "444daef69c676c2466571d3211180d559ccc2032b258fc5e73f99a103db462ef",
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_ARTIFACT_GIT_URL": "http://github/me/project/commit/abc50c8a53f79974d615df335669b59fb56a4ed3",
        "CDB_ARTIFACT_GIT_COMMIT": "abc50c8a53f79974d615df335669b59fb56a4ed4",
        "CDB_CI_BUILD_URL": "https://gitlab/build/2156",
        "CDB_BUILD_NUMBER": "751"
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_artifact("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])


def test_CDB_ARTIFACT_FILENAME_is_missing(capsys):
    set_env_vars = {}

    with ScopedEnvVars(CDB_DRY_RUN, set_env_vars), silent(capsys):
        put_artifact("tests/integration/test-pipefile.json")


def test_CDB_ARTIFACT_SHA_is_UNDEFINED(capsys):
    env = {
        "CDB_ARTIFACT_FILENAME": "tests/data/coverage.txt",
        "CDB_ARTIFACT_SHA": "UNDEFINED"
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars), silent(capsys):
        put_artifact("tests/integration/test-pipefile.json")


def test_CDB_ARTIFACT_SHA_is_not_defined(capsys):
    env = {
        "CDB_ARTIFACT_FILENAME": "tests/data/coverage.txt",
    }
    set_env_vars = {
        "CDB_ARTIFACT_SHA": "ccee89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    }

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars), silent(capsys):
        put_artifact("tests/integration/test-pipefile.json")


def test_CDB_ARTIFACT_SHA_is_defined(capsys):
    env = {
        "CDB_ARTIFACT_FILENAME": "tests/data/coverage.txt",
        "CDB_ARTIFACT_SHA": "ccee89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars), silent(capsys):
        put_artifact("tests/integration/test-pipefile.json")
