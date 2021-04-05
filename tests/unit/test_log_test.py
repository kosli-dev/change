from commands import main, run, External
from env_vars import TestResultsDirEnvVar
from tests.utils import *

USER_DATA = "/app/tests/data/user_data.json"

DOMAIN = "app.merkely.com"
OWNER = "acme"
PIPELINE = "road-runner"

IMAGE_NAME = "acme/widget:4.67"
SHA256 = "aecdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"

DEFAULT_TEST_RESULTS_DIR = TestResultsDirEnvVar({}).default


def test_non_zero_status_when_no_data_directory(capsys):
    env = dry_run(log_test_env())
    with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
        external = External(env=env, docker_fingerprinter=fingerprinter)
        status = main(external)

    assert_merkely_error(status, capsys, f"no directory {DEFAULT_TEST_RESULTS_DIR}")


def test_non_zero_status_when_dir_exists_but_has_no_xml_files(capsys):
    empty_dir = "/app/tests/data/"
    env = dry_run(log_test_env())
    env['MERKELY_TEST_RESULTS_DIR'] = empty_dir
    with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
        external = External(env=env, docker_fingerprinter=fingerprinter)
        status = main(external)

    assert_merkely_error(status, capsys, f"No test suites in {empty_dir}")


def test_non_zero_status_when_dir_exists_but_xml_files_are_not_JUnit(capsys):
    dir_name = "/app/tests/data/control_junit/xml_but_not_junit"
    path_name = f"{dir_name}/not_junit.xml"
    env = dry_run(log_test_env())
    env['MERKELY_TEST_RESULTS_DIR'] = dir_name
    with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
        external = External(env=env, docker_fingerprinter=fingerprinter)
        status = main(external)

    assert_merkely_error(status, capsys, f"XML file {path_name} not JUnit format.")


def test_zero_exit_status_when_there_is_a_data_directory(capsys):
    build_url = "https://gitlab/build/1457"
    evidence_type = "coverage"

    expected_method = "PUT"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/artifacts/{SHA256}"
    expected_payload = {
        "contents": {
            "description": "JUnit results xml verified by merkely/change: All tests passed in 2 test suites",
            "is_compliant": True,
            "url": build_url
        },
        "evidence_type": evidence_type,
        "user_data": {
            "status": "deployed"
        }
    }

    env = dry_run(log_test_env())
    with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
        with ScopedDirCopier('/app/tests/data/control_junit/xml_with_passed_results', DEFAULT_TEST_RESULTS_DIR):
            external = External(env=env, docker_fingerprinter=fingerprinter)
            method, url, payload = run(external)

    silence(capsys)

    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload


def test_junit_xml_results_dir_specified_with_env_var(capsys):
    build_url = "https://gitlab/build/1457"
    evidence_type = "coverage"

    expected_method = "PUT"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/artifacts/{SHA256}"
    expected_payload = {
        "contents": {
            "description": "JUnit results xml verified by merkely/change: All tests passed in 2 test suites",
            "is_compliant": True,
            "url": build_url
        },
        "evidence_type": evidence_type,
        "user_data": {
            "status": "deployed"
        }
    }

    env = dry_run(log_test_env())
    env['MERKELY_TEST_RESULTS_DIR'] = "/app/tests/data/control_junit/xml_with_passed_results"
    with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
        external = External(env=env, docker_fingerprinter=fingerprinter)
        method, url, payload = run(external)

    silence(capsys)

    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload


def test_junit_xml_with_error_results_dir_specified_with_env_var(capsys):
    build_url = "https://gitlab/build/1457"
    evidence_type = "coverage"

    expected_method = "PUT"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/artifacts/{SHA256}"
    expected_payload = {
        "contents": {
            "description": "JUnit results xml verified by merkely/change: Tests contain errors",
            "is_compliant": False,
            "url": build_url
        },
        "evidence_type": evidence_type,
        "user_data": {
            "status": "deployed"
        }
    }

    env = dry_run(log_test_env())
    env['MERKELY_TEST_RESULTS_DIR'] = "/app/tests/data/control_junit/xml_with_error"
    with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
        external = External(env=env, docker_fingerprinter=fingerprinter)
        method, url, payload = run(external)

    silence(capsys)

    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload


def assert_merkely_error(status, capsys, expected):
    assert status != 0
    stdout = capsys_read(capsys)
    lines = list(stdout.split("\n"))
    assert lines == [
        'MERKELY_COMMAND=log_test',
       f"Error: {expected}",
        ''
    ]

API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"
BUILD_URL = "https://gitlab/build/1457"
IMAGE_NAME = "acme/widget:4.67"
EVIDENCE_TYPE = "coverage"


def log_test_env():
    protocol = "docker://"
    return {
        "MERKELY_COMMAND": "log_test",
        "MERKELY_OWNER": OWNER,
        "MERKELY_PIPELINE": PIPELINE,
        "MERKELY_FINGERPRINT": f"{protocol}{IMAGE_NAME}",
        "MERKELY_EVIDENCE_TYPE": EVIDENCE_TYPE,
        "MERKELY_CI_BUILD_URL": BUILD_URL,
        "MERKELY_USER_DATA": USER_DATA,
        "MERKELY_API_TOKEN": API_TOKEN,
    }
