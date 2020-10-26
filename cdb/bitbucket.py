import json
import os
import sys

import requests

from cdb.cdb_utils import build_evidence_dict, send_evidence


def put_bitbucket_pull_request(project_config_file):

    is_compliant, pull_requests = get_pull_request_for_current_commit()

    print("Found pull request info: " + str(pull_requests))
    evidence = build_evidence_dict(
        is_compliant=is_compliant,
        evidence_type="pull_request",
        description="Bitbucket pull request",
        build_url=get_bitbucket_repo_url())
    evidence["contents"]["source"] = pull_requests
    send_evidence(project_config_file, evidence)


def get_pull_request_for_current_commit():
    workspace = os.getenv('BITBUCKET_WORKSPACE', None)
    repository = os.getenv('BITBUCKET_REPO_SLUG', None)
    commit = os.getenv('BITBUCKET_COMMIT', None)
    user = os.getenv('BITBUCKET_API_USER', None)
    password = os.getenv('BITBUCKET_API_TOKEN', None)
    force_compliant = os.getenv('CDB_FORCE_COMPLIANT', "FALSE") == "TRUE"
    fail_pipeline = os.getenv('CDB_FAIL_PIPELINE', "TRUE") == "TRUE"
    
    is_compliant, pull_requests = get_pull_requests_from_bitbucket_api(
        workspace=workspace, repository=repository, commit=commit, username=user, password=password, 
        force_compliant=force_compliant, fail_pipeline=fail_pipeline)
    return is_compliant, pull_requests


def verify_pull_request_evidence(pull_requests_evidence, force_compliant):
    return True


def get_pull_requests_from_bitbucket_api(workspace, repository, commit, username, password, force_compliant, fail_pipeline):
    pull_requests_evidence = []
    is_compliant = False

    url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/commit/{commit}/pullrequests"
    print("Getting pull requests from " + url)
    r = requests.get(url, auth=(username, password))
    if r.status_code == 200:
        is_compliant = parse_response(commit, force_compliant, is_compliant, password, pull_requests_evidence, r,
                                      username)
    elif r.status_code == 202:
        print("Repository pull requests are still being indexed, please retry.")
        if fail_pipeline:
            sys.exit(1)
    elif r.status_code == 404:
        print("Repository does not exists or pull requests are not indexed. Please make sure Pull Request Commit Links app is installed")
        if fail_pipeline:
            sys.exit(2)
    else:
        print(f"Exception occurred in fetching pull requests. Http return code is {r.status_code}")
        print("    " + r.text)
        if fail_pipeline:
            sys.exit(3)

    return is_compliant, pull_requests_evidence


def parse_response(commit, force_compliant, is_compliant, password, pull_requests_evidence, r, username):
    print("Pull requests response: " + r.text)
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
    is_compliant = verify_pull_request_evidence(pull_requests_evidence, force_compliant)
    return is_compliant


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
        print("Error occurred in fetching pull request details. Please review repository permissions.")
    return pr_evidence


def get_bitbucket_repo_url():
    bb_workspace = os.environ.get("BITBUCKET_WORKSPACE")
    bb_repo_slug = os.environ.get("BITBUCKET_REPO_SLUG")
    repo_url = f"https://bitbucket.org/{bb_workspace}/{bb_repo_slug}"
    return repo_url
