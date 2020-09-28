from cdb.cdb_utils import url_for_release


def test_url_for_release():
    partial_project_data = {"name": "hadroncollider", "owner": "cern"}
    url = url_for_release(host="http://localhost", project_data=partial_project_data, release_number="12")
    assert url == "http://localhost/api/v1/projects/cern/hadroncollider/releases/12"
