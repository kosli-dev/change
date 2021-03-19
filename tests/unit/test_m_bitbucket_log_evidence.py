from cdb.put_evidence import put_evidence
from commands import run, External

from tests.utils import *

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_bitbucket_log_evidence"

BB = 'bitbucket.org'
BB_ORG = 'acme'
BB_REPO = 'road-runner'
COMMIT = "abc50c8a53f79974d615df335669b59fb56a4ed3"
BUILD_NUMBER = '1975'

IMAGE_NAME = "acme/road-runner:4.67"
SHA256 = "aacdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee"

DOMAIN = "app.compliancedb.com"
OWNER = "acme"
PIPELINE = "road-runner"
API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"

DESCRIPTION = "branch coverage"
EVIDENCE_TYPE = "unit_test"


def test_bitbucket(capsys, mocker):
    # The original bitbucket code did not do a translation for put_evidence
    env = old_log_evidence_env()
    set_env_vars = {}
    with dry_run(env, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=SHA256)
        put_evidence("tests/data/Merkelypipe.acme-roadrunner.json")

    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    import inspect
    this_test = inspect.stack()[0].function
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    expected_method = "Putting"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/artifacts/{SHA256}"
    expected_payload = {
        "contents": {
            "description": DESCRIPTION,
            "is_compliant": True,
            "url": f"https://{BB}/{BB_ORG}/{BB_REPO}/addon/pipelines/home#!/results/{BUILD_NUMBER}",
        },
        "evidence_type": EVIDENCE_TYPE
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload

    # make merkely call
    ev = new_log_evidence_env()
    with dry_run(ev) as env:
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            external = External(env=env, docker_fingerprinter=fingerprinter)
            method, url, payload = run(external)

    # CHANGE IN BEHAVIOUR
    expected_payload['user_data'] = {}

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    assert extract_blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_evidence',
        'MERKELY_IS_COMPLIANT: True',
    ]


def old_log_evidence_env():
    return {
        "CDB_API_TOKEN": API_TOKEN,
        "CDB_ARTIFACT_DOCKER_IMAGE": IMAGE_NAME,
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_EVIDENCE_TYPE": EVIDENCE_TYPE,
        "CDB_DESCRIPTION": DESCRIPTION,
        "CDB_CI_BUILD_URL": f"https://{BB}/{BB_ORG}/{BB_REPO}/addon/pipelines/home#!/results/{BUILD_NUMBER}",
    }


def new_log_evidence_env():
    protocol = "docker://"
    return {
        "MERKELY_COMMAND": "log_evidence",
        "MERKELY_OWNER": OWNER,
        "MERKELY_PIPELINE": PIPELINE,
        "MERKELY_FINGERPRINT": f"{protocol}{IMAGE_NAME}",
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{DOMAIN}",

        "MERKELY_IS_COMPLIANT": "TRUE",
        "MERKELY_EVIDENCE_TYPE": EVIDENCE_TYPE,
        "MERKELY_DESCRIPTION": DESCRIPTION,

        "BITBUCKET_WORKSPACE": BB_ORG,
        "BITBUCKET_REPO_SLUG": BB_REPO,
        "BITBUCKET_COMMIT": COMMIT,
        "BITBUCKET_BUILD_NUMBER": BUILD_NUMBER,
    }
