from commands import run
from tests.utils import *


def test_file_at_root(capsys):
    commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    sha256 = "ccdd89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    protocol = "file://"
    filename = "jam.jar"
    ev = log_deployment_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{filename}"

    with dry_run(ev) as env, scoped_merkelypipe_json():
        with MockFileFingerprinter(filename, sha256) as fingerprinter:
            run(env, fingerprinter)

    verify_approval(capsys)
    #verify_payload_and_url(capsys)


def test_docker_image(capsys):
    commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    digest = "ccdd89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    protocol = "docker://"
    image_name = "acme/road-runner:6.8"
    ev = log_deployment_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{image_name}"

    with dry_run(ev) as env, scoped_merkelypipe_json():
        with MockImageFingerprinter(image_name, digest) as fingerprinter:
            run(env, fingerprinter)

    verify_approval(capsys)
    #verify_payload_and_url(capsys)


def log_deployment_env(commit):
    ev = {
        "MERKELY_FINGERPRINT": "file://coverage.txt",  # at root
        "MERKELY_CI_BUILD_URL": "https://gitlab/build/1456",
        "MERKELY_ENVIRONMENT": "production",
        "MERKELY_DESCRIPTION": "some description",
        "MERKELY_USER_DATA_FILE": "to do",
    }
    return {**core_env_vars("log_deployment"), **ev}


def any_commit():
    return "ddd50c8a53f79974d615df335669b59fb56a4aaa"

