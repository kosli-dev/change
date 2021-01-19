#!/usr/bin/env python
import os
from cdb.api_schema import ApiSchema
from cdb.cdb_utils import parse_cmd_line, load_project_configuration
from cdb.http import http_put_payload
from cdb.settings import CDB_SERVER
from cdb.http_retry import HttpRetryError


def main():
    """
    project.json
    """
    try:
        project_file = parse_cmd_line()
        put_pipeline(project_file)
    except HttpRetryError:
        pass


def put_pipeline(project_file, env=os.environ):
    print("Ensure Project - loading " + project_file)
    with open(project_file) as json_data_file:
        project_data = load_project_configuration(json_data_file)

        host = env.get('CDB_HOST', CDB_SERVER)
        projects_url = ApiSchema.url_for_owner_projects(host, project_data)

        api_token = env.get('CDB_API_TOKEN', 'NO_API_TOKEN_DEFINED')

        print("Put pipeline")
        create_response = http_put_payload(url=projects_url, payload=project_data, api_token=api_token)


if __name__ == '__main__':
    main()
