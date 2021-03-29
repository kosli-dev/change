from commands import run, External

from tests.utils import *

DOMAIN = "app.compliancedb.com"
OWNER = "compliancedb"
PIPELINE = "cdb-controls-test-pipeline"


def test_all_env_vars_image(capsys):
    sha256 = "ddcdaef69c676c2466571d3233380d559ccc2032b258fc5e73f99a103db462ee"
    commit = "12037940e4e7503055d8a8eea87e177f04f14616"
    image_name = "acme/widget:3.4"
    build_url = "https://gitlab/build/1456"
    build_number = "23"

    expected_method = "Putting"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/artifacts/"
    expected_payload = {
        "build_url": build_url,
        "commit_url": commit_url(commit),
        "description": f"Created by build {build_number}",
        "filename": image_name,
        "git_commit": commit,
        "is_compliant": True,
        "sha256": sha256,
        "user_data": {}
    }

    # make merkely call
    protocol = "docker://"
    ev = new_log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{image_name}"
    with dry_run(ev) as env:
        with MockDockerFingerprinter(image_name, sha256) as fingerprinter:
            external = External(env=env, docker_fingerprinter=fingerprinter)
            method, url, payload = run(external)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    assert extract_blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_artifact',
        'MERKELY_IS_COMPLIANT: True',
    ]


def test_all_env_vars_file(capsys):
    commit = "abc50c8a53f79974d615df335669b59fb56a4444"
    sha256 = "ccdd89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f5115"
    directory = "app/tests/data"
    filename = "jam.jar"
    artifact_name = f"{directory}/{filename}"
    build_url = "https://gitlab/build/1456"
    build_number = '23'

    expected_method = "Putting"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/artifacts/"
    expected_payload = {
        'build_url': build_url,
        'commit_url': commit_url(commit),
        'description': f'Created by build {build_number}',
        'filename': filename,
        'git_commit': commit,
        'is_compliant': True,
        'sha256': sha256,
        'user_data': {},
    }

    # make merkely call
    protocol = "file://"
    ev = new_log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{artifact_name}"
    with dry_run(ev) as env:
        with MockFileFingerprinter(artifact_name, sha256) as fingerprinter:
            external = External(env=env, file_fingerprinter=fingerprinter)
            method, url, payload = run(external)

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    assert extract_blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_artifact',
        'MERKELY_IS_COMPLIANT: True',
    ]


def test_all_env_vars_sha(capsys):
    commit = "abc50c8a53f79974d615df335669b59fb56a4ed4"
    artifact_name = "door-is-a.jar"
    sha256 = "444daef69c676c2466571d3211180d559ccc2032b258fc5e73f99a103db462ef"
    build_url = "https://gitlab/build/1456"
    build_number = '23'

    expected_method = "Putting"
    expected_url = f"https://{DOMAIN}/api/v1/projects/{OWNER}/{PIPELINE}/artifacts/"
    expected_payload = {
        "build_url": build_url,
        "commit_url": commit_url(commit),
        "description": f"Created by build {build_number}",
        "filename": artifact_name,
        "git_commit": commit,
        "is_compliant": True,
        "sha256": sha256,
        "user_data": {},
    }

    # make merkely call
    protocol = "sha256://"
    ev = new_log_artifact_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{sha256}/{artifact_name}"
    with dry_run(ev) as env:
        method, url, payload = run(External(env=env))

    # verify matching data
    assert method == expected_method
    assert url == expected_url
    assert payload == expected_payload

    assert extract_blurb(capsys_read(capsys)) == [
        'MERKELY_COMMAND=log_artifact',
        'MERKELY_IS_COMPLIANT: True',
    ]


API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"
BUILD_URL = 'https://gitlab/build/1456'
BUILD_NUMBER = '23'


def new_log_artifact_env(commit=None):
    if commit is None:
        commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    return {
        "MERKELY_COMMAND": "log_artifact",
        "MERKELY_OWNER": OWNER,
        "MERKELY_PIPELINE": PIPELINE,
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{DOMAIN}",
        "MERKELY_FINGERPRINT": 'docker://acme/road-runner:2.3',
        "MERKELY_CI_BUILD_URL": BUILD_URL,
        "MERKELY_CI_BUILD_NUMBER": BUILD_NUMBER,
        "MERKELY_ARTIFACT_GIT_URL": commit_url(commit),
        "MERKELY_ARTIFACT_GIT_COMMIT": commit,
        "MERKELY_IS_COMPLIANT": "TRUE"
    }


def commit_url(commit):
    return f"https://github/me/project/commit/{commit}"