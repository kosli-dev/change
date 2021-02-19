from commands import run
from commands.bitbucket import BitbucketPipe, schema

from tests.utils import *

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_bitbucket_log_artifact"

API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"
#BUILD_URL = 'https://gitlab/build/1456'
BUILD_NUMBER = '1975'


def test_required_env_vars(mocker): #capsys, mocker):
    commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    image_name = "acme/road-runner:4.67"

    merkelypipe = "pipefile.json"

    env = {
        "CDB_COMMAND": "put_artifact_image",
        "CDB_PIPELINE_DEFINITION": f"tests/data/{merkelypipe}",
        "CDB_API_TOKEN": API_TOKEN,
        "CDB_ARTIFACT_DOCKER_IMAGE": image_name,
        "BITBUCKET_COMMIT": commit,
        "BITBUCKET_BUILD_NUMBER": BUILD_NUMBER,
        "BITBUCKET_WORKSPACE": "acme",
        "BITBUCKET_REPO_SLUG": "road-runner"
    }
    sha256 = "aacdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee"
    set_env_vars = {
        'CDB_ARTIFACT_GIT_URL': 'https://bitbucket.org/acme/road-runner/commits/' + commit,
        'CDB_ARTIFACT_GIT_COMMIT': commit,
        'CDB_BUILD_NUMBER': BUILD_NUMBER,
        'CDB_CI_BUILD_URL': 'https://bitbucket.org/acme/road-runner/addon/pipelines/home#!/results/1975',
        'CDB_ARTIFACT_SHA': sha256,
    }
    with dry_run(env, set_env_vars):
        pipe = BitbucketPipe(pipe_metadata='/pipe.yml', schema=schema)
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha256)
        pipe.run()

    #verify_approval(capsys)

    # extract data from approved cdb text file
    import inspect
    this_test = inspect.stack()[0].function
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    expected_method = "Putting"
    expected_url = "https://app.compliancedb.com/api/v1/projects/merkely/test-pipefile/artifacts/"
    expected_payload = {
        "build_url": f"https://bitbucket.org/acme/road-runner/addon/pipelines/home#!/results/{BUILD_NUMBER}",
        "commit_url": f"https://bitbucket.org/acme/road-runner/commits/{commit}",
        "description": f"Created by build {BUILD_NUMBER}",
        "filename": image_name,
        "git_commit": commit,
        "is_compliant": False,
        "sha256": sha256,
    }

    # verify data from approved cdb text file
    assert old_payload == expected_payload
    assert old_method == expected_method
    assert old_url == expected_url

    # make merkely call
    protocol = "docker://"
    ev = new_log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{image_name}"
    #merkelypipe = "Merkelypipe.compliancedb.json"
    merkelypipe = "pipefile.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(filename=merkelypipe):
        with MockDockerFingerprinter(image_name, sha256) as fingerprinter:
            method, url, payload = run(env, fingerprinter, None)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload


def new_log_artifact_env(commit=None):
    if commit is None:
        commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    domain = "app.compliancedb.com"
    return {
        "MERKELY_COMMAND": "log_artifact",
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{domain}",
        "MERKELY_FINGERPRINT": 'docker://acme/road-runner:2.3',
        "MERKELY_CI_BUILD_URL": 'XXXXXX',
        "MERKELY_CI_BUILD_NUMBER": BUILD_NUMBER,
        "MERKELY_ARTIFACT_GIT_URL": commit_url(commit),
        "MERKELY_ARTIFACT_GIT_COMMIT": commit,
        "MERKELY_IS_COMPLIANT": "TRUE",

        "BITBUCKET_COMMIT": commit,
    }


def commit_url(commit):
    return f"https://github/me/project/commit/{commit}"
