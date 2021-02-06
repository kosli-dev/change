from cdb.put_artifact       import put_artifact
from cdb.put_artifact_image import put_artifact_image

from commands import run, build_command, RequiredEnvVar, Context

from tests.utils import *

MERKELY_DOMAIN = "test.compliancedb.com"
CDB_DOMAIN = "app.compliancedb.com"

CDB_OWNER = "compliancedb"
CDB_NAME = "cdb-controls-test-pipeline"

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_log_artifact"

API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"


def test_file_protocol_at_root(capsys, mocker):
    """
    Tests logging a file artifact via the env-var
    MERKELY_FINGERPRINT="file://${FILE_PATH}"
    when FILE_PATH _is_ in the root dir
    """
    # input data
    commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    protocol = "file://"
    directory = ""  # <<<<<
    filename = "jam.jar"
    sha256 = "ddcdaef69c676c2466571d3288880d559ccc2032b258fc5e73f99a103db462ee"
    domain = CDB_DOMAIN
    owner = CDB_OWNER
    name = CDB_NAME
    build_url = "https://gitlab/build/1456"
    build_number = '23'

    # make cdb call
    old_env = old_put_artifact_env(commit,
                                   build_url=build_url,
                                   build_number=build_number)
    old_env["CDB_ARTIFACT_FILENAME"] = filename
    set_env_vars = {'CDB_ARTIFACT_SHA': sha256}
    with dry_run(old_env, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_file', return_value=sha256)
        put_artifact("tests/integration/test-pipefile.json")

    # compare with approved cdb text file
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_file_protocol_at_root"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    expected_payload = {
        'build_url': build_url,
        'commit_url': f'https://github/me/project/commit/{commit}',
        'description': f'Created by build {build_number}',
        'filename': filename,  # <<<<<
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
                              build_url=build_url,
                              build_number=build_number)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{directory}{filename}"
    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        with ScopedFileCopier("/app/tests/data/jam.jar", "/"+filename):
            with MockFileFingerprinter(filename, sha256) as fingerprinter:
                method, url, payload = run(env, fingerprinter)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    assert extract_blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_artifact',
        f'Calculating fingerprint for {protocol}{directory}{filename}',
        f"Calculated fingerprint: {sha256}",
        'MERKELY_IS_COMPLIANT: True'
    ]


def test_file_protocol_not_at_root(capsys, mocker):
    """
    Tests logging a file artifact via the env-var
    MERKELY_FINGERPRINT="file://${FILE_PATH}"
    when FILE_PATH is _not_ in the root dir
    """
    # input data
    commit = "abc50c8a53f79974d615df335669b59fb56a4444"
    sha256 = "ccdd89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f5115"
    protocol = "file://"
    directory = "app/tests/data"  # <<<<<<
    filename = "jam.jar"
    build_url = "https://gitlab/build/1456"
    build_number = '23'

    domain = CDB_DOMAIN
    owner = CDB_OWNER
    name = CDB_NAME

    # make cdb call
    old_env = old_put_artifact_env(commit,
                                   build_url=build_url,
                                   build_number=build_number)
    old_env["CDB_ARTIFACT_FILENAME"] = f"{directory}/{filename}"
    set_env_vars = {'CDB_ARTIFACT_SHA': sha256}
    with dry_run(old_env, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_file', return_value=sha256)
        put_artifact("tests/integration/test-pipefile.json")

    # compare with approved cdb text file
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_file_protocol_not_at_root"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    expected_payload = {
        'build_url': build_url,
        'commit_url': f'https://github/me/project/commit/{commit}',
        'description': f'Created by build {build_number}',
        'filename': f"{directory}/{filename}",  # <<<<
        'git_commit': commit,
        'is_compliant': True,
        'sha256': sha256,
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload

    # make merkely call
    ev = new_log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{directory}/{filename}"

    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        with MockFileFingerprinter(f"{directory}/{filename}", sha256) as fingerprinter:
            method, url, payload = run(env, fingerprinter)

    # verify matching data
    expected_payload['filename'] = filename  # <<<<<

    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    assert extract_blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_artifact',
        f'Calculating fingerprint for {protocol}{directory}/{filename}',
        f"Calculated fingerprint: {sha256}",
        'MERKELY_IS_COMPLIANT: True'
    ]


def test_docker_protocol(capsys, mocker):
    """
    Tests logging a docker image artifact via the env-var
    MERKELY_FINGERPRINT="docker://${IMAGE_NAME}"
    """
    # input data
    sha256 = "ddcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ee"
    commit = "12037940e4e7503055d8a8eea87e177f04f14616"
    protocol = "docker://"
    image_name = "acme/widget:3.4"
    build_url = "https://gitlab/build/1456"
    build_number = "23"

    domain = CDB_DOMAIN
    owner = CDB_OWNER
    name = CDB_NAME

    # make cdb call
    old_env = {
        "CDB_API_TOKEN": API_TOKEN,
        "CDB_ARTIFACT_DOCKER_IMAGE": image_name,
        "CDB_BUILD_NUMBER": build_number,
        "CDB_CI_BUILD_URL": build_url,
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_ARTIFACT_GIT_URL": f"https://github/me/project/commit/{commit}",
        "CDB_ARTIFACT_GIT_COMMIT": commit,
    }
    with dry_run(old_env):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha256)
        put_artifact_image("tests/integration/test-pipefile.json")

    # compare with approved cdb text file
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_docker_protocol"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    expected_payload = {
        "build_url": build_url,
        "commit_url": f"https://github/me/project/commit/{commit}",
        "description": f"Created by build {build_number}",
        "filename": image_name,
        "git_commit": commit,
        "is_compliant": True,
        "sha256": sha256
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload

    # make merkely call
    ev = new_log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{image_name}"
    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        with MockImageFingerprinter(image_name, sha256) as fingerprinter:
            method, url, payload = run(env, fingerprinter)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    assert extract_blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_artifact',
        f'Calculating fingerprint for {protocol}{image_name}',
        f"Calculated fingerprint: {sha256}",
        'MERKELY_IS_COMPLIANT: True'
    ]


def test_sha256_protocol_file(capsys):
    """
    Tests logging a file artifact via the env-vars
    MERKELY_FINGERPRINT="sha256://${SHA256}"
    MERKELY_DISPLAY_NAME="${FILE_PATH}"
    """
    # input data
    commit = "abc50c8a53f79974d615df335669b59fb56a4ed4"
    sha256 = "444daef69c676c2466571d3211180d559ccc2032b258fc5e73f99a103db462ef"
    protocol = "sha256://"
    filename = "door-is-a.jar"
    build_url = "https://gitlab/build/2156"
    build_number = '751'

    domain = MERKELY_DOMAIN
    owner = CDB_OWNER
    name = CDB_NAME

    # make merkely call
    ev = new_log_artifact_env(commit,
                              domain=domain,
                              build_url=build_url,
                              build_number=build_number)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{sha256}"
    ev["MERKELY_DISPLAY_NAME"] = filename

    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        method, url, payload = run(env)

    # verify data
    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    expected_payload = {
        'build_url': build_url,
        'commit_url': f'https://github/me/project/commit/{commit}',
        'description': f'Created by build {build_number}',
        'filename': filename,
        'git_commit': commit,
        'is_compliant': True,
        'sha256': sha256,
    }

    assert url == expected_url
    assert method == expected_method
    assert payload == expected_payload
    assert extract_blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_artifact',
        'MERKELY_IS_COMPLIANT: True'
    ]

    # TODO: make cdb call
    old_dir = "tests/integration/approved_executions"
    old_file = "test_put_artifact"
    old_test = "test_all_env_vars_uses_FILENAME_and_SHA"
    approved = f"{old_dir}/{old_file}.{old_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)
    assert old_method == method
    assert old_url == url
    assert old_payload == payload


def test_sha256_protocol_docker_image(capsys):
    """
    Tests logging a docker image artifact via the env-vars
    MERKELY_FINGERPRINT="sha256://${SHA256}"
    MERKELY_DISPLAY_NAME="${IMAGE_NAME_AND_TAG}"
    """
    # input data
    commit = "ddc50c8a53f79974d615df335669b59fb56a4ed3"
    sha256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    protocol = "sha256://"
    image_name = "acme/road-runner:4.8"
    build_url = "https://gitlab/build/1456"
    build_number = '23'

    domain = CDB_DOMAIN
    owner = CDB_OWNER
    name = CDB_NAME

    # make merkely call
    ev = new_log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{sha256}"
    ev["MERKELY_DISPLAY_NAME"] = image_name

    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        method, url, payload = run(env)

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    expected_payload = {
        'build_url': build_url,
        'commit_url': f'https://github/me/project/commit/{commit}',
        'description': f'Created by build {build_number}',
        'filename': image_name,
        'git_commit': commit,
        'is_compliant': True,
        'sha256': sha256,
    }
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload
    assert extract_blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_artifact',
        'MERKELY_IS_COMPLIANT: True'
    ]
    # TODO: make cdb call
    #old_dir = "tests/integration/approved_executions"
    #old_file = "test_put_artifact"
    #old_test = "test_required_env_vars_uses_CDB_ARTIFACT_SHA"


def test_unknown_protocol(capsys):
    # input data
    commit = "ddc50c8a53f79974d615df335669b59fb56a4ed3"
    sha256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    protocol = "ash256://"
    image_name = "acme/road-runner:4.8"

    # make merkely call
    ev = new_log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{sha256}"
    ev["MERKELY_DISPLAY_NAME"] = image_name

    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        status = run(env)

    assert status != 0
    verify_approval(capsys, ["out"])


# TODO: Test when sha256://SHA and SHA does not look like a SHA?

# TODO: test_sha256_protocol_file() when DISPLAY_NAME is missing
# TODO: test_sha256_protocol_file() when supplied DISPLAY_NAME has full path...?
# TODO: test when all optional env-var are not supplied

# TODO: Test when docker image not found (decent error message)
# TODO: Test when image not pushed (eg to dockerhub) so cannot get digest (decent error message)
# TODO: Test when docker socket not volume-mounted


def test_each_required_env_var_missing(capsys):
    for env_var in make_command_env_vars():
        if isinstance(env_var, RequiredEnvVar):
            ev = new_log_artifact_env()
            ev.pop(env_var.name)
            with dry_run(ev) as env, scoped_merkelypipe_json():
                run(env)
    verify_approval(capsys)


def make_command_env_vars():
    env = new_log_artifact_env()
    context = Context(env)
    return build_command(context).env_vars


def old_put_artifact_env(commit, *,
                         build_url,
                         build_number):
    return {
        "CDB_API_TOKEN": API_TOKEN,
        "CDB_IS_COMPLIANT": "TRUE",
        "CDB_ARTIFACT_GIT_COMMIT": commit,
        "CDB_ARTIFACT_GIT_URL": f"https://github/me/project/commit/{commit}",
        "CDB_CI_BUILD_URL": build_url,
        "CDB_BUILD_NUMBER": build_number
    }


def new_log_artifact_env(commit=None, *,
                         domain=None,
                         build_url=None,
                         build_number=None):
    if commit is None:
        commit = any_commit()
    if domain is None:
        domain = "app.compliancedb.com"
    if build_url is None:
        build_url = 'https://gitlab/build/1456'
    if build_number is None:
        build_number = '23'
    return {
        "MERKELY_COMMAND": "log_artifact",
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{domain}",
        "MERKELY_FINGERPRINT": 'dummy',
        "MERKELY_CI_BUILD_URL": build_url,
        "MERKELY_CI_BUILD_NUMBER": build_number,
        "MERKELY_ARTIFACT_GIT_URL": "https://github/me/project/commit/" + commit,
        "MERKELY_ARTIFACT_GIT_COMMIT": commit,
        "MERKELY_IS_COMPLIANT": "TRUE"
    }


def any_commit():
    return "abc50c8a53f79974d615df335669b59fb56a4ed3"

