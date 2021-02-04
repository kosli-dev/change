from commands import command_processor, make_command, RequiredEnvVar
from tests.utils import *

# TODO: Test when docker socket not volume-mounted
# TODO: Test when sha256://SHA and SHA does not look like a SHA
# TODO: test_sha256_file() when DISPLAY_NAME is missing
# TODO: test_sha256_file() when supplied DISPLAY_NAME has full path...
# TODO: test when FINGERPRINT protocol is unknown

DOMAIN = "app.compliancedb.com"
OWNER = "merkely-test"
NAME = "merkely-change-test-pipeline"

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

    blurb, method, payload, url = blurb_method_payload_url(full_capsys(capsys))
    assert status_code == 0
    assert method == "Putting"
    assert url == f"https://{DOMAIN}/api/v1/projects/{OWNER}/{NAME}/artifacts/"
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

    old_dir = "tests/integration/approved_executions"
    old_file = "test_put_artifact"
    old_test = "test_required_env_vars_uses_CDB_ARTIFACT_FILENAME"
    approved = f"{old_dir}/{old_file}.{old_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = blurb_method_payload_url(old_approval)
    assert old_method == method
    #assert old_url == url





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

    blurb, method, payload, url = blurb_method_payload_url(full_capsys(capsys))
    assert status_code == 0
    assert method == "Putting"
    assert url == f"https://{DOMAIN}/api/v1/projects/{OWNER}/{NAME}/artifacts/"
    assert payload == {
        'build_url': 'https://gitlab/build/1456',
        'commit_url': f'http://github/me/project/commit/{commit}',
        'description': 'Created by build 23',
        'filename': filename, # <<<<<< does not contain directory
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
    sha256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    protocol = "docker://"
    image_name = "acme/road-runner:6.8"
    ev = log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{image_name}"

    with dry_run(ev) as env, scoped_merkelypipe_json():
        context = make_context(env)
        context.sha_digest_for_docker_image = lambda _image_name: sha256
        status_code = command_processor.execute(context)

    blurb, method, payload, url = blurb_method_payload_url(full_capsys(capsys))
    assert status_code == 0
    assert method == "Putting"
    assert url == f"https://{DOMAIN}/api/v1/projects/{OWNER}/{NAME}/artifacts/"
    assert payload == {
        'build_url': 'https://gitlab/build/1456',
        'commit_url': f'http://github/me/project/commit/{commit}',
        'description': 'Created by build 23',
        'filename': image_name,
        'git_commit': commit,
        'is_compliant': True,
        'sha256': sha256,
    }
    assert blurb == [
        'MERKELY_COMMAND=log_artifact',
        f'Getting SHA for {protocol} artifact: {image_name}',
        f"Calculated digest: {sha256}",
        'MERKELY_IS_COMPLIANT: True'
    ]


def test_sha256_file(capsys):
    commit = "ddc50c8a53f79974d615df335669b59fb56a4ed3"
    sha256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    protocol = "sha256://"
    filename = "door-is-a.jar"
    ev = log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{sha256}"
    ev["MERKELY_DISPLAY_NAME"] = filename

    with dry_run(ev) as env, scoped_merkelypipe_json():
        context = make_context(env)
        status_code = command_processor.execute(context)

    blurb, method, payload, url = blurb_method_payload_url(full_capsys(capsys))
    assert status_code == 0
    assert method == "Putting"
    assert url == f"https://{DOMAIN}/api/v1/projects/{OWNER}/{NAME}/artifacts/"
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
        #f'Getting SHA for {protocol} artifact: {filename}',
        #f"Calculated digest: {sha256}",
        'MERKELY_IS_COMPLIANT: True'
    ]


def test_sha256_docker_image(capsys):
    commit = "ddc50c8a53f79974d615df335669b59fb56a4ed3"
    sha256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    protocol = "sha256://"
    image_name = "acme/road-runner:4.8"
    ev = log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{sha256}"
    ev["MERKELY_DISPLAY_NAME"] = image_name

    with dry_run(ev) as env, scoped_merkelypipe_json():
        context = make_context(env)
        status_code = command_processor.execute(context)

    blurb, method, payload, url = blurb_method_payload_url(full_capsys(capsys))
    assert status_code == 0
    assert method == "Putting"
    assert url == f"https://{DOMAIN}/api/v1/projects/{OWNER}/{NAME}/artifacts/"
    assert payload == {
        'build_url': 'https://gitlab/build/1456',
        'commit_url': f'http://github/me/project/commit/{commit}',
        'description': 'Created by build 23',
        'filename': image_name,
        'git_commit': commit,
        'is_compliant': True,
        'sha256': sha256,
    }
    assert blurb == [
        'MERKELY_COMMAND=log_artifact',
        #f'Getting SHA for {protocol} artifact: {filename}',
        #f"Calculated digest: {sha256}",
        'MERKELY_IS_COMPLIANT: True'
    ]


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

