from commands import run, External
from errors import ChangeError

from tests.utils import *
from pytest import raises

DOMAIN = "app.compliancedb.com"
OWNER = "compliancedb"
PIPELINE = "cdb-controls-test-pipeline"

API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"


def test_docker_image(capsys):
    image_name = "acme/runner:4.56"
    sha256 = "bbcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db46212"

    expected_method = "POST"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/approvals/"
    expected_payload = {
        "artifact_sha256": sha256,
        "description": "The approval description here",
        'user_data': {},
        "src_commit_list": [
            "8f5b384644eb83e7f2a6d9499539a077e7256b8b",
            "e0ad84e1a2464a9486e777c1ecde162edff930a9"
        ],
        "approvals": [
            {
                "state": "APPROVED",
                "comment": "The approval description here",
                "approved_by": "External",
                "approval_url": "undefined"
            }
        ]
    }

    ev = new_approve_deployment_env()
    with dry_run(ev) as env:
        with ScopedDirCopier("/test_src", "/src"):
            with MockDockerFingerprinter(image_name, sha256) as fingerprinter:
                external = External(env=env, docker_fingerprinter=fingerprinter)
                method, url, payload = run(external)

    capsys_read(capsys)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload


def test_raises_when_src_repo_root_does_not_exist():
    ev = new_approve_deployment_env()
    with dry_run(ev) as env:
        with raises(ChangeError) as exc:
            run(External(env=env))

    assert str(exc.value) == "Error: Repository not found at /src/.git"


def new_approve_deployment_env():
    protocol = "docker://"
    image_name = "acme/runner:4.56"
    return {
        "MERKELY_COMMAND": "approve_deployment",
        "MERKELY_OWNER": OWNER,
        "MERKELY_PIPELINE": PIPELINE,
        "MERKELY_FINGERPRINT": f"{protocol}{image_name}",
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{DOMAIN}",
        "MERKELY_OLDEST_SRC_COMMITISH": "production",
        "MERKELY_NEWEST_SRC_COMMITISH": "master",
        "MERKELY_DESCRIPTION": "The approval description here",
    }

