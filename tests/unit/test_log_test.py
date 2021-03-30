from commands import main, run, External

from tests.utils import *

USER_DATA = "/app/tests/data/user_data.json"

DOMAIN = "app.merkely.com"
OWNER = "compliancedb"
PIPELINE = "lib-controls-test-pipeline"


def test_non_zero_status_when_no_data_directory(capsys):
    ev = new_log_test_env()
    with dry_run(ev) as env:
        status = main(External(env=env))

    assert status != 0
    output = capsys_read(capsys)
    lines = list(output.split("\n"))
    assert lines == [
        'MERKELY_COMMAND=log_test',
        "Error: no directory /data/junit/",
        ''
    ]


def test_zero_exit_status_when_there_is_a_data_directory(capsys):
    image_name = "acme/widget:4.67"
    sha256 = "aecdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    build_url = "https://gitlab/build/1457"
    evidence_type = "coverage"

    expected_method = "PUT"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/artifacts/{sha256}"
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

    # make merkely call
    ev = new_log_test_env()
    with dry_run(ev) as env:
        with MockDockerFingerprinter(image_name, sha256) as fingerprinter:
            with ScopedDirCopier('/app/tests/data/control_junit/xml_with_passed_results', '/data/junit'):
                external = External(env=env, docker_fingerprinter=fingerprinter)
                method, url, payload = run(external)

    capsys_read(capsys)  # keeping stdout silent

    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload


def test_junit_xml_results_dir_specified_with_env_var(capsys):
    image_name = "acme/widget:4.67"
    sha256 = "aecdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ef"
    build_url = "https://gitlab/build/1457"
    evidence_type = "coverage"

    expected_method = "PUT"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/artifacts/{sha256}"
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

    # make merkely call
    ev = new_log_test_env()
    ev['MERKELY_TEST_RESULTS_DIR'] = "/app/tests/data/control_junit/xml_with_passed_results"
    with dry_run(ev) as env:
        with MockDockerFingerprinter(image_name, sha256) as fingerprinter:
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


def new_log_test_env():
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

