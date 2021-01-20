from cdb.put_evidence import put_evidence

import docker
from pytest import raises
from tests.utils import AutoEnvVars, cdb_dry_run


def test_message_when_no_env_vars():
    with cdb_dry_run(), AutoEnvVars(), raises(docker.errors.DockerException):
        put_evidence("tests/integration/test-pipefile.json")
