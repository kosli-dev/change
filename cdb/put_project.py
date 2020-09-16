#!/usr/bin/env python
import os
import requests as req
from requests.auth import HTTPBasicAuth
from cdb.cdb_utils import parse_cmd_line, load_project_configuration, url_for_owner_projects
from cdb.settings import CDB_SERVER


def main():
    """
    project.json
    """
    project_file = parse_cmd_line()

    print("Ensure Project - loading " + project_file)
    with open(project_file) as json_data_file:
        project_data = load_project_configuration(json_data_file)

        host = os.getenv('CDB_HOST', CDB_SERVER)
        projects_url = url_for_owner_projects(host, project_data)

        api_token = os.getenv('CDB_API_TOKEN', 'NO_API_TOKEN_DEFINED')

        print("PUT: " + projects_url)
        print("PAYLOAD: " + str(project_data))

        print("Create project")
        create_response = req.put(projects_url, json=project_data, auth=HTTPBasicAuth(api_token, 'unused'))
        print(create_response.text)


if __name__ == '__main__':
    main()
