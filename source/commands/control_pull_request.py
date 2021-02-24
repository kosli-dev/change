import json
import requests
import sys

from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class ControlPullRequest(Command):

    @property
    def summary(self):
        return ""

    def invocation(self, _type):
        return ""

    def __call__(self):
        is_compliant, pull_requests = get_pull_request_for_current_commit(self.env)
        payload = {
            "evidence_type": self.evidence_type.value,
            "contents": {
                "is_compliant": is_compliant,
                "description": self.description.value,
                "url": self.ci_build_url.value,
                "source": pull_requests,
            }
        }
        url = ApiSchema.url_for_artifact(self.host.value, self.merkelypipe, self.fingerprint.sha)
        http_put_payload(url, payload, self.api_token.value)
        return 'Putting', url, payload

    @property
    def description(self):
        name = "MERKELY_DESCRIPTION"
        default = "Bitbucket pull request"
        notes = "Bitbucket pull request."
        return self._static_defaulted_env_var(name, default, notes)

    @property
    def evidence_type(self):
        name = "MERKELY_EVIDENCE_TYPE"
        default = "pull_request"
        notes = "The evidence type."
        return self._static_defaulted_env_var(name, default, notes)

    @property
    def _env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'ci_build_url',
            'description',
            'evidence_type',
            'api_token',
            'host',
        ]


def get_pull_request_for_current_commit(env):
    workspace = env.get('BITBUCKET_WORKSPACE', None)
    repository = env.get('BITBUCKET_REPO_SLUG', None)
    commit = env.get('BITBUCKET_COMMIT', None)
    user = env.get('BITBUCKET_API_USER', None)
    password = env.get('BITBUCKET_API_TOKEN', None)

    is_compliant, pull_requests = get_pull_requests_from_bitbucket_api(
        workspace=workspace, repository=repository, commit=commit,
        username=user, password=password)

    return is_compliant, pull_requests


def get_pull_requests_from_bitbucket_api(workspace, repository, commit, username, password):
    is_compliant = False
    pull_requests_evidence = []

    url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/commit/{commit}/pullrequests"
    print("Getting pull requests from " + url)
    r = requests.get(url, auth=(username, password))
    if r.status_code == 200:
        is_compliant = parse_response(commit, password, pull_requests_evidence, r, username)
    elif r.status_code == 202:
        print("Repository pull requests are still being indexed, please retry.")
        sys.exit(1)
    elif r.status_code == 404:
        print("Repository does not exists or pull requests are not indexed. Please make sure Pull Request Commit Links app is installed")
        sys.exit(2)
    else:
        print(f"Exception occurred in fetching pull requests. Http return code is {r.status_code}")
        print("    " + r.text)
        sys.exit(3)

    return is_compliant, pull_requests_evidence


def parse_response(commit, password, pull_requests_evidence, r, username):
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
    is_compliant = pull_requests_evidence != []
    return is_compliant


def get_pull_request_details_from_bitbucket(pr_evidence, pr_api_url, username, password):
    response = requests.get(pr_api_url, auth=(username, password))
    if response.status_code == 200:
        pr_json = json.loads(response.text)
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
