from commands import run
from tests.utils import *


def test_docker_image(capsys):
    commit = "abc50c8a53f79974d615df335669b59fb56a4ed3"
    digest = "ccdd89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"
    protocol = "docker://"
    image_name = "acme/road-runner:6.8"
    ev = create_deployment_env(commit)
    ev["MERKELY_FINGERPRINT"] = f"{protocol}{image_name}"

    with dry_run(ev) as env, scoped_merkelypipe_json():
        with MockDockerFingerprinter(image_name, digest) as fingerprinter:
            run(env, fingerprinter, None)

    verify_approval(capsys)
    #verify_payload_and_url(capsys)



def create_deployment_env(commit):
    ev = {
        "MERKELY_CI_BUILD_URL": "https://gitlab/build/1456",
        "MERKELY_ENVIRONMENT": "production",
        "MERKELY_DESCRIPTION": "some description",
        "MERKELY_USER_DATA_FILE": "/app/tests/data/user_data.json",
    }
    return {**core_env_vars("create_deployment"), **ev}

