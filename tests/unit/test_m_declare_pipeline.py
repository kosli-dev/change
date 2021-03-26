from commands import run, External
from tests.utils import *


DOMAIN = "app.compliancedb.com"
OWNER = "compliancedb"

def test_green(capsys):
    expected_method = "Putting"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/"
    expected_payload = {
        "description": "Test Pipeline for merkely/change",
        "name": "cdb-controls-test-pipeline",
        "owner": OWNER,
        "template": [
            "artifact",
            "unit_test",
            "coverage"
        ],
        "visibility": "public"
    }

    # make merkely call
    with dry_run(core_env_vars()) as env, scoped_merkelypipe_json():
        method, url, payload = run(External(env=env))

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload
