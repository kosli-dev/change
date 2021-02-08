from commands import LogArtifactCommand, Context, CommandError
from commands import DisplayNameEnvVar
from pytest import raises

SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_when_fingerprint_has_sha_protocol_value_is_from_env_var():
    artifact_name = "acme/road-runner:3.4"
    env, display_name = make_test_vars('sha256://', SHA256)
    env["MERKELY_DISPLAY_NAME"] = artifact_name
    assert display_name.value == artifact_name


def test_when_fingerprint_has_docker_protocol_value_is_its_image_and_tag():
    artifact_name = "acme/road-runner:4.8"
    _env, display_name = make_test_vars('docker://', artifact_name)
    assert display_name.value == artifact_name


def test_when_fingerprint_has_file_protocol_value_is_basename_of_its_filepath():
    artifact_name = "jam.jar"
    directory = "/user/artifact"
    _env, display_name = make_test_vars('file://', f"{directory}/{artifact_name}")
    assert display_name.value == artifact_name


def test_when_fingerprint_has_unknown_protocol_value_raises():
    _env, display_name = make_test_vars('ash256://', SHA256)
    with raises(CommandError) as exc:
        display_name.value
    assert str(exc.value) == f"Unknown protocol: ash256://{SHA256}"


def make_test_vars(protocol, artifact_name):
    fingerprint = f"{protocol}{artifact_name}"
    env = {
        "MERKELY_FINGERPRINT": fingerprint
    }
    context = Context(env, None, None)
    command = LogArtifactCommand(context)
    return env, DisplayNameEnvVar(command)
