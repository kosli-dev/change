from cdb.control_junit import control_junit
import docker

from pytest import raises
from tests.utils import *

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_log_test"


def test_docker_image(capsys, mocker):
    image_name = "acme/widget:3.4"
    sha256 = "aecdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    build_url = "https://gitlab/build/1457"
    evidence_type = "coverage"
    env = {
        "CDB_API_TOKEN": "7199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4",
        "CDB_ARTIFACT_DOCKER_IMAGE": image_name,
        "CDB_EVIDENCE_TYPE": evidence_type,
        "CDB_CI_BUILD_URL": build_url
    }
    set_env_vars = {}
    with dry_run(env, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha256)
        control_junit("tests/integration/test-pipefile.json")
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_docker_image"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/{sha256}"
    expected_payload = {
        "contents": {
            "description": "JUnit results xml verified by compliancedb/cdb_controls: All tests passed in 0 test suites",
            "is_compliant": True,
            "url": build_url
        },
        "evidence_type": evidence_type
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload
