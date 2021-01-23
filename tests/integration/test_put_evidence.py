from cdb.put_evidence import put_evidence

import docker
from pytest import raises
from tests.utils import AutoEnvVars, CDB_DRY_RUN, verify_approval


def test_message_when_no_env_vars(capsys):
    with AutoEnvVars(CDB_DRY_RUN), raises(docker.errors.DockerException):
        put_evidence("tests/integration/test-pipefile.json")

    verify_approval(capsys, ["out"])


def test_message_when_env_vars_defined(capsys):
    env= {
        "CDB_EVIDENCE_TYPE": "test",
        "CDB_DESCRIPTION": "integration test",
        "CDB_CI_BUILD_URL": "integration test",
        "CDB_IS_COMPLIANT": "TRUE",
    }
    with AutoEnvVars({**CDB_DRY_RUN, **env}), raises(docker.errors.DockerException):
        put_evidence("tests/integration/test-pipefile.json")

    verify_approval(capsys, ["out"])