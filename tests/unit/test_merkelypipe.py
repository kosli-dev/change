from commands import Command, External
from env_vars import PipePathEnvVar
from errors import ChangeError
from tests.utils import *
from pytest import raises


def test_MEREKELY_OWNER_and_MERKELY_PIPE_LINE_are_used_for_all_commands_except_declare_pipeline():
    os_env = {
        "MERKELY_COMMAND": "log_artifact",
        "MERKELY_OWNER": "acme",
        "MERKELY_PIPELINE": "road-runner",
    }
    external = External(env=os_env)
    cls = Command.named('declare_pipeline')
    json = cls(external).merkelypipe
    assert json["owner"] == "acme"
    assert json["name"] == "road-runner"


def test_MERKELY_OWNER_and_MERKELY_PIPE_override_entries_in_Merkelypipe_even_for_declare_pipeline():
    # declare_pipeline requires a Merkelypipe.json, all other commands don't.
    # Even for declare_pipeline, allow env-vars to override the "owner"
    # and "name" entries so that when anyone is doing the loan-calculator demo
    # they only need to set the values once in the env-vars for all commands.
    os_env = {
        "MERKELY_COMMAND": "declare_pipeline",
        "MERKELY_OWNER": "Acme",
        "MERKELY_PIPELINE": "road-runner-beep-beep",
    }
    external = External(env=os_env)
    cls = Command.named('declare_pipeline')
    with ScopedFileCopier('/app/tests/data/Merkelypipe.json', default_pipe_path()):
        json = cls(external).merkelypipe

    assert json["owner"] == "Acme"
    assert json["name"] == "road-runner-beep-beep"

    
def test_defaults_to_Merkelypipe_dot_json_in_data_dir():
    external = External(env={})
    with ScopedFileCopier('/app/tests/data/Merkelypipe.json', default_pipe_path()):
        json = external.merkelypipe
    assert json['owner'] == 'merkely-test'


def test_env_var_can_override_the_default():
    os_env = {"MERKELY_PIPE_PATH": "/app/tests/data/Merkelypipe.acme-roadrunner.json"}
    external = External(env=os_env)
    json = external.merkelypipe
    assert json['owner'] == 'acme'  # lowercase A


def test_raises_when_not_found():
    not_exist_filename = "/app/tests/data/Merkelypipe.does-not-exist.json"
    os_env = {"MERKELY_PIPE_PATH": not_exist_filename}
    external = External(env=os_env)
    with raises(ChangeError) as exc:
        external.merkelypipe
    assert str(exc.value) == f'{not_exist_filename} file not found.'


def test_raises_when_invalid_json():
    external = External(env={})
    with ScopedFileCopier("/app/tests/data/Merkelypipe.bad.json", default_pipe_path()):
        with raises(ChangeError) as exc:
            external.merkelypipe
    diagnostic = str(exc.value)
    assert diagnostic.startswith(f'{default_pipe_path()} invalid json'), diagnostic


def test_raises_when_is_a_dir():
    external = External(env={})
    with ScopedDirCopier("/app/tests/data", default_pipe_path()):
        with raises(ChangeError) as exc:
            external.merkelypipe
    diagnostic = str(exc.value)
    assert diagnostic.startswith(f'{default_pipe_path()} is a directory'), diagnostic


def default_pipe_path():
    return PipePathEnvVar({}).default


"""
Possible further tests:
TODO: json has no key "owner"
TODO: json "owner" value not string
"""
