from pipe import BitbucketPipe, schema

from tests.utils import ScopedEnvVars, CDB_DRY_RUN, verify_approval


def test_required_env_vars(capsys, mocker):
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
    with ScopedEnvVars({**CDB_DRY_RUN, **env}, set_env_vars):
        pipe = BitbucketPipe(pipe_metadata='/pipe.yml', schema=schema)
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha)
        pipe.run()
    verify_approval(capsys)


