from cdb.control_junit import control_junit
from commands import main, run, LogTest

from tests.utils import *

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_log_test"

CDB_DOMAIN = "app.compliancedb.com"

USER_DATA = "/app/tests/data/user_data.json"


def test_non_zero_status_when_no_data_directory(capsys, mocker):
    _image_name = "acme/widget:4.67"
    sha256 = "aecdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    build_url = "https://gitlab/build/1457"
    evidence_type = "coverage"
    env = old_control_junit_env()
    set_env_vars = {}
    with dry_run(env, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha256)
        control_junit("tests/integration/test-pipefile.json")

    verify_approval(capsys, ["out"])

     # extract data from approved cdb text file
    import inspect
    this_test = inspect.stack()[0].function
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/{sha256}"
    expected_payload = {
        "contents": {
            "description": "JUnit results xml verified by compliancedb/cdb_controls: All tests passed in 0 test suites",
            "is_compliant": True,
            "url": build_url
        },
        "evidence_type": evidence_type
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload

    # new behaviour is to fail with non-zero exit status
    ev = new_log_test_env()
    ev.pop('MERKELY_USER_DATA')
    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(filename=merkelypipe):
        status = main(env=env)

    assert status != 0
    output = capsys_read(capsys)
    lines = list(output.split("\n"))
    assert lines == [
        'MERKELY_COMMAND=log_test',
        "Error: no directory /data/junit/",
        ''
    ]


def test_zero_exit_status_when_there_is_a_data_directory(capsys, mocker):
    """
    The cdb code looks at CDB_USER_DATA but the line to add
    the json (in cdb_utils.py build_evidence_dict) is this:

    if user_data is not None:
        evidence["user_data"]: user_data

    which should be

    if user_data is not None:
        evidence["user_data"] = user_data

    So that functionality does not exist in the old cdb code.
    """
    image_name = "acme/widget:4.67"
    sha256 = "aecdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    build_url = "https://gitlab/build/1457"
    evidence_type = "coverage"
    env = old_control_junit_env()
    set_env_vars = {}
    with dry_run(env, set_env_vars):
        with ScopedDirCopier('/app/tests/data/control_junit/xml-with-passed-results', '/data/junit'):
            mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha256)
            control_junit("tests/integration/test-pipefile.json")

    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    import inspect
    this_test = inspect.stack()[0].function
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/{sha256}"
    expected_payload = {
        "contents": {
            "description": "JUnit results xml verified by compliancedb/cdb_controls: All tests passed in 2 test suites",
            "is_compliant": True,
            "url": build_url
        },
        "evidence_type": evidence_type
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload

    # make merkely call
    ev = new_log_test_env()
    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(filename=merkelypipe):
        with ScopedDirCopier('/app/tests/data/control_junit/xml-with-passed-results', '/data/junit'):
            with MockDockerFingerprinter(image_name, sha256) as fingerprinter:
                method, url, payload = run(env=env, docker_fingerprinter=fingerprinter)

    capsys_read(capsys)

    # verify matching data
    assert method == expected_method
    assert url == expected_url

    # image name has changed
    string = expected_payload['contents']['description']
    string = string.replace('compliancedb/cdb_controls', 'merkely/change')
    expected_payload['contents']['description'] = string

    # user_data works in new code
    expected_payload["user_data"] = {'status': 'deployed'}

    assert payload == expected_payload


def test_summary_is_not_empty():
    context = {}
    command = LogTest(context)
    assert len(command.summary) > 0


API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"
BUILD_URL = "https://gitlab/build/1457"


def old_control_junit_env():
    image_name = "acme/widget:4.67"
    evidence_type = "coverage"
    return {
        "CDB_ARTIFACT_DOCKER_IMAGE": image_name,
        "CDB_EVIDENCE_TYPE": evidence_type,
        "CDB_CI_BUILD_URL": BUILD_URL,
        "CDB_API_TOKEN": API_TOKEN,
    }


def new_log_test_env():
    protocol = "docker://"
    image_name = "acme/widget:4.67"
    evidence_type = "coverage"
    return {
        "MERKELY_COMMAND": "log_test",
        "MERKELY_FINGERPRINT": f"{protocol}{image_name}",
        "MERKELY_EVIDENCE_TYPE": evidence_type,
        "MERKELY_CI_BUILD_URL": BUILD_URL,
        "MERKELY_USER_DATA": USER_DATA,
        "MERKELY_API_TOKEN": API_TOKEN,
    }

