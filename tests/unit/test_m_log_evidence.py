from cdb.put_evidence import put_evidence
from commands import run, LogEvidence

from tests.utils import *

MERKELY_DOMAIN = "test.compliancedb.com"
CDB_DOMAIN = "app.compliancedb.com"
CDB_OWNER = "compliancedb"
CDB_NAME = "cdb-controls-test-pipeline"

API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_log_evidence"


def test_docker_protocol(capsys, mocker):
    # input data
    build_url = "https://gitlab/build/1956"
    sha256 = "bbcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    protocol = "docker://"
    image_name = "acme/widget:4.67"

    domain = CDB_DOMAIN
    owner = CDB_OWNER
    name = CDB_NAME

    # make cdb call
    cdb_env = {
        "CDB_API_TOKEN": API_TOKEN,
        "CDB_ARTIFACT_DOCKER_IMAGE": image_name,
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_EVIDENCE_TYPE": "unit_test",
        "CDB_DESCRIPTION": "branch coverage",
        "CDB_CI_BUILD_URL": build_url,
    }
    with dry_run(cdb_env):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha256)
        put_evidence("tests/integration/test-pipefile.json")
        
    # compare with approved cdb text file
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_docker_protocol"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/{sha256}"
    expected_payload = {
        "contents": {
            "description": "branch coverage",
            "is_compliant": True,
            "url": build_url
        },
        "evidence_type": "unit_test"
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload

    # make merkely call
    ev = new_log_evidence_env()
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{image_name}"
    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(filename=merkelypipe):
        with MockDockerFingerprinter(image_name, sha256) as fingerprinter:
            method, url, payload = run(env, fingerprinter, None)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    assert extract_blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_evidence',
        'MERKELY_IS_COMPLIANT: True',
    ]


def test_summary_is_not_empty():
    context = {}
    command = LogEvidence(context)
    assert len(command.summary) > 0


def new_log_evidence_env():
    domain = CDB_DOMAIN
    build_url = "https://gitlab/build/1956"
    protocol = "docker://"
    image_name = "acme/widget:4.67"
    return {
        "MERKELY_COMMAND": "log_evidence",
        "MERKELY_FINGERPRINT": f"{protocol}{image_name}",
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{domain}",
        "MERKELY_CI_BUILD_URL": build_url,
        "MERKELY_IS_COMPLIANT": "TRUE",
        "MERKELY_EVIDENCE_TYPE": "unit_test",
        "MERKELY_DESCRIPTION": "branch coverage"
    }


