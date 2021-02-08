from cdb.put_artifact       import put_artifact
from cdb.put_artifact_image import put_artifact_image

from commands import run, build_command, Context
from env_vars import RequiredEnvVar

from tests.utils import *

CDB_DOMAIN = "app.compliancedb.com"
CDB_OWNER = "compliancedb"
CDB_NAME = "cdb-controls-test-pipeline"

APPROVAL_DIR = "tests/unit/approved_executions"
APPROVAL_FILE = "test_m_log_artifact"


def test_all_env_vars_image(capsys, mocker):
    """
    New: MERKELY_COMMAND=log_artifact
         MERKELY_FINGERPRINT="docker://${IMAGE_NAME}"
         docker run ... merkely/change
    Old: CDB_ARTIFACT_DOCKER_IMAGE=${IMAGE_NAME}
         docker run ... cdb.put_artifact_image ...
    """
    # input data
    sha256 = "ddcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ee"
    commit = "12037940e4e7503055d8a8eea87e177f04f14616"
    image_name = "acme/widget:3.4"
    build_url = "https://gitlab/build/1456"
    build_number = "23"

    domain = CDB_DOMAIN
    owner = CDB_OWNER
    name = CDB_NAME

    # make cdb call
    env = old_put_artifact_env(commit)
    env["CDB_ARTIFACT_DOCKER_IMAGE"] = image_name
    with dry_run(env):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_docker_image', return_value=sha256)
        put_artifact_image("tests/integration/test-pipefile.json")  # <<<<<<

    # compare with approved cdb text file
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_all_env_vars_image"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    expected_payload = {
        "build_url": build_url,
        "commit_url": commit_url(commit),
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
    protocol = "docker://"
    ev = new_log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{image_name}"
    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        with MockDockerFingerprinter(image_name, sha256) as fingerprinter:
            method, url, payload = run(env, fingerprinter, None)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    assert extract_blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_artifact',
        'MERKELY_IS_COMPLIANT: True',
        f'Calculating fingerprint for {protocol}{image_name}',
        f"Calculated fingerprint: {sha256}",
    ]


def test_all_env_vars_file(capsys, mocker):
    """
    New: MERKELY_COMMAND=log_artifact
         MERKELY_FINGERPRINT="file://${FILE_PATH}"
         docker run ... merkely/change
    Old: CDB_ARTIFACT_FILENAME=${FILE_PATH}
         docker run ... cdb.put_artifact ...
    """
    # input data
    commit = "abc50c8a53f79974d615df335669b59fb56a4444"
    sha256 = "ccdd89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f5115"
    artifact_name = "app/tests/data/jam.jar"
    build_url = "https://gitlab/build/1456"
    build_number = '23'

    domain = CDB_DOMAIN
    owner = CDB_OWNER
    name = CDB_NAME

    # make cdb call
    old_env = old_put_artifact_env(commit)
    old_env["CDB_ARTIFACT_FILENAME"] = artifact_name
    set_env_vars = {'CDB_ARTIFACT_SHA': sha256}
    with dry_run(old_env, set_env_vars):
        mocker.patch('cdb.cdb_utils.calculate_sha_digest_for_file', return_value=sha256)
        put_artifact("tests/integration/test-pipefile.json")

    # compare with approved cdb text file
    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_all_env_vars_file"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    expected_payload = {
        'build_url': build_url,
        'commit_url': commit_url(commit),
        'description': f'Created by build {build_number}',
        'filename': artifact_name,
        'git_commit': commit,
        'is_compliant': True,
        'sha256': sha256,
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload

    # make merkely call
    protocol = "file://"
    ev = new_log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{artifact_name}"
    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        with MockFileFingerprinter(artifact_name, sha256) as fingerprinter:
            method, url, payload = run(env, None, fingerprinter)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    assert extract_blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_artifact',
        'MERKELY_IS_COMPLIANT: True',
        f'Calculating fingerprint for {protocol}{artifact_name}',
        f"Calculated fingerprint: {sha256}",
    ]


def test_all_env_vars_sha(capsys, mocker):
    """
    New: MERKELY_COMMAND=log_artifact
         MERKELY_FINGERPRINT="sha256://${SHA256}/${FILE_PATH}"
         docker run ... merkely/change
    Old: CDB_ARTIFACT_FILENAME=${FILE_PATH}
         CDB_ARTIFACT_SHA=${SHA256}
         docker run ... cdb.put_artifact ...
    """

    commit = "abc50c8a53f79974d615df335669b59fb56a4ed4"
    artifact_name = "door-is-a.jar"
    sha256 = "444daef69c676c2466571d3211180d559ccc2032b258fc5e73f99a103db462ef"
    build_url = "https://gitlab/build/1456"
    build_number = '23'

    domain = "app.compliancedb.com"
    owner = "compliancedb"
    name = "cdb-controls-test-pipeline"

    env = old_put_artifact_env(commit)
    env["CDB_ARTIFACT_FILENAME"] = artifact_name
    env["CDB_ARTIFACT_SHA"] = sha256
    set_env_vars = {}
    with dry_run(env, set_env_vars):
        put_artifact("tests/integration/test-pipefile.json")

    verify_approval(capsys, ["out"])

    # extract data from approved cdb text file
    this_test = "test_all_env_vars_sha"
    approved = f"{APPROVAL_DIR}/{APPROVAL_FILE}.{this_test}.approved.txt"
    with open(approved) as file:
        old_approval = file.read()
    _old_blurb, old_method, old_payload, old_url = extract_blurb_method_payload_url(old_approval)

    expected_method = "Putting"
    expected_url = f"https://{domain}/api/v1/projects/{owner}/{name}/artifacts/"
    expected_payload = {
        "build_url": build_url,
        "commit_url": commit_url(commit),
        "description": f"Created by build {build_number}",
        "filename": artifact_name,
        "git_commit": commit,
        "is_compliant": True,
        "sha256": sha256
    }

    # verify data from approved cdb text file
    assert old_method == expected_method
    assert old_url == expected_url
    assert old_payload == expected_payload

    # make merkely call
    protocol = "sha256://"
    ev = new_log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{sha256}/{artifact_name}"
    merkelypipe = "Merkelypipe.compliancedb.json"
    with dry_run(ev) as env, scoped_merkelypipe_json(merkelypipe):
        method, url, payload = run(env, None, None)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    assert extract_blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_artifact',
        'MERKELY_IS_COMPLIANT: True',
    ]


# TODO: test when all optional env-var are not supplied


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


API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"
BUILD_URL = 'https://gitlab/build/1456'
BUILD_NUMBER = '23'


def old_put_artifact_env(commit):
    return {
        "CDB_API_TOKEN": API_TOKEN,
        "CDB_ARTIFACT_GIT_COMMIT": commit,
        "CDB_ARTIFACT_GIT_URL": commit_url(commit),
        "CDB_CI_BUILD_URL": BUILD_URL,
        "CDB_BUILD_NUMBER": BUILD_NUMBER,
        "CDB_IS_COMPLIANT": "TRUE",
    }


def new_log_artifact_env(commit=None):
    if commit is None:
        commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    domain = "app.compliancedb.com"
    return {
        "MERKELY_COMMAND": "log_artifact",
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{domain}",
        "MERKELY_FINGERPRINT": 'dummy',
        "MERKELY_CI_BUILD_URL": BUILD_URL,
        "MERKELY_CI_BUILD_NUMBER": BUILD_NUMBER,
        "MERKELY_ARTIFACT_GIT_URL": commit_url(commit),
        "MERKELY_ARTIFACT_GIT_COMMIT": commit,
        "MERKELY_IS_COMPLIANT": "TRUE"
    }


def commit_url(commit):
    return f"https://github/me/project/commit/{commit}"