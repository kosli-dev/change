from cdb.put_pipeline import put_pipeline
from commands import run, External

from tests.utils import *

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_bitbucket_declare_pipeline"

DOMAIN = "app.compliancedb.com"
OWNER = "acme"
PIPELINE = "road-runner"
API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"


def test_bitbucket(capsys):
    env = {"CDB_API_TOKEN": API_TOKEN}
    with dry_run({}):
        put_pipeline("tests/data/Merkelypipe.acme-roadrunner.json", env)

    verify_approval(capsys)

    # extract data from approved cdb text file
    import inspect
    this_test = inspect.stack()[0].function
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

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

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload

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
