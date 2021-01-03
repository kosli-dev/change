#!/usr/bin/env python
import os

from cdb.api_schema import ApiSchema
from cdb.cdb_utils import parse_cmd_line, load_project_configuration, \
    get_artifacts_for_commit, latest_artifact_for_commit, get_artifact_sha, \
    DEFAULT_REPO_ROOT, build_approval_json, get_host, get_api_token
from cdb.git import commit_for_commitish, list_commits_between, repo_at
from cdb.http import http_post_payload


def create_approval(project_config_file, env):
    env = create_approval_environment_variables(env)
    with open(project_config_file) as json_data_file:
        project_data = load_project_configuration(json_data_file)

        if env["artifact_sha256"] is None:
            src_commit = commit_for_commitish(repo_at(env["repo_path"]), env["target_src_commit"])
            response = get_artifacts_for_commit(env["host"], env["api_token"], project_data, src_commit)
            env["artifact_sha256"] = latest_artifact_for_commit(response)
            print(
                f"Found artifact {env['artifact_sha']} as latest artifact for source commit {env['target_src_commit']}")

        commit_list = list_commits_between(
            repo_at(env["repo_path"]), target_commit=env["target_src_commit"], base_commit=env["base_src_commit"])

        approval_json = build_approval_json(
            artifact_sha256=env["artifact_sha256"],
            description=env["description"],
            is_approved=env["is_externally_approved"],
            src_commit_list=commit_list)

        url = ApiSchema.url_for_approvals(env["host"], project_data)
        http_post_payload(approval_json, url, env["api_token"])


'''
| VARIABLE | Requirement | Description |
|------|-----|-----|
| CDB_HOST | Optional | The host name for ComplianceDB, default is https://app.compliancedb.com |
| CDB_API_TOKEN | Required | Your API token for ComplianceDB |
| CDB_ARTIFACT_SHA or CDB_ARTIFACT_DOCKER_IMAGE | Optional | The SHA256 for the artifact that you would like to approve, if not given then this is retrieved from CDB  |
| CDB_BASE_SRC_COMMITISH | Required | The source commit-ish for the oldest change in the approval |
| CDB_TARGET_SRC_COMMITISH | Required | The source commit-ish for the oldest change in the approval |
| CDB_DESCRIPTION | Optional | A description for the approval |
| CDB_IS_APPROVED_EXTERNALLY | Optional | Use this if the approval has taken place outside compliancedb, default false |
| CDB_SRC_REPO_ROOT | Optional | The path where the source git repository is mounted, default to `/src` |
'''


def create_approval_environment_variables(env=os.environ):
    env = {
        "host": get_host(env),
        "api_token": get_api_token(env),
        "artifact_sha256": get_artifact_sha(env),
        "base_src_commit": env.get('CDB_BASE_SRC_COMMITISH', None),
        "target_src_commit": env.get('CDB_TARGET_SRC_COMMITISH', None),
        "description": env.get('CDB_DESCRIPTION', "No description provided"),
        "is_externally_approved": env.get('CDB_IS_APPROVED_EXTERNALLY', "FALSE") == "TRUE",
        "repo_path": env.get('CDB_SRC_REPO_ROOT', DEFAULT_REPO_ROOT)
    }
    return env


if __name__ == '__main__':
    project_config_file = parse_cmd_line()
    create_approval(project_config_file, env=os.environ)
