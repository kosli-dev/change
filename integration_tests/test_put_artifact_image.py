import pytest
from cdb.put_artifact_image import put_artifact_image

from tests.utils import AutoEnvVars, cdb_dry_run, verify_approval


@pytest.mark.skip(reason="pending while investigating env-vars state being set in other tests")
def test_message_when_no_env_vars(capsys):
    with cdb_dry_run(), AutoEnvVars():
        put_artifact_image("integration_tests/test-pipefile.json")

    verify_approval(capsys, ["out"])