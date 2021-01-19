import os
import pytest
from cdb.put_artifact_image import put_artifact_image

from tests.utils import AutoEnvVars, cdb_dry_run, verify_approval


@pytest.mark.skip(reason="investigating env-vars being set in other tests")
def test_message_when_no_env_vars(): #capsys):

    print("X"*60)
    for name,value in os.environ.items():
        print(name+"="+value)
    print("X"*60)

    with cdb_dry_run():
        put_artifact_image("integration_tests/test-pipefile.json")

    verify_approval(capsys, ["out"])