from commands import run, External

from tests.utils import *

DOMAIN = "app.merkely.com"
OWNER = "acme"
PIPELINE = "lib-controls-test-pipeline"


def test_fingerprint_is_echoed_to_stdout():
    sha256 = "ddcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ee"
    commit = "12037940e4e7503055d8a8eea87e177f04f14616"
    image_name = "acme/widget:3.4"
    build_url = "https://gitlab/build/1456"
    build_number = "23"

    expected_method = None
    expected_url = None
    expected_payload = None

    protocol = "docker://"
    env = dry_run(echo_fingerprint_env(commit))
    env["MERKELY_FINGERPRINT"] = f"{protocol}{image_name}"
    with MockDockerFingerprinter(image_name, sha256) as fingerprinter:
        external = External(env=env, docker_fingerprinter=fingerprinter)
        method, url, payload = run(external)

    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    stdout = external.stdout.getvalue()
    assert stdout == sha256 + '\n'


def echo_fingerprint_env(commit):
    return {
        "MERKELY_COMMAND": "echo_fingerprint",
        "MERKELY_FINGERPRINT": 'docker://acme/road-runner:2.3',
    }