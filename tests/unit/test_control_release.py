from cdb.api_schema import ApiSchema


def test_url_for_release():
    partial_project_data = {"name": "hadroncollider", "owner": "cern"}
    url = ApiSchema.url_for_release(host="http://localhost", project_data=partial_project_data, release_number="12")
    assert url == "http://localhost/api/v1/projects/cern/hadroncollider/releases/12"
