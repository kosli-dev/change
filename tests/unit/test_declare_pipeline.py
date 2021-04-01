from commands import run, External
from tests.utils import *


DOMAIN = "app.merkely.com"
OWNER = "acme"
PIPELINE = "lib-controls-test-pipeline"


def test_green(capsys):
    expected_method = "PUT"
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

    with dry_run(core_env_vars('declare_pipeline')) as env, scoped_merkelypipe_json():
        method, url, payload = run(External(env=env))

    capsys_read(capsys)

    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload
