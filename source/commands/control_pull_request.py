import json
import requests

from commands import Command
from errors import ChangeError
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class ControlPullRequest(Command):

    def summary(self, _ci):
        return ""

    def volume_mounts(self, ci):
        if ci == 'bitbucket':
            return []
        else:
            return ["/var/run/docker.sock:/var/run/docker.sock"]

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
        if not is_compliant:
            raise ChangeError(f"Artifact with sha {self.fingerprint.sha} is not compliant")
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
    def _merkely_env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'ci_build_url',
            'description',
            'evidence_type',
            'api_token',
            'owner',
            'pipeline',
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
    response = requests.get(url, auth=(username, password))
    if response.status_code == 200:
        is_compliant = parse_response(commit, password, pull_requests_evidence, response, username)
    elif response.status_code == 202:
        message = "Repository pull requests are still being indexed, please retry."
        raise ChangeError(message)
    elif response.status_code == 404:
        message = " ".join([
            "Repository does not exists or pull requests are not indexed.",
            "Please make sure Pull Request Commit Links app is installed"
        ])
        raise ChangeError(message)
    else:
        message = " ".join([
            "Exception occurred in fetching pull requests.",
            f"Http return code is {response.status_code}"
        ])
        message += f"\n    {response.text}"
        raise ChangeError(message)

    return is_compliant, pull_requests_evidence


def parse_response(commit, password, pull_requests_evidence, response, username):
    print("Pull requests response: " + response.text)
    pull_requests_json = json.loads(response.text)
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


"""
Notes for implementation on Github Actions
https://docs.github.com/en/rest/reference/pulls#list-pull-requests
GET /repos/{owner}/{repo}/pulls/{pull_number}/commits
This needs the pull_number. Also, this is limited to 100.
See https://github.com/actions/checkout/issues/58
Uses the env-var $GITHUB_EVENT_PATH
Eg:
    const fs = require('fs')
    const ev = JSON.parse(
      fs.readFileSync(process.env.GITHUB_EVENT_PATH, 'utf8')
    )
    const prNum = ev.pull_request.number 

This could be awkward. The information in the file $GITHUB_EVENT_PATH
needs to get inside the merkely/change container somehow. volume-mounting is
problematic (in general as some CI's don't allow it).
Or do it CI itself and create an env-var. Maybe will require some jq.
Look into using pygit with David? 
Will also need (username,password)
"""