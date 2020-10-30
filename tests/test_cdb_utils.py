import os

from cdb.cdb_utils import load_user_data


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


