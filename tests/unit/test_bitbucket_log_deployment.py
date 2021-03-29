from commands import run, External

from tests.utils import *

BB = 'bitbucket.org'
BB_ORG = 'acme'
BB_REPO = 'road-runner'
COMMIT = "abc50c8a53f79974d615df335669b59fb56a4ed3"
BUILD_NUMBER = '1975'

DOMAIN = "app.compliancedb.com"
OWNER = "acme"
PIPELINE = "road-runner"
API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"

IMAGE_NAME = "acme/road-runner:4.67"
SHA256 = "aacdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee"

DESCRIPTION = f"Deployment of {IMAGE_NAME}:aacdaef to docker hub"
ENVIRONMENT = "dockerhub"
USER_DATA = "/app/tests/data/user_data.json"
USER_DATA_JSON = {'status': 'deployed'}


def test_bitbucket(capsys):
    expected_method = "POST"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/deployments/"
    expected_payload = {
        "artifact_sha256": SHA256,
        "build_url": f"https://{BB}/{BB_ORG}/{BB_REPO}/addon/pipelines/home#!/results/{BUILD_NUMBER}",
        "description": DESCRIPTION,
        "environment": ENVIRONMENT,
        "user_data": USER_DATA_JSON,
    }

    # make merkely call
    ev = new_log_deployment_env()
    with dry_run(ev) as env:
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            external = External(env=env, docker_fingerprinter=fingerprinter)
            method, url, payload = run(external)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    assert extract_blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_deployment',
    ]


def new_log_deployment_env():
    protocol = "docker://"
    return {
        "MERKELY_COMMAND": "log_deployment",
        "MERKELY_OWNER": OWNER,
        "MERKELY_PIPELINE": PIPELINE,
        "MERKELY_FINGERPRINT": f"{protocol}{IMAGE_NAME}",
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{DOMAIN}",

        "MERKELY_DESCRIPTION": DESCRIPTION,
        "MERKELY_ENVIRONMENT": ENVIRONMENT,
        "MERKELY_USER_DATA": USER_DATA,

        "BITBUCKET_WORKSPACE": BB_ORG,
        "BITBUCKET_REPO_SLUG": BB_REPO,
        "BITBUCKET_COMMIT": COMMIT,
        "BITBUCKET_BUILD_NUMBER": BUILD_NUMBER,
    }
