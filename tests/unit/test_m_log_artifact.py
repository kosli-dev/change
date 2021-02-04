from commands import command_processor, make_command, RequiredEnvVar
from tests.utils import *

# TODO: Test when docker socket not volume-mounted
# TODO: Test when sha256://SHA and SHA does not look like a SHA
# TODO: test_sha256_file() when DISPLAY_NAME is missing
# TODO: test_sha256_file() when supplied DISPLAY_NAME has full path...


def test_file_at_root(capsys):
    commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    protocol = "file://"
    directory = ""
    filename = "jam.jar"
    sha256 = "ccdd89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    ev = log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{directory}{filename}"

    with dry_run(ev) as env, scoped_merkelypipe_json():
        with ScopedFileCopier("/app/tests/data/jam.jar", "/"+filename):
            context = make_context(env)
            context.sha_digest_for_file = lambda _filename: sha256
            status_code = command_processor.execute(context)

    assert status_code == 0
    blurb, method, payload, url = blurb_method_payload_url(full_capsys(capsys))
    assert method == "Putting"
    assert url == "https://test.merkely.com/api/v1/projects/merkely-test/merkely-change-test-pipeline/artifacts/"
    assert payload == {
        'build_url': 'https://gitlab/build/1456',
        'commit_url': f'http://github/me/project/commit/{commit}',
        'description': 'Created by build 23',
        'filename': filename,
        'git_commit': commit,
        'is_compliant': True,
        'sha256': sha256,
    }
    assert blurb == [
        'MERKELY_COMMAND=log_artifact',
        f'Getting SHA for {protocol} artifact: {filename}',
        f"Calculated digest: {sha256}",
        'MERKELY_IS_COMPLIANT: True'
    ]


def test_file_not_at_root(capsys):
    commit = "abc50c8a53f79974d615df335669b59fb56a4444"
    protocol = "file://"
    directory = "app/tests/data"
    filename = "jam.jar"
    sha256 = "ccdd89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f5115"
    ev = log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{directory}/{filename}"

    with dry_run(ev) as env, scoped_merkelypipe_json():
        context = make_context(env)
        context.sha_digest_for_file = lambda _filename: sha256
        status_code = command_processor.execute(context)

    assert status_code == 0
    blurb, method, payload, url = blurb_method_payload_url(full_capsys(capsys))
    assert method == "Putting"
    assert url == "https://test.merkely.com/api/v1/projects/merkely-test/merkely-change-test-pipeline/artifacts/"

    assert payload == {
        'build_url': 'https://gitlab/build/1456',
        'commit_url': f'http://github/me/project/commit/{commit}',
        'description': 'Created by build 23',
        'filename': filename,
        'git_commit': commit,
        'is_compliant': True,
        'sha256': sha256,
    }
    assert blurb == [
        'MERKELY_COMMAND=log_artifact',
        f'Getting SHA for {protocol} artifact: {directory}/{filename}',
        f"Calculated digest: {sha256}",
        'MERKELY_IS_COMPLIANT: True'
    ]


def test_docker_image(capsys):
    commit = "ddc50c8a53f79974d615df335669b59fb56a4ed3"
    digest = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    ev = log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = "docker://acme/road-runner:6.8"

    with dry_run(ev) as env, scoped_merkelypipe_json():
        context = make_context(env)
        context.sha_digest_for_docker_image = lambda _image_name: digest
        status_code = command_processor.execute(context)

    assert status_code == 0
    verify_payload_and_url(capsys)


def test_sha256_file(capsys):
    commit = "ddc50c8a53f79974d615df335669b59fb56a4ed3"
    digest = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    ev = log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"sha256://{digest}"
    ev["MERKELY_DISPLAY_NAME"] = "myjam.jar"

    with dry_run(ev) as env, scoped_merkelypipe_json():
        context = make_context(env)
        status_code = command_processor.execute(context)

    assert status_code == 0
    verify_payload_and_url(capsys)


def test_sha256_docker_image(capsys):
    commit = "ddc50c8a53f79974d615df335669b59fb56a4ed3"
    digest = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    ev = log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"sha256://{digest}"
    ev["MERKELY_DISPLAY_NAME"] = "acme/road-runner:4.8"

    with dry_run(ev) as env, scoped_merkelypipe_json():
        context = make_context(env)
        status_code = command_processor.execute(context)

    assert status_code == 0
    verify_payload_and_url(capsys)


def test_each_required_env_var_missing(capsys):
    for arg in make_command_args():
        if isinstance(arg, RequiredEnvVar):
            ev = log_artifact_env(any_commit())
            ev.pop(arg.name)
            with dry_run(ev) as env, scoped_merkelypipe_json():
                context = make_context(env)
                status_code = command_processor.execute(context)
                assert status_code != 0
    verify_approval(capsys)


def make_command_args():
    env = log_artifact_env(any_commit())
    context = make_context(env)
    return make_command(context).args


def log_artifact_env(commit):
    ev = {
        "MERKELY_FINGERPRINT": "file://jam.jar",
        "MERKELY_CI_BUILD_URL": "https://gitlab/build/1456",
        "MERKELY_CI_BUILD_NUMBER": "23",
        "MERKELY_ARTIFACT_GIT_URL": "http://github/me/project/commit/" + commit,
        "MERKELY_ARTIFACT_GIT_COMMIT": commit,
        "MERKELY_IS_COMPLIANT": "TRUE"
    }
    return {**core_env_vars("log_artifact"), **ev}


def any_commit():
    return "abc50c8a53f79974d615df335669b59fb56a4ed3"

