import json
import os
import sys

import requests

from cdb.cdb_utils import build_evidence_dict, send_evidence


def put_bitbucket_pull_request(project_config_file):

    pull_requests = get_pull_request_for_current_commit()

    print("Found pull request info: " + str(pull_requests))
    evidence = build_evidence_dict(
        is_compliant=True,
        evidence_type="pull_request",
        description="Bitbucket pull request",
        build_url=pull_requests[0]["pullRequestURL"])
    evidence["contents"]["source"] = pull_requests
    send_evidence(project_config_file, evidence)


def get_pull_request_for_current_commit():
    workspace = os.getenv('BITBUCKET_WORKSPACE', None)
    repository = os.getenv('BITBUCKET_REPO_SLUG', None)
    commit = os.getenv('BITBUCKET_COMMIT', None)
    user = os.getenv('BITBUCKET_USER', None)
    password = os.getenv('BITBUCKET_PWD', None)
    pull_requests = get_pull_requests_from_bitbucket_api(
        workspace=workspace, repository=repository, commit=commit, username=user, password=password)
    return pull_requests


def get_pull_requests_from_bitbucket_api(workspace, repository, commit, username, password):
    pull_requests_evidence = []

    url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/commit/{commit}/pullrequests"
    r = requests.get(url, auth=(username, password))
    if r.status_code == 200:
        pull_requests_json = json.loads(r.text)
        pull_requests = pull_requests_json["values"]
        for pr in pull_requests:
            pr_evidence = {}

            pr_html_url = pr['links']['html']['href']
            pr_api_url = pr['links']['self']['href']

            pr_evidence['pullRequestMergeCommit'] = commit
            pr_evidence['pullRequestURL'] = pr_html_url

            pr_evidence = get_pull_request_details_from_bitbucket(pr_evidence, pr_api_url, username, password)

            pull_requests_evidence.append(pr_evidence)

    elif r.status_code == 202:
        print("Repository pull requests are still being indexed, please retry.")
        sys.exit(1)
    elif r.status_code == 404:
        print("Repository does not exists or pull requests are not indexed. Please make sure Pull Request Commit Links app is installed")
        sys.exit(2)
    else:
        print(f"Exception occured in fetching pull requests. Http return code is {r.status_code}")
        sys.exit(3)

    return pull_requests_evidence


def get_pull_request_details_from_bitbucket(pr_evidence, pr_api_url, username, password):
    r = requests.get(pr_api_url, auth=(username, password))
    if r.status_code == 200:
        pr_json = json.loads(r.text)
        pr_evidence['pullRequestState'] = pr_json['state']
        participants = pr_json['participants']
        approvers = ""
        if len(participants) > 0:
            for participant in participants:
                if participant['approved']:
                    approvers = approvers + participant['user']['display_name'] + ","
            approvers = approvers[:-1]
            pr_evidence['approvers'] = approvers
        else:
            print("No approvers found")
    else:
        print("Error occured in fetching pull request details. Please review repository permissions.")
    return pr_evidence





