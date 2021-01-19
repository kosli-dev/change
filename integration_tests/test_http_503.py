from cdb.put_pipeline import main as main_put_pipeline
from cdb.http_retry import MAX_RETRY_COUNT

import responses
import sys
from tests.utils import AutoEnvVars, verify_approval, stub_http_503, retry_backoff_factor


@responses.activate
def test_503_exception_for_put_pipeline_main(capsys, mocker):
    host = 'http://test.compliancedb.com'
    url = host + '/api/v1/projects/compliancedb/'
    _, _, api_token = stub_http_503('PUT', 1+MAX_RETRY_COUNT, url)
    env = {
        'CDB_HOST': host,
        'CDB_API_TOKEN': 'random-api-token',
    }
    mocker.patch.object(sys, 'argv', ['name', '--project', '/app/tests_data/pipefile.json'])

    with retry_backoff_factor(0.001), AutoEnvVars(env):
        exit_code = main_put_pipeline()

    assert exit_code != 0
    verify_approval(capsys)
