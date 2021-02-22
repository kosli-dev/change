#!/usr/bin/env python
import os

from cdb.api_schema import ApiSchema
from cdb.cdb_utils import parse_cmd_line, load_project_configuration, \
    get_artifacts_for_commit, latest_artifact_for_commit, build_release_json, get_host, get_artifact_sha, get_api_token, \
    DEFAULT_REPO_ROOT
from cdb.git import commit_for_commitish, list_commits_between, repo_at
from cdb.http import http_post_payload


def create_release(project_config_file):
    env = create_release_environment_variables()
    with open(project_config_file) as json_data_file:
        project_data = load_project_configuration(json_data_file)

        if env["artifact_sha"] is None:
            src_commit = commit_for_commitish(repo_at(env["repo_path"]), env["target_src_commit"])
            response = get_artifacts_for_commit(env["host"], env["api_token"], project_data, src_commit)
            env["artifact_sha"] = latest_artifact_for_commit(response)
            print(
                f"Found artifact {env['artifact_sha']} as latest artifact for source commit {env['target_src_commit']}")

        commit_list = list_commits_between(repo_at(env["repo_path"]), env["target_src_commit"], env["base_src_commit"])
        release_json = build_release_json(env["artifact_sha"], env["description"], commit_list)
        url = ApiSchema.url_for_releases(env["host"], project_data)
        http_post_payload(url, release_json, env["api_token"])


def create_release_environment_variables():
    env = {
        "host": get_host(),
        "base_src_commit": os.getenv('CDB_BASE_SRC_COMMITISH', None),
        "target_src_commit": os.getenv('CDB_TARGET_SRC_COMMITISH', None),
        "artifact_sha": get_artifact_sha(),
        "api_token": get_api_token(),
        "description": os.getenv('CDB_RELEASE_DESCRIPTION', "No description provided"),
        "repo_path": os.getenv('CDB_SRC_REPO_ROOT', DEFAULT_REPO_ROOT)
    }
    return env


if __name__ == '__main__':
    project_config_file = parse_cmd_line()
    create_release(project_config_file)
