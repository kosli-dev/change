#import os
import responses
import requests as r

from cdb.create_approval import create_approval
from tests.test_git import TEST_REPO_ROOT


"""
responses is a library for mocking out the requests Python library.
https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#combining-timeouts-and-retries
https://github.com/getsentry/responses
"""

@responses.activate
def test_create_approval_with_responses_mock():
    #os.environ["CDB_DRY_RUN"] = "FALSE"

    responses.add(responses.POST, 'https://app.compliancedb.com/api/v1/projects/compliancedb/cdb-controls-test-pipeline/approvals/',
                      json={'error': 'service unavailable'}, status=503)
    env = {
        "CDB_ARTIFACT_SHA": "1234",
        "CDB_BASE_SRC_COMMITISH": "production",
        "CDB_TARGET_SRC_COMMITISH": "master",
        "CDB_DESCRIPTION": "Description",
        "CDB_IS_APPROVED_EXTERNALLY": "FALSE",
        "CDB_SRC_REPO_ROOT": TEST_REPO_ROOT,
    }
    create_approval("integration_tests/test-pipefile.json", env=env)


