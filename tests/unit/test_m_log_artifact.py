from cdb.put_artifact import put_artifact
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

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_log_artifact"

API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"


def test_file_at_root(capsys, mocker):
    # Data
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

    # make cdb call
    old_env = old_put_artifact_env(commit,
                                   build_url_number=build_url_number,
                                   build_number=build_number)
    old_env["CDB_ARTIFACT_FILENAME"] = filename
    set_env_vars = {'CDB_ARTIFACT_SHA': sha256}
    with ScopedEnvVars({**CDB_DRY_RUN, **old_env}, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_file', return_value=sha256)
        put_artifact("tests/integration/test-pipefile.json")

    # compare with approved cdb text file
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_file_at_root"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = blurb_method_payload_url(old_approval)

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    expected_payload = {
        'build_url': f'https://gitlab/build/{build_url_number}',
        'commit_url': f'https://github/me/project/commit/{commit}',
        'description': f'Created by build {build_number}',
        'filename': filename,
        'git_commit': commit,
        'is_compliant': True,
        'sha256': sha256,
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload

    # make merkely call
    ev = new_log_artifact_env(commit,
                              domain=domain,
                              build_url_number=build_url_number,
                              build_number=build_number)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{directory}{filename}"
    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        with ScopedFileCopier("/app/tests/data/jam.jar", "/"+filename):
            context = make_context(env)
            context.sha_digest_for_file = lambda _filename: sha256
            method, url, payload = command_processor.execute(context)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    assert blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_artifact',
        f'Getting SHA for {protocol} artifact: {filename}',
        f"Calculated digest: {sha256}",
        'MERKELY_IS_COMPLIANT: True'
    ]


def test_file_not_at_root(capsys):
    commit = "abc50c8a53f79974d615df335669b59fb56a4444"
    sha256 = "ccdd89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f5115"
    protocol = "file://"
    directory = "app/tests/data"
    filename = "jam.jar"
    domain = CDB_DOMAIN
    owner = CDB_OWNER
    name = CDB_NAME
    ev = new_log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{directory}/{filename}"

    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        context = make_context(env)
        context.sha_digest_for_file = lambda _filename: sha256
        method, url, payload = command_processor.execute(context)

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    expected_payload = {
        'build_url': 'https://gitlab/build/1456',
        'commit_url': f'https://github/me/project/commit/{commit}',
        'description': 'Created by build 23',
        'filename': filename, # <<<<<< does _not_ contain directory
        'git_commit': commit,
        'is_compliant': True,
        'sha256': sha256,
    }

    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    assert blurb(capsys_read(capsys)) == [
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
    ev = new_log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{image_name}"

    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        context = make_context(env)
        context.sha_digest_for_docker_image = lambda _image_name: sha256
        method, url, payload = command_processor.execute(context)

    assert method == "Putting"
    assert url == f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    assert payload == {
        'build_url': 'https://gitlab/build/1456',
        'commit_url': f'https://github/me/project/commit/{commit}',
        'description': 'Created by build 23',
        'filename': image_name,
        'git_commit': commit,
        'is_compliant': True,
        'sha256': sha256,
    }
    assert blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_artifact',
        f'Getting SHA for {protocol} artifact: {image_name}',
        f"Calculated digest: {sha256}",
        'MERKELY_IS_COMPLIANT: True'
    ]


def test_sha256_file(capsys):
    commit = "abc50c8a53f79974d615df335669b59fb56a4ed4"
    sha256 = "444daef69c676c2466571d3211180d559ccc2032b258fc5e73f99a103db462ef"
    protocol = "sha256://"
    filename = "door-is-a.jar"
    domain = MERKELY_DOMAIN
    owner = CDB_OWNER
    name = CDB_NAME
    build_url_number = '2156'
    build_number = '751'
    ev = new_log_artifact_env(commit,
                              domain=domain,
                              build_url_number=build_url_number,
                              build_number=build_number)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{sha256}"
    ev["MERKELY_DISPLAY_NAME"] = filename

    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        context = make_context(env)
        method, url, payload = command_processor.execute(context)

    assert method == "Putting"
    assert url == f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    assert payload == {
        'build_url': f'https://gitlab/build/{build_url_number}',
        'commit_url': f'https://github/me/project/commit/{commit}',
        'description': f'Created by build {build_number}',
        'filename': filename,
        'git_commit': commit,
        'is_compliant': True,
        'sha256': sha256,
    }
    assert blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_artifact',
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
    ev = new_log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{sha256}"
    ev["MERKELY_DISPLAY_NAME"] = image_name

    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        context = make_context(env)
        method, url, payload = command_processor.execute(context)

    assert method == "Putting"
    assert url == f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    assert payload == {
        'build_url': 'https://gitlab/build/1456',
        'commit_url': f'https://github/me/project/commit/{commit}',
        'description': 'Created by build 23',
        'filename': image_name,
        'git_commit': commit,
        'is_compliant': True,
        'sha256': sha256,
    }
    assert blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_artifact',
        'MERKELY_IS_COMPLIANT: True'
    ]


def test_each_required_env_var_missing(capsys):
    for arg in make_command_args():
        if isinstance(arg, RequiredEnvVar):
            ev = new_log_artifact_env(any_commit())
            ev.pop(arg.name)
            with dry_run(ev) as env, scoped_merkelypipe_json():
                context = make_context(env)
                command_processor.execute(context)
    verify_approval(capsys)


def make_command_args():
    env = new_log_artifact_env(any_commit())
    context = make_context(env)
    return make_command(context).args


def old_put_artifact_env(commit, *,
                         build_url_number,
                         build_number):
    return {
        "CDB_API_TOKEN": API_TOKEN,
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_ARTIFACT_GIT_COMMIT": commit,
        "CDB_ARTIFACT_GIT_URL": f"https://github/me/project/commit/{commit}",
        "CDB_CI_BUILD_URL": f"https://gitlab/build/{build_url_number}",
        "CDB_BUILD_NUMBER": build_number
    }


def new_log_artifact_env(commit, *,
                         domain=None,
                         build_url_number=None,
                         build_number=None):
    if domain is None:
        domain = "app.compliancedb.com"
    if build_url_number is None:
        build_url_number = '1456'
    if build_number is None:
        build_number = '23'
    return {
        "MERKELY_COMMAND": "log_artifact",
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{domain}",
        "MERKELY_FINGERPRINT": 'dummy',
        "MERKELY_CI_BUILD_URL": f"https://gitlab/build/{build_url_number}",
        "MERKELY_CI_BUILD_NUMBER": build_number,
        "MERKELY_ARTIFACT_GIT_URL": "https://github/me/project/commit/" + commit,
        "MERKELY_ARTIFACT_GIT_COMMIT": commit,
        "MERKELY_IS_COMPLIANT": "TRUE"
    }


def any_commit():
    return "abc50c8a53f79974d615df335669b59fb56a4ed3"


def blurb(output):
    blurb, _, _, _ = blurb_method_payload_url(output)
    return blurb


def blurb_method_payload_url(output):
    """
    Splits output so each part can be asserted individually.
    """
    other_lines = []
    payload_lines = []
    in_payload = False
    for line in output.splitlines(False):
        if line == "{" or line == "}" or in_payload:
            payload_lines.append(line)
            if line == "{":
                in_payload = True
            if line == "}":
                in_payload = False
        else:
            other_lines.append(line)
            in_payload = False

    import json
    payload = json.loads("".join(payload_lines))
    *blurb, method_line, to_url_line, _dry_run_line = other_lines
    method = method_line.split()[0]
    url = to_url_line.split()[-1]
    return blurb, method, payload, url
