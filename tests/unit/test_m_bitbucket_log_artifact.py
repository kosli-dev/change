from commands import run, External

from tests.utils import *

BB = "https://bitbucket.org"
BB_ORG = 'acme'
BB_REPO = 'road-runner'
COMMIT = "abc50c8a53f79974d615df335669b59fb56a4ed3"
BUILD_NUMBER = '1975'

DOMAIN = "app.compliancedb.com"
OWNER = "merkely"
PIPELINE = "test-pipefile"
API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"

IMAGE_NAME = "acme/road-runner:4.67"
SHA256 = "aacdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee"


def test_required_env_vars(capsys):
    expected_method = "Putting"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/artifacts/"
    expected_payload = {
        "build_url": f"{BB}/{BB_ORG}/{BB_REPO}/addon/pipelines/home#!/results/{BUILD_NUMBER}",
        "commit_url": f"{BB}/{BB_ORG}/{BB_REPO}/commits/{COMMIT}",
        "description": f"Created by build {BUILD_NUMBER}",
        "filename": IMAGE_NAME,
        "git_commit": COMMIT,
        "is_compliant": False,
        "sha256": SHA256,
        "user_data": {},
    }

    # make merkely call
    ev = new_log_artifact_env()
    with dry_run(ev) as env:
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            external = External(env=env, docker_fingerprinter=fingerprinter)
            method, url, payload = run(external)

    capsys_read(capsys)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload


def new_log_artifact_env():
    protocol = "docker://"
    return {
        "MERKELY_COMMAND": "log_artifact",
        "MERKELY_OWNER": OWNER,
        "MERKELY_PIPELINE": PIPELINE,
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{DOMAIN}",
        "MERKELY_FINGERPRINT": f"{protocol}{IMAGE_NAME}",

        "MERKELY_IS_COMPLIANT": "FALSE",

        "BITBUCKET_WORKSPACE": BB_ORG,
        "BITBUCKET_REPO_SLUG": BB_REPO,
        "BITBUCKET_COMMIT": COMMIT,
        "BITBUCKET_BUILD_NUMBER": BUILD_NUMBER,
    }
