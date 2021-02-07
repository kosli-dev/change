from cdb.put_artifact import put_artifact

from tests.utils import *

APPROVAL_DIR = "tests/integration/approved_executions"
APPROVAL_FILE = "test_put_artifact"

def test_all_env_vars_uses_FILENAME_and_SHA(capsys):
    # Provides CDB_ARTIFACT_FILENAME and CDB_ARTIFACT_SHA.
    # Assumption is that CDB_ARTIFACT_FILENAME is naming a file
    # that is not volume-mounted, so the sha cannot be calculated
    # from the file, so SHA is passed too.

    commit = "abc50c8a53f79974d615df335669b59fb56a4ed4"
    artifact_name = "door-is-a.jar"
    sha256 = "444daef69c676c2466571d3211180d559ccc2032b258fc5e73f99a103db462ef"
    build_url = "https://gitlab/build/2156"

    env = {
        "CDB_HOST": "https://app.compliancedb.com",
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_FILENAME": artifact_name,
        "CDB_ARTIFACT_SHA": sha256,
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_ARTIFACT_GIT_URL": f"https://github/me/project/commit/{commit}",
        "CDB_ARTIFACT_GIT_COMMIT": commit,
        "CDB_CI_BUILD_URL": build_url,
        "CDB_BUILD_NUMBER": "2156"
    }
    set_env_vars = {}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        put_artifact("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_all_env_vars_uses_FILENAME_and_SHA"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    expected_payload = {
        "build_url": build_url,
        "commit_url": f"https://github/me/project/commit/{commit}",
        "description": "Created by build 2156",
        "filename": artifact_name,
        "git_commit": commit,
        "is_compliant": True,
        "sha256": sha256
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_required_env_vars_uses_CDB_ARTIFACT_FILENAME(capsys, mocker):
    # Does not provide CDB_ARTIFACT_SHA
    # Assumption is that CDB_ARTIFACT_FILENAME names a file
    # that is volume-mounted and the CDB_ARTIFACT_SHA is calculated.
    commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    build_url = "https://gitlab/build/1456"
    artifact_name = "jam.jar"
    env = {
        "CDB_API_TOKEN": "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_FILENAME": artifact_name,
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_ARTIFACT_GIT_URL": f"https://github/me/project/commit/{commit}",
        "CDB_ARTIFACT_GIT_COMMIT": commit,
        "CDB_CI_BUILD_URL": build_url,
        "CDB_BUILD_NUMBER": "1456"
    }
    sha256 = "ddcdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee"
    set_env_vars = {'CDB_ARTIFACT_SHA': sha256}

    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_file', return_value=sha256)
        put_artifact("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_required_env_vars_uses_CDB_ARTIFACT_FILENAME"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    expected_payload = {
        "build_url": build_url,
        "commit_url": f"https://github/me/project/commit/{commit}",
        "description": "Created by build 1456",
        "filename": artifact_name,
        "git_commit": commit,
        "is_compliant": True,
        "sha256": sha256
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


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
