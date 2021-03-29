from commands import run, External

from tests.utils import *

DOMAIN = "app.compliancedb.com"
OWNER = "acme"
PIPELINE = "road-runner"
API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"


def test_bitbucket(capsys):
    expected_method = "Putting"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/"
    expected_payload = {
        "owner": OWNER,
        "name": PIPELINE,
        "description": "Test Pipeline for merkely/change",
        "template": [
            "artifact",
            "unit_test",
            "coverage"
        ],
        "visibility": "public"
    }

    # make merkely call
    ev = new_declare_pipeline_env()
    merkelypipe = "Merkelypipe.acme-roadrunner.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(filename=merkelypipe):
        method, url, payload = run(External(env=env))

    capsys_read(capsys)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload


def new_declare_pipeline_env():
    return {
        "MERKELY_COMMAND": "declare_pipeline",
        "MERKELY_OWNER": OWNER,
        "MERKELY_PIPELINE": PIPELINE,
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{DOMAIN}",
    }
