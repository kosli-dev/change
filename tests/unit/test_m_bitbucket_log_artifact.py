from commands import run
from commands.bitbucket import BitbucketPipe, schema

from tests.utils import *

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_bitbucket_log_artifact"

DOMAIN = "app.compliancedb.com"
API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"
BUILD_NUMBER = '1975'
COMMIT = "abc50c8a53f79974d615df335669b59fb56a4ed3"
PROTOCOL = "docker://"
IMAGE_NAME = "acme/road-runner:4.67"
SHA256 = "aacdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee"
BB = "https://bitbucket.org"
ORG = 'acme'
REPO = 'road-runner'


def test_required_env_vars(capsys, mocker):

    merkelypipe = "pipefile.json"

    env = {
        "CDB_COMMAND": "put_artifact_image",
        "CDB_PIPELINE_DEFINITION": f"tests/data/{merkelypipe}",
        "CDB_API_TOKEN": API_TOKEN,
        "CDB_ARTIFACT_DOCKER_IMAGE": IMAGE_NAME,
        "BITBUCKET_COMMIT": COMMIT,
        "BITBUCKET_BUILD_NUMBER": BUILD_NUMBER,
        "BITBUCKET_WORKSPACE": ORG,
        "BITBUCKET_REPO_SLUG": REPO
    }
    set_env_vars = {
        'CDB_ARTIFACT_GIT_URL': f"{BB}/{ORG}/{REPO}/commits/{COMMIT}",
        'CDB_ARTIFACT_GIT_COMMIT': COMMIT,
        'CDB_BUILD_NUMBER': BUILD_NUMBER,
        'CDB_CI_BUILD_URL': f'{BB}/{ORG}/{REPO}/addon/pipelines/home#!/results/{BUILD_NUMBER}',
        'CDB_ARTIFACT_SHA': SHA256,
    }
    with dry_run(env, set_env_vars):
        pipe = BitbucketPipe(pipe_metadata='/pipe.yml', schema=schema)
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=SHA256)
        pipe.run()

    # extract data from approved cdb text file
    import inspect
    this_test = inspect.stack()[0].function
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    expected_method = "Putting"
    expected_url = f"https://{DOMAIN}/api/v1/projects/merkely/test-pipefile/artifacts/"

    expected_payload = {
        "build_url": f"{BB}/{ORG}/{REPO}/addon/pipelines/home#!/results/{BUILD_NUMBER}",
        "commit_url": f"{BB}/{ORG}/{REPO}/commits/{COMMIT}",
        "description": f"Created by build {BUILD_NUMBER}",
        "filename": IMAGE_NAME,
        "git_commit": COMMIT,
        "is_compliant": False,
        "sha256": SHA256,
    }

    # verify data from approved cdb text file
    assert old_payload == expected_payload
    assert old_method == expected_method
    assert old_url == expected_url

    # make merkely call
    ev = new_log_artifact_env()
    merkelypipe = "pipefile.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(filename=merkelypipe):
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            method, url, payload = run(env=env, docker_fingerprinter=fingerprinter)

    capsys_read(capsys)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload


def new_log_artifact_env():
    return {
        "MERKELY_COMMAND": "log_artifact",
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{DOMAIN}",
        "MERKELY_FINGERPRINT": f"{PROTOCOL}{IMAGE_NAME}",
        "MERKELY_IS_COMPLIANT": "FALSE",

        "MERKELY_CI_BUILD_URL": f"{BB}/{ORG}/{REPO}/addon/pipelines/home#!/results/{BUILD_NUMBER}",

        "MERKELY_ARTIFACT_GIT_URL": f"{BB}/{ORG}/{REPO}/commits/{COMMIT}",

        #"MERKELY_ARTIFACT_GIT_COMMIT": COMMIT,
        "BITBUCKET_COMMIT": COMMIT,

        #"MERKELY_CI_BUILD_NUMBER": BUILD_NUMBER,
        "BITBUCKET_BUILD_NUMBER": BUILD_NUMBER
    }
