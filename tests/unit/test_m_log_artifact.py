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

API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"


def test_all_env_vars(capsys, mocker):
    """
    Uses
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
    this_test = "test_all_env_vars"
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


# TODO: test when all optional env-var are not supplied


def test_each_required_env_var_missing(capsys):
    for env_var in make_command_env_vars():
        #if env_var.name == 'MERKELY_FINGERPRINT':
        #    continue
        #if env_var.name == 'MERKELY_DISPLAY_NAME':
        #    continue
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

