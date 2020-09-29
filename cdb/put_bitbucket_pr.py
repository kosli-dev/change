import json
import os
import sys

import requests

from cdb.cdb_utils import get_host, get_api_token, get_artifact_sha, parse_cmd_line, load_project_configuration, \
    build_evidence_dict, send_evidence


def getPullRequestsForCommit(workspace, repository, commit, uname, password):
    pull_reqests_for_commit = []
    url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/commit/{commit}/pullrequests"
    r = requests.get(url, auth=(uname, password))
    if r.status_code == 200:
        pullrequestsofcommit = json.loads(r.text)
        pullrequestslist = pullrequestsofcommit["values"]
        for pr in pullrequestslist:
            details = {}
            urlforapi = pr['links']['self']['href']
            htmlurl = pr['links']['html']['href']
            details['pullRequestURL'] = htmlurl
            details['pullRequestMergeCommit'] = commit
            # pull_reqest_dict[count] = details
            details = getPullRequestDetails(details, urlforapi, uname, password)
            pull_reqests_for_commit.append(details)
    elif r.status_code == 202:
        print("Repository pull requests are still being indexed, please retry.")
        sys.exit(1)
    elif r.status_code == 404:
        print("Repository does not exists or pull requests are not indexed. Please make sure Pull Request Commit Links app is installed")
        sys.exit(2)
    else:
        print(f"Exception occured in fetching pull requests. Http return code is {r.status_code}")
        sys.exit(3)
    return pull_reqests_for_commit


def getPullRequestDetails(details, pullrequesturl, uname, password):
    r = requests.get(pullrequesturl, auth=(uname, password))
    if r.status_code == 200:
        pullrequest = json.loads(r.text)
        details['pullRequestState'] = pullrequest['state']
        participants = pullrequest['participants']
        approvers = ""
        if len(participants) > 0:
            for participant in participants:
                if participant['approved'] == True:
                    approvers = approvers + participant['user']['display_name'] + ","
            approvers = approvers[:-1]
            details['approvers'] = approvers
        else:
            print("No approvers found")
    else:
        print("Error occured in fetching pull request details. Please review repository permissions.")
    return details


if __name__ == '__main__':
    host = get_host()
    api_token = get_api_token()
    artifact_sha = get_artifact_sha()
    project_config_file = parse_cmd_line()

    workspace = os.getenv('BITBUCKET_WORKSPACE', None)
    repository = os.getenv('BITBUCKET_REPO_SLUG', None)
    commit = os.getenv('BITBUCKET_COMMIT', None)
    user = os.getenv('BITBUCKET_USER', None)
    password = os.getenv('BITBUCKET_PWD', None)

    with open(project_config_file) as json_data_file:
        project_data = load_project_configuration(json_data_file)
        pull_requests = getPullRequestsForCommit(
            workspace=workspace, repository=repository, commit=commit, uname=user, password=password)
        print("Found pull request info: " + str(pull_requests))
        evidence = build_evidence_dict(
            is_compliant=True,
            evidence_type="pull_request",
            description="Bitbucket pull request",
            build_url=pull_requests[0]["pullRequestURL"])
        evidence["contents"]["source"] = pull_requests
        send_evidence(evidence)