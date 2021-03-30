from lib.api_schema import ApiSchema

partial_project_data = {"name": "hadroncollider", "owner": "cern"}


def test_url_for_releases():
    url = ApiSchema.url_for_releases(host="http://localhost", project_data=partial_project_data)
    assert url == "http://localhost/api/v1/projects/cern/hadroncollider/releases/"


def test_url_for_commit():
    url = ApiSchema.url_for_commit(host="http://localhost", project_data=partial_project_data, commit="12345678")
    assert url == "http://localhost/api/v1/projects/cern/hadroncollider/commits/12345678"


def test_url_for_release():
    url = ApiSchema.url_for_release(host="http://localhost", project_data=partial_project_data, release_number="12")
    assert url == "http://localhost/api/v1/projects/cern/hadroncollider/releases/12"
