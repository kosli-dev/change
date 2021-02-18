from commands.bitbucket import BitbucketPipe, schema

from tests.utils import *

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_bitbucket_log_artifact"


def test_required_env_vars(mocker): #capsys, mocker):
    bitbucket_commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    env = {
        "CDB_COMMAND": "put_artifact_image",
        "CDB_PIPELINE_DEFINITION": "tests/data/pipefile.json",
        "CDB_API_TOKEN": "SOME_RANDOM_TOKEN",
        "CDB_ARTIFACT_DOCKER_IMAGE": "acme/road-runner:4.67",
        "BITBUCKET_COMMIT": bitbucket_commit,
        "BITBUCKET_BUILD_NUMBER": "1975",
        "BITBUCKET_WORKSPACE": "acme",
        "BITBUCKET_REPO_SLUG": "road-runner"
    }
    sha = "aacdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee"
    set_env_vars = {
        'CDB_ARTIFACT_GIT_URL': 'https://bitbucket.org/acme/road-runner/commits/' + bitbucket_commit,
        'CDB_ARTIFACT_GIT_COMMIT': bitbucket_commit,
        'CDB_BUILD_NUMBER': '1975',
        'CDB_CI_BUILD_URL': 'https://bitbucket.org/acme/road-runner/addon/pipelines/home#!/results/1975',
        'CDB_ARTIFACT_SHA': 'aacdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee'
    }
    with dry_run(env, set_env_vars):
        pipe = BitbucketPipe(pipe_metadata='/pipe.yml', schema=schema)
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha)
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
    #expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{NAME}/deployments/"
    expected_url = "https://app.compliancedb.com/api/v1/projects/merkely/test-pipefile/artifacts/"
    expected_payload = {
        "build_url": "https://bitbucket.org/acme/road-runner/addon/pipelines/home#!/results/1975",
        "commit_url": "https://bitbucket.org/acme/road-runner/commits/abc50c8a53f79974d615df335669b59fb56a4ed3",
        "description": "Created by build 1975",
        "filename": "acme/road-runner:4.67",
        "git_commit": "abc50c8a53f79974d615df335669b59fb56a4ed3",
        "is_compliant": False,
        "sha256": "aacdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee"
    }

    # verify data from approved cdb text file
    assert old_payload == expected_payload
    assert old_method == expected_method
    assert old_url == expected_url

