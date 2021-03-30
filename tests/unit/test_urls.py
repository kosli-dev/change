from lib.api_schema import ApiSchema

partial_project_data = {
    "owner": "cern",
    "name": "hadroncollider",
}


def test_url_for_pipelines():
    url = ApiSchema.url_for_pipelines(host="http://localhost", project_data=partial_project_data)
    assert url == "http://localhost/api/v1/projects/cern/"


def test_url_for_project():
    url = ApiSchema.url_for_project(host="http://localhost", project_data=partial_project_data)
    assert url == "http://localhost/api/v1/projects/cern/hadroncollider"


def test_url_for_owner_projects():
    url = ApiSchema.url_for_owner_projects(host="http://localhost", project_data=partial_project_data)
    assert url == "http://localhost/api/v1/projects/cern/"
