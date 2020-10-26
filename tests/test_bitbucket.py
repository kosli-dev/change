
"""
"pull_request": {
      "is_compliant": false,
      "url": "https://bitbucket.org/meekrosoft/demo_bitbucket_pipe/pull-requests/1",
      "description": "Bitbucket pull request",
      "source": [
        {
          "pullRequestMergeCommit": "d7f5d5b11b268a70684f8683b411caed57da9d34",
          "pullRequestURL": "https://bitbucket.org/meekrosoft/demo_bitbucket_pipe/pull-requests/1",
          "pullRequestState": "OPEN"
        }
      ]
"""
from cdb.bitbucket import verify_pull_request_evidence

OPEN_PR_EVIDENCE = {
    "pull_request": {
        "is_compliant": False,
        "url": "https://bitbucket.org/meekrosoft/demo_bitbucket_pipe/pull-requests/1",
        "description": "Bitbucket pull request",
        "source": [
            {
              "pullRequestMergeCommit": "d7f5d5b11b268a70684f8683b411caed57da9d34",
              "pullRequestURL": "https://bitbucket.org/meekrosoft/demo_bitbucket_pipe/pull-requests/1",
              "pullRequestState": "OPEN"
            }
        ]
    }
}


def test_verify_pull_request_evidence_true_if_force_compliant():
    is_compliant = verify_pull_request_evidence(OPEN_PR_EVIDENCE, force_compliant=True)
    assert is_compliant is True

