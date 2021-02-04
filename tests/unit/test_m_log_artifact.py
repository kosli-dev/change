from commands import command_processor, make_command, RequiredEnvVar
from tests.utils import *

# TODO: Test when docker socket not volume-mounted
# TODO: Test when sha256://SHA and SHA does not look like a SHA
# TODO: test_sha256_file() when DISPLAY_NAME is missing
# TODO: test_sha256_file() when supplied DISPLAY_NAME has full path...
# TODO: test when FINGERPRINT protocol is unknown

MERKELY_DOMAIN = "test.compliancedb.com"
CDB_DOMAIN = "app.compliancedb.com"

CDB_OWNER = "compliancedb"

CDB_NAME = "cdb-controls-test-pipeline"


def test_file_at_root(capsys):
    commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    protocol = "file://"
    directory = ""
    filename = "jam.jar"
    sha256 = "ddcdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee"
    domain = CDB_DOMAIN
    owner = CDB_OWNER
    name = CDB_NAME
    build_url_number = '1456'
    build_number = '349'
    ev = log_artifact_env(commit, domain, build_url_number, build_number)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{directory}{filename}"

    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        with ScopedFileCopier("/app/tests/data/jam.jar", "/"+filename):
            context = make_context(env)
            context.sha_digest_for_file = lambda _filename: sha256
            status_code = command_processor.execute(context)

    blurb, method, payload, url = blurb_method_payload_url(full_capsys(capsys))
    assert status_code == 0
    assert method == "Putting"
    assert url == f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    assert payload == {
        'build_url': f'https://gitlab/build/{build_url_number}',
        'commit_url': f'http://github/me/project/commit/{commit}',
        'description': f'Created by build {build_number}',
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
    assert old_url == url
    assert old_payload == payload


def test_file_not_at_root(capsys):
    commit = "abc50c8a53f79974d615df335669b59fb56a4444"
    sha256 = "ccdd89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f5115"
    protocol = "file://"
    directory = "app/tests/data"
    filename = "jam.jar"
    domain = CDB_DOMAIN
    owner = CDB_OWNER
    name = CDB_NAME
    ev = log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{directory}/{filename}"

    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        context = make_context(env)
        context.sha_digest_for_file = lambda _filename: sha256
        status_code = command_processor.execute(context)

    blurb, method, payload, url = blurb_method_payload_url(full_capsys(capsys))
    assert status_code == 0
    assert method == "Putting"
    assert url == f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    assert payload == {
        'build_url': 'https://gitlab/build/1456',
        'commit_url': f'http://github/me/project/commit/{commit}',
        'description': 'Created by build 23',
        'filename': filename, # <<<<<< does _not_ contain directory
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
    domain = CDB_DOMAIN
    owner = CDB_OWNER
    name = CDB_NAME
    ev = log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{image_name}"

    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        context = make_context(env)
        context.sha_digest_for_docker_image = lambda _image_name: sha256
        status_code = command_processor.execute(context)

    blurb, method, payload, url = blurb_method_payload_url(full_capsys(capsys))
    assert status_code == 0
    assert method == "Putting"
    assert url == f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
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
    commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    sha256 = "444daef69c676c2466571d3211180d559ccc2032b258fc5e73f99a103db462ef"
    protocol = "sha256://"
    filename = "door-is-a.jar"
    domain = MERKELY_DOMAIN
    owner = CDB_OWNER
    name = CDB_NAME
    build_url_number = '2156'
    build_number = '751'
    ev = log_artifact_env(commit, domain, build_url_number, build_number)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{sha256}"
    ev["MERKELY_DISPLAY_NAME"] = filename

    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        context = make_context(env)
        status_code = command_processor.execute(context)

    blurb, method, payload, url = blurb_method_payload_url(full_capsys(capsys))
    assert status_code == 0
    assert method == "Putting"
    assert url == f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    assert payload == {
        'build_url': f'https://gitlab/build/{build_url_number}',
        'commit_url': f'http://github/me/project/commit/{commit}',
        'description': f'Created by build {build_number}',
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
    old_dir = "tests/integration/approved_executions"
    old_file = "test_put_artifact"
    old_test = "test_all_env_vars_uses_FILENAME_and_SHA"
    approved = f"{old_dir}/{old_file}.{old_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = blurb_method_payload_url(old_approval)
    assert old_method == method
    assert old_url == url
    assert old_payload == payload


def test_sha256_docker_image(capsys):
    commit = "ddc50c8a53f79974d615df335669b59fb56a4ed3"
    sha256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    protocol = "sha256://"
    image_name = "acme/road-runner:4.8"
    domain = CDB_DOMAIN
    owner = CDB_OWNER
    name = CDB_NAME
    ev = log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{sha256}"
    ev["MERKELY_DISPLAY_NAME"] = image_name

    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        context = make_context(env)
        status_code = command_processor.execute(context)

    blurb, method, payload, url = blurb_method_payload_url(full_capsys(capsys))
    assert status_code == 0
    assert method == "Putting"
    assert url == f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
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


def log_artifact_env(commit, domain=None, build_url_number=None, build_number=None):
    if domain is None:
        domain = "app.compliancedb.com"
    if build_url_number is None:
        build_url_number = '1456'
    if build_number is None:
        build_number = '23'
    return {
        "MERKELY_COMMAND": "log_artifact",
        "MERKELY_API_TOKEN": "MY_SUPER_SECRET_API_TOKEN",
        "MERKELY_HOST": f"https://{domain}",
        "MERKELY_FINGERPRINT": "file://jam.jar",
        "MERKELY_CI_BUILD_URL": f"https://gitlab/build/{build_url_number}",
        "MERKELY_CI_BUILD_NUMBER": build_number,
        "MERKELY_ARTIFACT_GIT_URL": "http://github/me/project/commit/" + commit,
        "MERKELY_ARTIFACT_GIT_COMMIT": commit,
        "MERKELY_IS_COMPLIANT": "TRUE"
    }


def any_commit():
    return "abc50c8a53f79974d615df335669b59fb56a4ed3"
