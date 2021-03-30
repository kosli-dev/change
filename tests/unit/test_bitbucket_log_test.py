from commands import run, External

from tests.utils import *

BB = "bitbucket.org"
BB_ORG = 'acme'
BB_REPO = 'beep-beep'
COMMIT = "abc50c8a53f79974d615df335669b59fb56a4ed3"
BUILD_NUMBER = '703'

PROTOCOL = "docker://"
IMAGE_NAME = "acme/road-runner:4.67"
SHA256 = "aacdaef69c676c2466571d3277770d559ccc2032b258fc5e73f99a103db462ee"
EVIDENCE_TYPE = "junit"

USER_DATA = "/app/tests/data/user_data.json"

DOMAIN = "app.merkely.com"
OWNER = "acme"
PIPELINE = "test-pipefile"
API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"


def test_bitbucket(capsys):
    expected_method = "PUT"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/artifacts/{SHA256}"
    expected_payload = {
        "contents": {
            "description": "JUnit results xml verified by merkely/change: Tests contain failures",
            "is_compliant": False,
            "url": f"https://{BB}/{BB_ORG}/{BB_REPO}/addon/pipelines/home#!/results/{BUILD_NUMBER}"
        },
        "evidence_type": EVIDENCE_TYPE,
        "user_data": {
            "status": "deployed"
        },
    }

    ev = log_test_env()
    with dry_run(ev) as env:
        with ScopedDirCopier('/app/tests/data/control_junit/xml_with_fails', '/data/junit'):
            with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
                external = External(env=env, docker_fingerprinter=fingerprinter)
                method, url, payload = run(external)

    capsys_read(capsys)

    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload


def log_test_env():
    return {
        "MERKELY_COMMAND": "log_test",
        "MERKELY_OWNER": OWNER,
        "MERKELY_PIPELINE": PIPELINE,
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{DOMAIN}",
        "MERKELY_FINGERPRINT": f"{PROTOCOL}{IMAGE_NAME}",
        
        "MERKELY_EVIDENCE_TYPE": EVIDENCE_TYPE,
        "MERKELY_USER_DATA": USER_DATA,

        "BITBUCKET_WORKSPACE": BB_ORG,
        "BITBUCKET_REPO_SLUG": BB_REPO,
        "BITBUCKET_COMMIT": COMMIT,
        "BITBUCKET_BUILD_NUMBER": BUILD_NUMBER,
    }
