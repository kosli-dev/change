from cdb.put_pipeline import put_pipeline

from tests.utils import *

APPROVAL_DIR = "tests/integration/approved_executions"
APPROVAL_FILE = "test_put_pipeline"

def test_required_env_vars(capsys):
    env = {
        "CDB_API_TOKEN": "SOME_RANDOM_TOKEN",
    }

    with ScopedEnvVars(CDB_DRY_RUN):
        put_pipeline("tests/integration/test-pipefile.json", env)
    verify_approval(capsys)

    # extract data from approved cdb text file
    this_test = "test_required_env_vars"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/"
    expected_payload = {
        "description": "Test Pipeline Controls for ComplianceDB",
        "name": "cdb-controls-test-pipeline",
        "owner": owner,
        "template": [
            "artifact",
            "unit_test",
            "coverage"
        ],
        "visibility": "public"
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload


def test_all_env_vars(capsys):
    env = {
        "CDB_HOST": "https://app.compliancedb.com",  # optional
        "CDB_API_TOKEN": "SOME_RANDOM_TOKEN",
    }

    with ScopedEnvVars(CDB_DRY_RUN):
        put_pipeline("tests/integration/test-pipefile.json", env)
    verify_approval(capsys)

    # extract data from approved cdb text file
    this_test = "test_all_env_vars"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/"
    expected_payload = {
        "description": "Test Pipeline Controls for ComplianceDB",
        "name": "cdb-controls-test-pipeline",
        "owner": owner,
        "template": [
            "artifact",
            "unit_test",
            "coverage"
        ],
        "visibility": "public"
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload
