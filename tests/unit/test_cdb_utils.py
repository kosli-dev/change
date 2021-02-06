import os
from cdb.cdb_utils import load_user_data
from tests.utils import ScopedEnvVars


def test_load_user_data_None_if_not_in_env(mocker):
    with ScopedEnvVars({}):
        assert not os.getenv('CDB_USER_DATA')
        user_data = load_user_data()
        assert user_data is None


def test_load_user_data_returns_object_from_file(mocker, fs):
    set_env_vars = {'CDB_USER_DATA': '/some/random/file.json'}
    with ScopedEnvVars({}, set_env_vars):
        os.environ['CDB_USER_DATA'] = "/some/random/file.json"
        fs.create_file("/some/random/file.json", contents='{"super_cool": "user data"}')
        user_data = load_user_data()
        assert user_data == {"super_cool": "user data"}


