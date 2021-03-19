from commands import run, External
from commands.bitbucket import BitbucketPipe, schema

from tests.utils import *

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_bitbucket_log_test"

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

DOMAIN = "app.compliancedb.com"
OWNER = "merkely"
PIPELINE = "test-pipefile"
API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"


def test_bitbucket(capsys):
    env = {
        "CDB_COMMAND": "control_junit",
        "CDB_PIPELINE_DEFINITION": "tests/data/pipefile.json",
        "CDB_API_TOKEN": API_TOKEN,
        "CDB_ARTIFACT_SHA": SHA256,
        "CDB_TEST_RESULTS_DIR": "/app/tests/data/control_junit/xml-with-fails",
        "BITBUCKET_COMMIT": COMMIT,
        "BITBUCKET_BUILD_NUMBER": BUILD_NUMBER,
        "BITBUCKET_WORKSPACE": BB_ORG,
        "BITBUCKET_REPO_SLUG": BB_REPO,
    }
    set_env_vars = {
        'CDB_ARTIFACT_GIT_URL': f'https://{BB}/{BB_ORG}/{BB_REPO}/commits/{COMMIT}',
        'CDB_ARTIFACT_GIT_COMMIT': COMMIT,
        'CDB_BUILD_NUMBER': BUILD_NUMBER,
        'CDB_CI_BUILD_URL': f'https://{BB}/{BB_ORG}/{BB_REPO}/addon/pipelines/home#!/results/{BUILD_NUMBER}'
     }
    with dry_run(env, set_env_vars):
        pipe = BitbucketPipe(pipe_metadata='/pipe.yml', schema=schema)
        pipe.run()

    verify_approval(capsys)

    # extract data from approved cdb text file
    import inspect
    this_test = inspect.stack()[0].function
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    expected_method = "Putting"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/artifacts/{SHA256}"
    expected_payload = {
        "contents": {
            "description": "JUnit results xml verified by compliancedb/cdb_controls: Tests contain failures",
            "is_compliant": False,
            "url": f"https://{BB}/{BB_ORG}/{BB_REPO}/addon/pipelines/home#!/results/{BUILD_NUMBER}"
        },
        "evidence_type": EVIDENCE_TYPE
    }

    # verify data from approved cdb text file
    assert old_payload == expected_payload
    assert old_method == expected_method
    assert old_url == expected_url

    # make merkely call
    ev = new_log_test_env()
    with dry_run(ev) as env:
        with ScopedDirCopier('/app/tests/data/control_junit/xml-with-fails', '/data/junit'):
            with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
                external = External(env=env, docker_fingerprinter=fingerprinter)
                method, url, payload = run(external)

    capsys_read(capsys)

    # verify matching data
    assert method == expected_method
    assert url == expected_url

    # image name has changed
    old_description = expected_payload['contents']['description']
    new_description = old_description.replace('compliancedb/cdb_controls', 'merkely/change')
    expected_payload['contents']['description'] = new_description

    # user_data works did not work in cdb code
    expected_payload["user_data"] = {'status': 'deployed'}

    assert payload == expected_payload


def new_log_test_env():
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
