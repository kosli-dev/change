import os

from cdb.cdb_utils import load_user_data
from cdb.put_artifact_image import put_artifact_image

# def test_put_dry_run_doesnt_call(mocker):
#     requests = mocker.patch('cdb.http.req')
#     os.environ["CDB_DRY_RUN"] = "TRUE"
#     put_payload({}, "https://www.example.com", "")
#     requests.put.assert_not_called()


def test_load_user_data_None_if_not_in_env(mocker):
    if os.getenv('CDB_USER_DATA'):
        del os.environ['CDB_USER_DATA']
    user_data = load_user_data()
    assert user_data is None


def test_load_user_data_returns_object_from_file(mocker):
    mock_json = mocker.patch('cdb.cdb_utils.json')
    mock_json.load.return_value = {"super_cool": "user data"}
    os.environ['CDB_USER_DATA'] = "/some/random/file.json"

    user_data = load_user_data()

    assert user_data == {"super_cool": "user data"}
    mock_json.load.assert_called_once_with("/some/random/file.json")


# def test_put_artifact_image():
#     put_artifact_image("test-pipeline.json")

