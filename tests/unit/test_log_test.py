from commands import main, run, External

from tests.utils import *

USER_DATA = "/app/tests/data/user_data.json"

DOMAIN = "app.merkely.com"
OWNER = "acme"
PIPELINE = "lib-controls-test-pipeline"

IMAGE_NAME = "acme/widget:4.67"
SHA256 = "aecdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"


def test_non_zero_status_when_no_data_directory(capsys):
    ev = log_test_env()
    with dry_run(ev) as env:
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            external = External(env=env, docker_fingerprinter=fingerprinter)
            status = main(external)

    assert status != 0
    output = capsys_read(capsys)
    lines = list(output.split("\n"))
    assert lines == [
        'MERKELY_COMMAND=log_test',
        "Error: no directory /data/junit/",
        ''
    ]


def test_non_zero_status_when_dir_exists_but_has_no_xml_files(capsys):
    ev = log_test_env()
    ev['MERKELY_TEST_RESULTS_DIR'] = "/app/tests/data/"
    with dry_run(ev) as env:
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            external = External(env=env, docker_fingerprinter=fingerprinter)
            status = main(external)

    assert status != 0
    output = capsys_read(capsys)
    lines = list(output.split("\n"))
    assert lines == [
        'MERKELY_COMMAND=log_test',
        "Error: No test suites in /app/tests/data/",
        ''
    ]


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

    ev = log_test_env()
    with dry_run(ev) as env:
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            with ScopedDirCopier('/app/tests/data/control_junit/xml_with_passed_results', '/data/junit'):
                external = External(env=env, docker_fingerprinter=fingerprinter)
                method, url, payload = run(external)

    capsys_read(capsys)  # keeping stdout silent

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

    ev = log_test_env()
    ev['MERKELY_TEST_RESULTS_DIR'] = "/app/tests/data/control_junit/xml_with_passed_results"
    with dry_run(ev) as env:
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            external = External(env=env, docker_fingerprinter=fingerprinter)
            method, url, payload = run(external)

    capsys_read(capsys)

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

    ev = log_test_env()
    ev['MERKELY_TEST_RESULTS_DIR'] = "/app/tests/data/control_junit/xml_with_error"
    with dry_run(ev) as env:
        with MockDockerFingerprinter(IMAGE_NAME, SHA256) as fingerprinter:
            external = External(env=env, docker_fingerprinter=fingerprinter)
            method, url, payload = run(external)

    capsys_read(capsys)

    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload


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
