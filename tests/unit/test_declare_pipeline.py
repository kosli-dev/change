from commands import run, External
from tests.utils import *


DOMAIN = "app.merkely.com"
OWNER = "acme"
PIPELINE = "lib-controls-test-pipeline"


def test_green():
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

    env = dry_run(core_env_vars('declare_pipeline'))
    directory = "/app/tests/data"
    filename = "Merkelypipe.json"
    with ScopedFileCopier(f"{directory}/{filename}", "/data/Merkelypipe.json"):
        method, url, payload = run(External(env=env))

    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload
