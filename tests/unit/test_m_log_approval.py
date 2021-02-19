from cdb.create_approval import create_approval
from commands import run, CommandError

from tests.utils import *
from pytest import raises


CDB_DOMAIN = "app.compliancedb.com"
CDB_OWNER = "compliancedb"
CDB_NAME = "cdb-controls-test-pipeline"

API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_log_approval"


def test_docker_image(capsys, mocker):
    image_name = "acme/runner:4.56"
    sha256 = "bbcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"
    merkleypipe_dir = "tests/data"
    merkelypipe = "test-pipefile.json"
    mock_artifacts_for_commit = {
        "artifacts": [{"sha256": sha256}]
    }
    env = {
        "CDB_API_TOKEN": API_TOKEN,
        "CDB_ARTIFACT_DOCKER_IMAGE": image_name,
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
        "CDB_DESCRIPTION": "The approval description here",
        "CDB_IS_APPROVED_EXTERNALLY": "TRUE",
    }
    set_env_vars = {"CDB_ARTIFACT_SHA": sha256}
    with dry_run(env, set_env_vars) as env, ScopedDirCopier("/test_src", "/src"):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha256)
        mocker.patch('cdb.create_release.get_artifacts_for_commit', return_value=mock_artifacts_for_commit)
        create_approval(f"{merkleypipe_dir}/{merkelypipe}", env)

    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_docker_image"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = CDB_DOMAIN
    owner = CDB_OWNER
    name = CDB_NAME

    expected_method = "Posting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/approvals/"
    expected_payload = {
        "artifact_sha256": sha256,
        "description": "The approval description here",
        "is_approved": True,
        "src_commit_list": [
            "8f5b384644eb83e7f2a6d9499539a077e7256b8b",
            "e0ad84e1a2464a9486e777c1ecde162edff930a9"
        ],
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload

    # make merkely call
    ev = new_log_approval_env()
    with dry_run(ev) as env:
        with ScopedDirCopier("/test_src", "/src"):
            with scoped_merkelypipe_json(directory=merkleypipe_dir, filename=merkelypipe):
                with MockDockerFingerprinter(image_name, sha256) as fingerprinter:
                    method, url, payload = run(env=env, docker_fingerprinter=fingerprinter)

    capsys_read(capsys)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload


def test_raises_when_src_repo_root_does_not_exist(capsys):
    merkleypipe_dir = "tests/data"
    merkelypipe = "test-pipefile.json"

    # make merkely call
    ev = new_log_approval_env()
    with dry_run(ev) as env:
        with scoped_merkelypipe_json(directory=merkleypipe_dir, filename=merkelypipe):
            with raises(CommandError) as exc:
                run(env=env)

    silent(capsys)
    assert str(exc.value) == "Error: Repository not found at /src/.git"


def new_log_approval_env():
    protocol = "docker://"
    image_name = "acme/runner:4.56"
    domain = CDB_DOMAIN
    return {
        "MERKELY_COMMAND": "log_approval",
        "MERKELY_FINGERPRINT": f"{protocol}{image_name}",
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{domain}",
        "MERKELY_TARGET_SRC_COMMITISH": "master",
        "MERKELY_BASE_SRC_COMMITISH": "production",
        "MERKELY_DESCRIPTION": "The approval description here",
        'MERKELY_IS_APPROVED': 'TRUE',
    }