from commands import command_processor
from tests.utils import *

# def test_file_not_at_root(capsys):


def test_file_at_root(capsys):
    commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    digest = "ccdd89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    ev = log_deployment_env(commit)
    ev["MERKELY_FINGERPRINT"] = "file://jam.jar"

    with dry_run(ev) as env, scoped_merkelypipe_json():
        with ScopedFileCopier("/app/tests/data/jam.jar", "/jam.jar"):
            context = make_context(env)
            context.sha_digest_for_file = lambda _filename: digest
            command_processor.execute(context)

    verify_approval(capsys)
    #verify_payload_and_url(capsys)


def test_docker_image(capsys):
    commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    digest = "ccdd89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    ev = log_deployment_env(commit)
    ev["MERKELY_FINGERPRINT"] = "docker://acme/road-runner:6.8"

    with dry_run(ev) as env, scoped_merkelypipe_json():
        with ScopedFileCopier("/app/tests/data/coverage.txt", "/jam.jar"):
            context = make_context(env)
            context.sha_digest_for_docker_image = lambda _filename: digest
            command_processor.execute(context)

    verify_approval(capsys)
    #verify_payload_and_url(capsys)

#def test_sha256_file(capsys):
#def test_sha256_docker_image(capsys):

#def test_MERKELY_CI_BUILD_URL_missing(capsys):
#def test_MERKELY_FINGERPRINT_missing(capsys):


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

