from commands import run

from tests.utils import *

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_log_evidence"

DOMAIN = 'bitbucket.org'
API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"
ORG = 'acme'
REPO = 'road-runner'
BUILD_NUMBER = '1975'
COMMIT = "abc50c8a53f79974d615df335669b59fb56a4ed3"
SHA256 = "aacdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee"
PROTOCOL = "docker://"
IMAGE_NAME = "acme/road-runner:4.67"


def test_bitbucket(capsys):
    # The original bitbucket code did not do a translation for put_evidence

    expected_method = "Putting"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{ORG}/{REPO}/artifacts/{SHA256}"
    expected_payload = {
        "contents": {
            "description": "branch coverage",
            "is_compliant": True,
            "url": f"https://{DOMAIN}/{ORG}/{REPO}/addon/pipelines/home#!/results/{BUILD_NUMBER}",
        },
        "evidence_type": "unit_test"
    }

    # make merkely call
    ev = new_log_evidence_env()
    merkelypipe = "Merkelypipe.acme-roadrunner.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(filename=merkelypipe):
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            method, url, payload = run(env=env, docker_fingerprinter=fingerprinter)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    assert extract_blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_evidence',
        'MERKELY_IS_COMPLIANT: True',
    ]


def new_log_evidence_env():
    return {
        "MERKELY_COMMAND": "log_evidence",
        "MERKELY_FINGERPRINT": f"{PROTOCOL}{IMAGE_NAME}",
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{DOMAIN}",
        "MERKELY_IS_COMPLIANT": "TRUE",
        "MERKELY_EVIDENCE_TYPE": "unit_test",
        "MERKELY_DESCRIPTION": "branch coverage",

        "BITBUCKET_WORKSPACE": ORG,
        "BITBUCKET_REPO_SLUG": REPO,
        "BITBUCKET_COMMIT": COMMIT,
        "BITBUCKET_BUILD_NUMBER": BUILD_NUMBER,
    }
