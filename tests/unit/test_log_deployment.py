from commands import run, External
from tests.utils import *

DOMAIN = "app.merkely.com"
OWNER = "acme"
NAME = "lib-controls-test-pipeline"

DESCRIPTION = "some description"
ENVIRONMENT = "production"
CI_BUILD_URL = "https://gitlab/build/1456"

IMAGE_NAME = "acme/road-runner:4.56"
SHA256 = "efcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"

USER_DATA = "/app/tests/data/user_data.json"


def test_docker_image():
    expected_method = "POST"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{NAME}/deployments/"
    expected_payload = {
        "artifact_sha256": SHA256,
        "build_url": CI_BUILD_URL,
        "description": DESCRIPTION,
        "environment": ENVIRONMENT,
        "user_data": {'status': 'deployed'},
    }

    protocol = "docker://"
    env = dry_run(log_deployment_env())
    env["MERKELY_FINGERPRINT"] = f"{protocol}{IMAGE_NAME}"
    with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
        external = External(env=env, docker_fingerprinter=fingerprinter)
        method, url, payload = run(external)

    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload
    stdout = external.stdout.getvalue()
    assert extract_blurb(stdout) == [
        'MERKELY_COMMAND=log_deployment',
        'Posting this payload:',
    ]


def log_deployment_env():
    ev = {
        "MERKELY_CI_BUILD_URL": CI_BUILD_URL,
        "MERKELY_ENVIRONMENT": ENVIRONMENT,
        "MERKELY_DESCRIPTION": DESCRIPTION,
        "MERKELY_HOST": f"https://{DOMAIN}",
        "MERKELY_USER_DATA": USER_DATA,
    }
    # MERKELY_OWNER and MERKELY_PIPELINE set in core_env_vars
    return {**core_env_vars("log_deployment"), **ev}

