from cdb.put_evidence import put_evidence

from commands import command_processor, make_command

from tests.utils import *

MERKELY_DOMAIN = "test.compliancedb.com"
CDB_DOMAIN = "app.compliancedb.com"

CDB_OWNER = "compliancedb"
CDB_NAME = "cdb-controls-test-pipeline"

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_log_artifact"

API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"


def test_docker_protocol(capsys, mocker):
    # integration/test_put_evidence.py
    # def test_required_env_vars_uses_CDB_ARTIFACT_DOCKER_IMAGE(capsys, mocker):
    build_url = "https://gitlab/build/1956"
    sha256 = "bbcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    image_name = "acme/widget:4.67"

    cdb_env = {
        "CDB_API_TOKEN": API_TOKEN,
        "CDB_ARTIFACT_DOCKER_IMAGE": image_name,
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_EVIDENCE_TYPE": "unit_test",
        "CDB_DESCRIPTION": "branch coverage",
        "CDB_CI_BUILD_URL": build_url,
    }

    with dry_run(cdb_env):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha256)
        put_evidence("tests/integration/test-pipefile.json")

    verify_approval(capsys, ["out"])





def make_command_args():
    env = new_log_evidence_env()
    context = make_context(env)
    return make_command(context).args


def old_put_evidence_env(commit, *,
                         build_url):
    return {
        "CDB_API_TOKEN": API_TOKEN,
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_CI_BUILD_URL": build_url
    }


def new_log_evidence_env(commit=None, *,
                         domain=None,
                         build_url=None):
    if commit is None:
        commit = any_commit()
    if domain is None:
        domain = "app.compliancedb.com"
    if build_url is None:
        build_url = 'https://gitlab/build/1456'
    return {
        "MERKELY_COMMAND": "log_evidence",
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{domain}",
        "MERKELY_CI_BUILD_URL": build_url,
        "MERKELY_IS_COMPLIANT": "TRUE"
    }


def any_commit():
    return "abc50c8a53f79974d615df335669b59fb56a4ed3"

